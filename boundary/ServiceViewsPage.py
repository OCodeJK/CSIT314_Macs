from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from control.ServiceViewsController import ServiceViewsController

service_views_bp = Blueprint('service_views', __name__)

class ServiceViewsPage:
    """Boundary class for service views functionality"""
    
    def __init__(self):
        self.controller = ServiceViewsController()
    
    def get_service_views(self, cleanerId, serviceId=None):

        return self.controller.getTotalViews(cleanerId, serviceId)
    
    def increment_view(self, serviceId):

        return self.controller.incrementViewCount(serviceId)


# Flask routes
@service_views_bp.route('/service/<serviceId>/views', methods=['GET'])
def get_service_views(serviceId):
    """Route to get view count for a specific service"""
    cleaner_id = request.args.get('cleaner_id', current_app.config.get('DEFAULT_CLEANER_ID', '1'))
    
    # Get view count
    service_page = ServiceViewsPage()
    view_count = service_page.get_service_views(cleaner_id, serviceId)
    
    # Sử dụng template đã tồn tại - service_view.html thay vì service_view_count.html
    return render_template(
        'service_view.html',
        cleaner_id=cleaner_id,
        service_id=serviceId,
        view_count=view_count
    )

@service_views_bp.route('/cleaner/total-views', methods=['GET'])
def get_total_views():
    """Route to get total views for a cleaner"""
    cleaner_id = request.args.get('cleaner_id', current_app.config.get('DEFAULT_CLEANER_ID', '1'))
    
    # Get total view count
    service_page = ServiceViewsPage()
    total_views = service_page.get_service_views(cleaner_id)
    
    # Render template
    return render_template(
        'total_views.html',
        cleaner_id=cleaner_id,
        total_views=total_views
    )

@service_views_bp.route('/service/<serviceId>/view', methods=['GET', 'POST'])
def increment_service_view(serviceId):
    """Route to increment view count for a service"""
    # Increment view count
    service_page = ServiceViewsPage()
    success = service_page.increment_view(serviceId)
    
    if success:
        flash("View count incremented successfully", "success")
    else:
        flash("Failed to increment view count", "error")
    
    # Redirect back to the referrer page
    return redirect(request.referrer or url_for('view_service.index'))