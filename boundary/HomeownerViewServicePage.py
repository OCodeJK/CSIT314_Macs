from flask import Blueprint, render_template, request, redirect, url_for, session
from control.HomeownerViewServiceController import HomeownerViewServiceController
from control.HomeownerSearchServiceController import HomeownerSearchServiceController
from control.HomeownerCreateShortlistController import HomeownerCreateShortlistController

view_hoservice_bp = Blueprint('view_hoservice', __name__)

@view_hoservice_bp.route('/homeowner_base')
def homeowner_base():
    return render_template('homeowner_base.html')

@view_hoservice_bp.route('/view_hoservice')
def view_service():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        services = HomeownerSearchServiceController.homeownerSearchService(search_query)
        print("testttt: ", services)
    else:
        services = HomeownerViewServiceController.homeownerViewService()
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


@view_hoservice_bp.route('/inc_viewcount', methods=['POST'])
def inc_viewcount(): # increase viewcount of service when full service is viewed
    serviceid = request.form.get("serviceid") #get the search input from clicking view more details
    print("serviceid: ", serviceid)
    final = HomeownerViewServiceController.homeownerIncViewcount(serviceid)

    return ''  # Don't return anything