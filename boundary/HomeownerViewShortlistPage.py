from flask import Blueprint, render_template, request, redirect, url_for, session
from control.HomeownerViewShortlistController import HomeownerViewShortlistController
from control.HomeownerSearchShortlistController import HomeownerSearchShortlistController

view_hoshortlist_bp = Blueprint('view_hoshortlist', __name__)

@view_hoshortlist_bp.route('/view_hoshortlist')
def view_shortlist():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        shortlist = HomeownerSearchShortlistController.homeownerSearchShortlist(userid, search_query)
    else:
        shortlist = HomeownerViewShortlistController.homeownerViewShortlist(userid)


    return render_template('view_hoshortlist.html', shortlist=shortlist)

