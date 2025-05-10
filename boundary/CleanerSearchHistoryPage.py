from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from control.CleanerSearchHistoryController import CleanerSearchHistoryController
import traceback

# Create the blueprint instance
cleaner_search_history_bp = Blueprint('cleaner_search_history', __name__)

class CleanerSearchHistoryPage:

    def __init__(self):
        self.controller = CleanerSearchHistoryController()
    
    def search_service_history(self):
       
        try:
            # Get parameters from request
            cleaner_id = request.form.get('cleaner_id', request.args.get('cleaner_id', '1'))
            search_query = request.form.get('search_query', request.args.get('search_query', ''))
            
            print(f"Searching history for cleaner {cleaner_id} with query: '{search_query}'")
            
            # Search history records using the controller's function
            history = self.controller.cleanerSearchService(search_query, cleaner_id)
            
            # Format results for display
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
            
            print(f"Found {len(formatted_history)} history records")


            return render_template(
                'history.html',  # Combined view template
                cleaner_id=cleaner_id,
                search_query=search_query,
                history=formatted_history,
                start_date='',  # Empty for filter fields
                end_date=''
            )
        except Exception as e:
            print(f"Error searching history: {e}")
            print(traceback.format_exc())
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(error=str(e)), 500
            flash("An error occurred while searching history records", "error")
            return redirect(url_for('dashboard', cleaner_id=cleaner_id))

# Create an instance of the page class
page = CleanerSearchHistoryPage()

# Define routes using the page class methods
@cleaner_search_history_bp.route('/cleaner/history/search', methods=['GET', 'POST'])
def search_history():
    """Route for searching history records"""
    return page.search_service_history()

# Add a route that can be accessed directly from the history.html form
@cleaner_search_history_bp.route('/history/search', methods=['GET', 'POST'])
def direct_search_history():
    """Alternative route for searching history records"""
    return page.search_service_history()