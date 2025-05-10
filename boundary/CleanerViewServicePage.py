from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from control.CleanerViewServiceController import CleanerViewServiceController
from control.ServiceViewsController import ServiceViewsController
from control.ShortlistCountForCleanerController import ShortlistCountForCleanerController
from entity.Service import Service
from helper.util_functions import get_profile_by_id

# Create blueprint
view_service_bp = Blueprint('view_service', __name__)

class CleanerViewServicePage:
    """Boundary class for handling cleaner service view UI operations"""
    
    def __init__(self):
        self.controller = CleanerViewServiceController()
        self.views_controller = ServiceViewsController()
        self.shortlist_controller = ShortlistCountForCleanerController()
    
    def displayServiceList(self, cleaner_id):
        # Initialize controllers
        service_controller = CleanerViewServiceController()
        views_controller = ServiceViewsController()
        shortlist_controller = ShortlistCountForCleanerController()
        
        # Get services for the cleaner
        db_services = service_controller.getServiceList(cleaner_id)
        
        # Format services for the template
        formatted_services = []
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
        
        # Get available services
        available_services = Service.get_available_services()
        
        # Format available services
        formatted_available = []
        if available_services:
            for service in available_services:
                formatted_available.append({
                    'serviceId': service[0],
                    'serviceName': service[1],
                    'categoryId': service[2],
                    'price': service[4] if len(service) > 4 else None,
                })
        
        # Get cleaner object
        cleaner = {"cleanerId": cleaner_id}
        
        # Render the template
        return render_template(
            "services.html",
            services=formatted_services,
            search_query=None,
            available_services=formatted_available,
            cleaner_id=cleaner_id,
            cleaner=cleaner,
            service_views=service_views,
            shortlist_counts=shortlist_counts
        )

@view_service_bp.route('/')
def index():
    """Home page route"""
    # If user is logged in and is a cleaner, redirect to services page
    if 'user_id' in session:
        profile = get_profile_by_id(session.get('profile_id'))
        if profile and profile[1] == "Cleaner":
            cleaner_id = session.get('user_id')
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
        # Redirect other user types to appropriate pages
        elif profile and profile[1] in ["User Admin", "Platform Management"]:
            return redirect(url_for('register_ui.createUserAccount'))
    
    # Otherwise, redirect to login page
    return redirect(url_for('login_ui.Login'))

@view_service_bp.route('/services/<cleaner_id>')
def view_services(cleaner_id):
    """View all services for a cleaner"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please log in to view services", "error")
        return redirect(url_for('login_ui.Login'))
    
    # Check if user is a cleaner
    profile = get_profile_by_id(session.get('profile_id'))
    if not profile or profile[1] != "Cleaner":
        flash("Only cleaners can access this page", "error")
        return redirect(url_for('login_ui.Login'))
    
    # Check if the logged-in cleaner is trying to access their own services
    if str(session.get('user_id')) != str(cleaner_id):
        flash("You can only view your own services", "error")
        return redirect(url_for('view_service.view_services', cleaner_id=session.get('user_id')))
    