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
            
        matches = page_handler.confirmed_controller.cleanerViewMatches(cleaner_id)
        
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
        if matches:
            for match in matches:
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
            matches=formatted_matches,
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
            matches=[],
            start_date='',
            end_date=''
        )



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