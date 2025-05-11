from flask import Blueprint, render_template, request, flash
from control.CleanerSearchHistoryController import CleanerSearchHistoryController

cleaner_search_history_bp = Blueprint('cleaner_search_history', __name__)

class CleanerSearchHistoryPage:
   def __init__(self):
       self.controller = CleanerSearchHistoryController()

page = CleanerSearchHistoryPage()

@cleaner_search_history_bp.route('/cleaner/history/search', methods=['GET', 'POST'])
def search_history():
   return search_service_history()

def search_service_history():
   try:
       cleaner_id = request.form.get('cleaner_id', request.args.get('cleaner_id', '1'))
       search_query = request.form.get('search_query', request.args.get('search_query', ''))
       
       history = page.controller.cleanerSearchService(search_query, cleaner_id)
       
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
       
       return render_template(
           'history.html',
           cleaner_id=cleaner_id,
           search_query=search_query,
           history=formatted_history,
           matches=[],
           start_date='',
           end_date=''
       )
   except Exception as e:
       flash(f"An error occurred: {str(e)}", "error")
       return render_template(
           'history.html',
           cleaner_id=request.form.get('cleaner_id', request.args.get('cleaner_id', '1')),
           search_query=request.form.get('search_query', request.args.get('search_query', '')),
           history=[],
           matches=[],
           start_date='',
           end_date=''
       )