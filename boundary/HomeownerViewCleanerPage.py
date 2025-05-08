from flask import Blueprint, render_template, request, redirect, url_for, session
from control.HomeownerViewCleanerController import HomeownerViewCleanerController
from control.HomeownerSearchCleanerController import HomeownerSearchCleanerController
from control.HomeownerCreateShortlistController import HomeownerCreateShortlistController

view_cleaner_bp = Blueprint('view_cleaner', __name__)

@view_cleaner_bp.route('/homeowner_base')
def homeowner_base():
    return render_template('homeowner_base.html')

@view_cleaner_bp.route('/homeowner_base/view_cleaner')
def view_cleaners():
    userid = session.get('userid')
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        cleaners = HomeownerSearchCleanerController.homeownerSearchCleaner(search_query)
    else:
        cleaners = HomeownerViewCleanerController.homeownerViewCleaner()
    return render_template('view_cleaner.html', cleaners=cleaners.values())

@view_cleaner_bp.route('/homeowner_base/add_shortlist', methods=['POST'])
def add_shortlist():
    userid = session.get('userid')
    cleanerid = request.form.get("cleanerid")

    final = HomeownerCreateShortlistController.homeownerCreateShortlist(cleanerid, userid)
    
    if final:
        return redirect(url_for('view_cleaner.view_cleaners', message='Cleaner successfully added to shortlist'))
    else:
        return redirect(url_for('view_cleaner.view_cleaners', message='Cleaner already shortlisted'))

