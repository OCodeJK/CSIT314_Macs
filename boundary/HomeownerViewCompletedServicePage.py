from flask import Blueprint, render_template, request, redirect, url_for, session
from control.HomeownerViewCompletedServiceController import HomeownerViewCompletedServiceController
from control.HomeownerSearchCompletedServiceController import HomeownerSearchCompletedServiceController

view_completedservice_bp = Blueprint('view_completedservice', __name__)

@view_completedservice_bp.route('/homeowner_base')
def homeowner_base():
    return render_template('homeowner_base.html')

@view_completedservice_bp.route('/view_completedservice')
def view_completedservice():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    date_range = request.args.get('datefilter', '') #get the search input from the URL
    print("test date: ",date_range)
    
    if search_query and not date_range: #search only
        completedservice = HomeownerSearchCompletedServiceController.homeownerSearchCompletedService(userid, search_query)
    elif not search_query and date_range: #date only
        completedservice = HomeownerSearchCompletedServiceController.homeownerSearchCompletedServiceDateOnly(userid, date_range)
    elif search_query and date_range: #search and date
        completedservice = HomeownerSearchCompletedServiceController.homeownerSearchCompletedServiceSearchNDate(userid, search_query, date_range)
    else:
        completedservice = HomeownerViewCompletedServiceController.homeownerViewCompletedService(userid)
    


    return render_template('view_completedservice.html', completedservice=completedservice)

