from flask import Blueprint, render_template, request, redirect, flash
from control.CleanerFilterHistoryController import CleanerFilterHistoryController
from control.CleanerConfirmedMatchesController import CleanerConfirmedMatchesController
from datetime import datetime

filter_history_bp = Blueprint('filter_history', __name__)

class CleanerFilterHistoryPg:
   def __init__(self):
       self.controller = CleanerFilterHistoryController()
       self.matches_controller = CleanerConfirmedMatchesController()

cleaner_filter_pg = CleanerFilterHistoryPg()

@filter_history_bp.route('/cleaner/history/filter', methods=['GET'])
def display_history():
   try:
       return apply_history_filters(request)
   except Exception as e:
       flash(f"An error occurred while loading history records: {str(e)}", "error")
       return render_template('history.html', cleaner_id=request.args.get('cleaner_id', '1'),
                             history=[], matches=[], search_query='', start_date='', end_date='')

@filter_history_bp.route('/cleaner/history/filter_records', methods=['GET'])
def filter_records():
   return display_history()

@filter_history_bp.route('/cleaner/history/details/<history_id>', methods=['GET'])
def view_history_details(history_id):
   cleaner_id = request.args.get('cleaner_id', '1')
   return get_history_details(history_id, cleaner_id)

@filter_history_bp.route('/cleaner/service/end', methods=['GET'])
def end_service():
   try:
       cleaner_id = request.args.get('cleaner_id', '1')
       service_id = request.args.get('service_id')
       
       if not service_id:
           flash("Service ID is required", "error")
           return redirect('/cleaner/history/filter?cleaner_id=' + cleaner_id)
       
       
       result = cleaner_filter_pg.controller.endService(cleaner_id, service_id)
       
       flash("Service has been successfully completed" if result else 
             "Failed to end service. It may already be completed or does not exist.", 
             "success" if result else "error")
           
       return redirect('/cleaner/history/filter?cleaner_id=' + cleaner_id)
   except Exception as e:
       flash(f"An error occurred while ending the service: {str(e)}", "error")
       return redirect('/cleaner/history/filter?cleaner_id=' + cleaner_id)

def apply_history_filters(request):
   try:
       cleaner_id = request.args.get('cleaner_id', '1')
       start_date = request.args.get('start_date', '')
       end_date = request.args.get('end_date', '')
       
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

       filtered_history = cleaner_filter_pg.controller.filterHistory(cleaner_id, start_date_obj, end_date_obj)
       
       if not isinstance(filtered_history, list):
           filtered_history = []
       
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

       matches = cleaner_filter_pg.matches_controller.cleanerViewMatches(cleaner_id)
       
       formatted_matches = []
       if matches:
           for match in matches:
               formatted_matches.append({
                   'matchId': match[0],
                   'serviceId': match[1],
                   'date': match[2],
                   'serviceName': match[5] if len(match) > 5 else 'Unknown Service'
               })
       
       return render_template('history.html', cleaner_id=cleaner_id, history=formatted_history,
                             matches=formatted_matches, search_query='',
                             start_date=start_date, end_date=end_date)
   except Exception as e:
       flash(f"An error occurred while filtering history records: {str(e)}", "error")
       return render_template('history.html', cleaner_id=request.args.get('cleaner_id', '1'),
                             history=[], matches=[], search_query='', start_date='', end_date='')
   


def get_history_details(history_id, cleaner_id):
   try:
       record = cleaner_filter_pg.controller.getHistoryDetails(history_id, cleaner_id)
       
       if not record:
           flash("History record not found or you don't have permission to view it", "error")
           return redirect('/cleaner/history/filter?cleaner_id=' + cleaner_id)
       
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
       
       return render_template('history_detail.html', cleaner_id=cleaner_id, record=formatted_record)
   except Exception as e:
       flash(f"An error occurred while loading history details: {str(e)}", "error")
       return redirect('/cleaner/history/filter?cleaner_id=' + cleaner_id)