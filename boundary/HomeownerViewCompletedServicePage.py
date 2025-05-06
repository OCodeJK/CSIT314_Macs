from flask import Blueprint, render_template, request, redirect, url_for, session
from control.HomeownerViewCompletedServiceController import HomeownerViewCompletedServiceController
from control.HomeownerSearchCompletedServiceController import HomeownerSearchCompletedServiceController

view_completedservice_bp = Blueprint('view_completedservice', __name__)

@view_completedservice_bp.route('/homeowner_base')
def homeowner_base():
    return render_template('homeowner_base.html')

@view_completedservice_bp.route('/homeowner_base/view_completedservice')
def view_completedservice():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    date_range = request.args.get('datefilter', '') #get the search input from the URL
    print(date_range)
    
    if search_query:
        completedservice = HomeownerSearchCompletedServiceController.homeownerSearchCompletedService(userid, search_query)
    else:
        completedservice = HomeownerViewCompletedServiceController.homeownerViewCompletedService(userid)
    


    return render_template('view_completedservice.html', completedservice=completedservice)

