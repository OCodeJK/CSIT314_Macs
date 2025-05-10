from flask import Blueprint, render_template, request, redirect, url_for, flash
from control.ShortlistCountForCleanerController import ShortlistCountForCleanerController

# Create blueprint
shortlist_bp = Blueprint('shortlist', __name__)

class ShortlistCountForCleanerPage:
    
    def __init__(self):
        self.controller = ShortlistCountForCleanerController()
    
    def view_shortlist_stats(self, cleaner_id, service_id=None):

        # Convert empty string to None
        if service_id == "":
            service_id = None
        
        # Get shortlist count using controller
        shortlist_count = self.controller.getNumberOfShortlistedTime(cleaner_id, service_id)
        
        # Render template with the count
        return render_template(
            'shortlist_count.html',
            cleaner_id=cleaner_id,
            shortlist_count=shortlist_count,
            service_id=service_id
        )


# Flask routes

@shortlist_bp.route('/cleaner/shortlist-stats/<cleaner_id>', methods=['GET'])
def view_shortlist_stats(cleaner_id):
    """View shortlist statistics for a cleaner"""
    page = ShortlistCountForCleanerPage()
    return page.view_shortlist_stats(cleaner_id)

@shortlist_bp.route('/cleaner/shortlist-stats/<cleaner_id>/<service_id>', methods=['GET'])
def view_service_shortlist_stats(cleaner_id, service_id):
    """View shortlist statistics for a specific service"""
    page = ShortlistCountForCleanerPage()
    return page.view_shortlist_stats(cleaner_id, service_id)

@shortlist_bp.route('/cleaner/shortlist-count', methods=['GET'])
def view_shortlist_count():
    """View shortlist statistics using query parameters"""
    cleaner_id = request.args.get('cleaner_id')
    service_id = request.args.get('service_id')
    
    if not cleaner_id:
        flash("Missing cleaner ID", "error")
        return redirect(url_for('view_service.index'))
    
    page = ShortlistCountForCleanerPage()
    return page.view_shortlist_stats(cleaner_id, service_id)