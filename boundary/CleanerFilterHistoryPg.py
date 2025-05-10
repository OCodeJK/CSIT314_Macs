from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from control.CleanerFilterHistoryController import CleanerFilterHistoryController
from control.CleanerConfirmedMatchesController import CleanerConfirmedMatchesController
from entity.HistoryRecord import HistoryRecord
from datetime import datetime, timedelta

# Create blueprint with name matching routes in templates
filter_history_bp = Blueprint('filter_history', __name__)

class CleanerFilterHistoryPg:

    def __init__(self):
        # Initialize controller for business logic
        self.controller = CleanerFilterHistoryController()

    def apply_history_filters(self, request):
        try:
            # Extract filter parameters from request
            cleaner_id = request.args.get('cleaner_id', '1')
            search_query = request.args.get('search_query', '')
            start_date = request.args.get('start_date', '')
            end_date = request.args.get('end_date', '')

            # Initialize date objects
            start_date_obj = None
            end_date_obj = None

            # Process manual date inputs
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                except ValueError:
                    flash("Invalid start date format", "error")

            if end_date:
                try:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                except ValueError:
                    flash("Invalid end date format", "error")

            # Get the base history records to filter on
            if search_query:
                filtered_history = HistoryRecord.searchService(search_query, cleaner_id)
            else:
                filtered_history = HistoryRecord.get_cleaner_history(cleaner_id)

            # Apply date filter if provided
            if (start_date_obj or end_date_obj) and filtered_history:
                date_filtered = []
                for record in filtered_history:
                    # Get start date from record
                    record_start_date = record[2]
                    if isinstance(record_start_date, str):
                        try:
                            record_start_date = datetime.strptime(record_start_date, '%Y-%m-%d').date()
                        except ValueError:
                            continue
                    
                    # Check if record falls within date range
                    if (not start_date_obj or record_start_date >= start_date_obj) and \
                       (not end_date_obj or record_start_date <= end_date_obj):
                        date_filtered.append(record)
                
                filtered_history = date_filtered

            # Format records for template rendering
            formatted_history = []
            if filtered_history:
                for record in filtered_history:
                    formatted_history.append({
                        'historyId': record[0],
                        'serviceId': record[1],
                        'startDate': record[2],
                        'endDate': record[3],
                        'cleanerId': record[4],
                        'serviceName': record[5] if len(record) > 5 else 'Unknown Service'
                    })

            # Get confirmed matches for display
            matches_controller = CleanerConfirmedMatchesController()
            matches = matches_controller.cleanerViewMatches(cleaner_id)
            
            # Format matches for template
            formatted_matches = []
            if matches:
                for match in matches:
                    formatted_matches.append({
                        'matchId': match[0],
                        'serviceId': match[1],
                        'date': match[2],
                        'serviceName': match[5] if len(match) > 5 else 'Unknown Service'
                    })

            # Render template for regular requests
            return render_template(
                'history.html',
                cleaner_id=cleaner_id,
                history=formatted_history,
                matches=formatted_matches,
                search_query=search_query,
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            print(f"Error in apply_history_filters: {str(e)}")
            # Handle exceptions and provide user feedback
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(error=str(e)), 500
            flash(f"An error occurred while filtering history records: {str(e)}", "error")
            # Return a fallback template instead of redirecting
            return render_template(
                'history.html',
                cleaner_id=request.args.get('cleaner_id', '1'),
                history=[],
                matches=[],
                search_query='',
                start_date='',
                end_date=''
            )

    def view_history_details(self, history_id, cleaner_id):
        try:
            # Get record details from the database
            record = HistoryRecord.getHistoryDetails(history_id, cleaner_id)
            
            if not record:
                flash("History record not found or you don't have permission to view it", "error")
                return redirect(url_for('cleaner_filter_history.filter_records', cleaner_id=cleaner_id))
            
            # Format the record for the template
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
            
            # Render the template with the record data
            return render_template(
                'history_detail.html',
                cleaner_id=cleaner_id,
                record=formatted_record
            )
        except Exception as e:
            print(f"Error in view_history_details: {str(e)}")
            flash(f"An error occurred while loading history details: {str(e)}", "error")
            return redirect(url_for('cleaner_filter_history.filter_records', cleaner_id=cleaner_id))


# Route definitions
@filter_history_bp.route('/cleaner/history/filter', methods=['GET'])
def display_history():
    """
    Display filtered history records
    """
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        
        # Create instance of the page class
        cleanerFilterPg = CleanerFilterHistoryPg()
        
        # For AJAX requests, just return filtered data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return cleanerFilterPg.apply_history_filters(request)
        
        # Check for filter parameters
        search_query = request.args.get('search_query', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        # If filters applied, use filter method
        if search_query or start_date or end_date:
            return cleanerFilterPg.apply_history_filters(request)
        
        # Otherwise, get all history records
        history_records = HistoryRecord.get_cleaner_history(cleaner_id)
        
        # Format history records for template
        formatted_history = []
        if history_records:
            for record in history_records:
                formatted_history.append({
                    'historyId': record[0],
                    'serviceId': record[1],
                    'startDate': record[2],
                    'endDate': record[3],
                    'cleanerId': record[4],
                    'serviceName': record[5] if len(record) > 5 else 'Unknown Service'
                })
        
        # Get confirmed matches for display
        controller = CleanerConfirmedMatchesController()
        matches = controller.cleanerViewMatches(cleaner_id)
        
        # Format matches for template
        formatted_matches = []
        if matches:
            for match in matches:
                formatted_matches.append({
                    'matchId': match[0],
                    'serviceId': match[1],
                    'date': match[2],
                    'serviceName': match[5] if len(match) > 5 else 'Unknown Service'
                })
        
        # Render template with both history and matches
        return render_template(
            'history.html',
            cleaner_id=cleaner_id,
            history=formatted_history,
            matches=formatted_matches,
            search_query=search_query,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        print(f"Error in display_history: {str(e)}")
        flash(f"An error occurred while loading history records: {str(e)}", "error")
        # Return a fallback template instead of redirecting
        return render_template(
            'history.html',
            cleaner_id=request.args.get('cleaner_id', '1'),
            history=[],
            matches=[],
            search_query='',
            start_date='',
            end_date=''
        )

# Backward compatibility route
@filter_history_bp.route('/cleaner/history/filter_records', methods=['GET'])
def filter_records():
    """
    Alias for display_history for backward compatibility
    """
    return display_history()

@filter_history_bp.route('/cleaner/history/details/<history_id>', methods=['GET'])
def view_history_details(history_id):
    """
    View details of a specific history record
    """
    cleaner_id = request.args.get('cleaner_id', '1')
    cleanerFilterPg = CleanerFilterHistoryPg()
    return cleanerFilterPg.view_history_details(history_id, cleaner_id)

@filter_history_bp.route('/cleaner/service/end', methods=['GET'])
def end_service():
    """
    Mark a service as completed by setting its end date
    """
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        service_id = request.args.get('service_id')
        
        if not service_id:
            flash("Service ID is required", "error")
            return redirect(url_for('cleaner_filter_history.filter_records', cleaner_id=cleaner_id))
        
        # Call entity method to end service
        result = HistoryRecord.end_service(cleaner_id, service_id)
        
        if result:
            flash("Service has been successfully completed", "success")
        else:
            flash("Failed to end service. It may already be completed or does not exist.", "error")
            
        return redirect(url_for('cleaner_filter_history.filter_records', cleaner_id=cleaner_id))
    except Exception as e:
        print(f"Error in end_service: {str(e)}")
        flash(f"An error occurred while ending the service: {str(e)}", "error")
        return redirect(url_for('cleaner_filter_history.filter_records', cleaner_id=cleaner_id))