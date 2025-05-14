from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from control.CleanerViewServiceController import CleanerViewServiceController
from control.ServiceViewsController import ServiceViewsController
from control.ShortlistCountForCleanerController import ShortlistCountForCleanerController

# Create blueprint
view_service_bp = Blueprint('view_service', __name__)

class CleanerViewServicePage:
    def __init__(self):
        """Initialize with controllers for business logic"""
        self.controller = CleanerViewServiceController()
        self.views_controller = ServiceViewsController()
        self.shortlist_controller = ShortlistCountForCleanerController()

# Define the route with the same function name as used in url_for
@view_service_bp.route('/services/<cleaner_id>')
def view_services(cleaner_id):
    # Create controller instances
    view_controller = CleanerViewServiceController()
    views_controller = ServiceViewsController()
    shortlist_controller = ShortlistCountForCleanerController()
    
    # Get data from controllers
    db_services = view_controller.getServiceList(cleaner_id)
    
    # Format services for the template
    formatted_services = []
    
    # Initialize view and shortlist count dictionaries
    service_views = {}
    shortlist_counts = {}
    
    if db_services:
        for service in db_services:
            # Format service data
            service_id = service[0]
            formatted_service = {
                'serviceId': service_id,
                'serviceName': service[1],
                'categoryId': service[2],
                'cleanerId': service[3],
                'price': service[4],
                'suspended': service[5] if len(service) > 5 else False
            }
            formatted_services.append(formatted_service)
            
            # Get view count for this service
            service_views[service_id] = views_controller.getTotalViews(cleaner_id, service_id)
            
            # Get shortlist count for this service
            shortlist_counts[service_id] = shortlist_controller.getNumberOfShortlistedTime(cleaner_id, service_id)
            print(f"Service {service_id} - Shortlist count: {shortlist_counts[service_id]}")
    
    # Get cleaner object
    cleaner = {"cleanerId": cleaner_id}
    
    # Return the rendered template
    return render_template(
        "services.html",
        services=formatted_services,
        search_query=None,
        cleaner_id=cleaner_id,
        cleaner=cleaner,
        service_views=service_views,
        shortlist_counts=shortlist_counts
    )

@view_service_bp.route('/')
def index():
    # Render the index.html template (home page)
    return render_template('index.html')