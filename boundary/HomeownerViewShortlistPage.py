from flask import Blueprint, render_template, request, redirect, url_for, session
from control.HomeownerViewShortlistController import HomeownerViewShortlistController
from control.HomeownerSearchShortlistController import HomeownerSearchShortlistController

view_shortlist_bp = Blueprint('view_shortlist', __name__)

@view_shortlist_bp.route('/homeowner_base')
def homeowner_base():
    return render_template('homeowner_base.html')

@view_shortlist_bp.route('/homeowner_base/view_shortlist')
def view_shortlist():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        shortlist = HomeownerSearchShortlistController.homeownerSearchShortlist(userid, search_query)
    else:
        shortlist = HomeownerViewShortlistController.homeownerViewShortlist(userid)


    return render_template('view_shortlist.html', shortlist=shortlist.values())

