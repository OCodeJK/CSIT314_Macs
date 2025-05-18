from flask import Blueprint, render_template, request, redirect, flash
from control.CleanerViewConfirmedMatchesController import CleanerViewConfirmedMatchesController
from control.CleanerFilterHistoryController import CleanerFilterHistoryController
from control.CleanerSearchHistoryController import CleanerSearchHistoryController
from datetime import datetime

history_bp = Blueprint('cleaner_history', __name__)

class CleanerHistoryPg:
    def __init__(self):
        self.confirmed_controller = CleanerViewConfirmedMatchesController()
        self.filter_controller = CleanerFilterHistoryController()
        self.search_controller = CleanerSearchHistoryController()

page_handler = CleanerHistoryPg()

@history_bp.route('/cleaner/history', methods=['GET'])
def display_history():
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        search_query = request.args.get('search_query', '')
        
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
        
        history = []
        
        if search_query:
            history = page_handler.search_controller.cleanerSearchService(search_query, cleaner_id)
        elif start_date or end_date:
            history = page_handler.filter_controller.filterHistory(cleaner_id, start_date_obj, end_date_obj)
        else:
            history = page_handler.confirmed_controller.cleanerViewMatches(cleaner_id)
        
        if not isinstance(history, list):
            history = []
        
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
        
        formatted_history.sort(key=lambda x: x['startDate'] if x['startDate'] else '', reverse=True)
        
        return render_template(
            'history.html', 
            cleaner_id=cleaner_id,
            search_query=search_query,
            history=formatted_history,
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
            start_date='',
            end_date=''
        )

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