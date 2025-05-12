from flask import Blueprint, render_template, request, redirect, flash
from control.CleanerConfirmedMatchesController import CleanerConfirmedMatchesController
from control.CleanerFilterHistoryController import CleanerFilterHistoryController
from control.CleanerSearchHistoryController import CleanerSearchHistoryController
from datetime import datetime

# Create the blueprint instance - integrating all history functionality
history_bp = Blueprint('cleaner_history', __name__)

class CleanerConfirmedMatchesPg:
    def __init__(self):
        self.confirmed_controller = CleanerConfirmedMatchesController()
        self.filter_controller = CleanerFilterHistoryController()
        self.search_controller = CleanerSearchHistoryController()

page_handler = CleanerConfirmedMatchesPg()

@history_bp.route('/cleaner/history', methods=['GET'])
def display_history():
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        search_query = request.args.get('search_query', '')
        
        # Handle date parsing
        start_date_obj = None
        end_date_obj = None

        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid start date format. Please use YYYY-MM-DD.", "error")

        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid end date format. Please use YYYY-MM-DD.", "error")
        
        # Get history based on filters
        history = []
        
        # If search query is provided, use search controller
        if search_query:
            history = page_handler.search_controller.cleanerSearchService(search_query, cleaner_id)
        else:
            # Otherwise use filter controller
            history = page_handler.filter_controller.filterHistory(cleaner_id, start_date_obj, end_date_obj)
        
        if not isinstance(history, list):
            history = []
            
        # Get active matches and merge into the main history display
        active_matches = page_handler.confirmed_controller.cleanerViewMatches(cleaner_id)
        
        # Format results for template
        formatted_history = []
        if history:
            for record in history:
                formatted_history.append({
                    'historyId': record[0],
                    'serviceId': record[1],
                    'startDate': record[2],
                    'endDate': record[3],
                    'cleanerId': record[4],
                    'serviceName': record[5] if len(record) > 5 else 'Unknown Service'
                })
                
        formatted_matches = []
        if active_matches:
            for match in active_matches:
                # Only add if not already in history (to avoid duplicates)
                match_id = match[0]
                if not any(record['historyId'] == match_id for record in formatted_history):
                    formatted_matches.append({
                        'historyId': match[0],
                        'serviceId': match[1],
                        'startDate': match[2],
                        'endDate': match[3],
                        'cleanerId': match[4],
                        'serviceName': match[5] if len(match) > 5 else 'Unknown Service'
                    })
        
        return render_template(
            'history.html', 
            cleaner_id=cleaner_id,
            search_query=search_query,
            history=formatted_history,
            active_matches=formatted_matches,
            start_date=start_date, 
            end_date=end_date
        )
    except Exception as e:
        print(f"Error in display_history: {str(e)}")
        flash(f"An error occurred: {str(e)}", "error")
        return render_template(
            'history.html',
            cleaner_id=request.args.get('cleaner_id', '1'),
            search_query='',
            history=[],
            active_matches=[],
            start_date='',
            end_date=''
        )

@history_bp.route('/cleaner/history/details/<record_id>', methods=['GET'])
def view_record_details(record_id):
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        
        # Get record details - using the filter controller's getHistoryDetails method
        record = page_handler.filter_controller.getHistoryDetails(record_id, cleaner_id)
        
        if not record:
            flash("Record not found or you don't have permission to view it", "error")
            return redirect('/cleaner/history?cleaner_id=' + cleaner_id)
        
        formatted_record = {
            'historyId': record[0],
            'serviceId': record[1],
            'startDate': record[2].strftime('%Y-%m-%d') if hasattr(record[2], 'strftime') else record[2],
            'endDate': record[3].strftime('%Y-%m-%d') if record[3] and hasattr(record[3], 'strftime') else record[3],
            'cleanerId': record[4],
            'serviceName': record[5] if len(record) > 5 else 'Unknown Service',
            'categoryName': record[6] if len(record) > 6 else 'Unknown Category',
            'price': record[7] if len(record) > 7 else 0.0,
            'viewCount': record[8] if len(record) > 8 else 0
        }
        
        return render_template(
            'history_detail.html',
            cleaner_id=cleaner_id,
            record=formatted_record
        )
    except Exception as e:
        print(f"Error in view_record_details: {str(e)}")
        flash(f"An error occurred while loading details: {str(e)}", "error")
        return redirect('/cleaner/history?cleaner_id=' + cleaner_id)

@history_bp.route('/cleaner/service/end', methods=['GET'])
def end_service():
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        service_id = request.args.get('service_id')
        
        if not service_id:
            flash("Service ID is required", "error")
            return redirect('/cleaner/history?cleaner_id=' + cleaner_id)
        
        result = page_handler.filter_controller.endService(cleaner_id, service_id)
        
        flash("Service has been successfully completed" if result else 
            "Failed to end service. It may already be completed or does not exist.", 
            "success" if result else "error")
            
        return redirect('/cleaner/history?cleaner_id=' + cleaner_id)
    except Exception as e:
        print(f"Error in end_service: {str(e)}")
        flash(f"An error occurred while ending the service: {str(e)}", "error")
        return redirect('/cleaner/history?cleaner_id=' + cleaner_id)

# Redirect from old URLs to new consolidated route
@history_bp.route('/cleaner/confirmed-matches', methods=['GET'])
def redirect_from_confirmed_matches():
    cleaner_id = request.args.get('cleaner_id', '1')
    return redirect('/cleaner/history?cleaner_id=' + cleaner_id)

@history_bp.route('/cleaner/history/filter', methods=['GET'])
def redirect_from_filter():
    cleaner_id = request.args.get('cleaner_id', '1')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    return redirect(f'/cleaner/history?cleaner_id={cleaner_id}&start_date={start_date}&end_date={end_date}')

@history_bp.route('/cleaner/history/search', methods=['GET'])
def redirect_from_search():
    cleaner_id = request.args.get('cleaner_id', '1')
    search_query = request.args.get('search_query', '')
    return redirect(f'/cleaner/history?cleaner_id={cleaner_id}&search_query={search_query}')

# These routes are for backward compatibility
@history_bp.route('/cleaner/match-details/<match_id>', methods=['GET'])
def view_match_details(match_id):
    cleaner_id = request.args.get('cleaner_id', '1')
    return redirect(f'/cleaner/history/details/{match_id}?cleaner_id={cleaner_id}')