from flask import Blueprint, render_template, request
from control.ShortlistCountForCleanerController import ShortlistCountForCleanerController

# Create blueprint
shortlist_bp = Blueprint('shortlist', __name__)

class ShortlistCountForCleanerPage:
   def __init__(self):
       self.controller = ShortlistCountForCleanerController()

# Flask routes
@shortlist_bp.route('/cleaner/shortlist-stats/<cleaner_id>', methods=['GET'])
@shortlist_bp.route('/cleaner/shortlist-stats/<cleaner_id>/<service_id>', methods=['GET'])
def view_shortlist_stats(cleaner_id, service_id=None):
   """View shortlist statistics for a cleaner or specific service"""
   controller = ShortlistCountForCleanerController()
   shortlist_count = controller.getNumberOfShortlistedTime(cleaner_id, service_id)
   
   return render_template(
       'shortlist_count.html',
       cleaner_id=cleaner_id,
       shortlist_count=shortlist_count,
       service_id=service_id
   )

@shortlist_bp.route('/cleaner/shortlist-count', methods=['GET'])
def view_shortlist_count():
   """View shortlist statistics using query parameters"""
   cleaner_id = request.args.get('cleaner_id')
   service_id = request.args.get('service_id', None)
   
   controller = ShortlistCountForCleanerController()
   shortlist_count = controller.getNumberOfShortlistedTime(cleaner_id, service_id)
   
   return render_template(
       'shortlist_count.html',
       cleaner_id=cleaner_id,
       shortlist_count=shortlist_count,
       service_id=service_id
   )