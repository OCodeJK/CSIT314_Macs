from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from control.HomeownerViewServiceController import HomeownerViewServiceController
from control.HomeownerSearchServiceController import HomeownerSearchServiceController
from control.HomeownerCreateShortlistController import HomeownerCreateShortlistController
from helper.util_functions import viewServiceForHomeownerH

view_hoservice_bp = Blueprint('view_hoservice', __name__)

@view_hoservice_bp.route('/search_hoservice')
def search_service():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        services = HomeownerSearchServiceController.homeownerSearchService(search_query)
    else:
        services = viewServiceForHomeownerH() #display all service from helper
    return render_template('view_hoservice.html', services=services)

@view_hoservice_bp.route('/add_shortlist', methods=['POST'])
def add_shortlist():
    userid = session.get('userid')
    serviceid = request.form.get("serviceid")

    final = HomeownerCreateShortlistController.homeownerCreateShortlist(serviceid, userid)
    
    if final:
        return redirect(url_for('view_hoservice.view_service', message='Service successfully added to shortlist'))
    else:
        return redirect(url_for('view_hoservice.view_service', message='Service already shortlisted'))


@view_hoservice_bp.route('/view_hoservice', methods=['POST']) 
def view_service(): # ====== VIEW SERVICE USER STORY =======
    serviceid = request.form.get("serviceid") #get the search input from clicking view more details
    final = HomeownerViewServiceController.homeownerViewService(serviceid)

    return jsonify({
        "serviceid": final[0][0],
        "service": final[0][1],  # 'Carpet Cleaning'
        "cleaner": final[0][2],  # 'boom'
        "category": final[0][3],  # 'Dry Cleaning'
        "price": str(final[0][4])  # '1250.00' as string for JSON compatibility
    })