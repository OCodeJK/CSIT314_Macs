from flask import Blueprint, render_template, request, redirect, url_for, flash
from control.CleanerUpdateServiceController import CleanerUpdateServiceController

# Create the blueprint instance
update_service_bp = Blueprint('update_service', __name__)

class CleanerUpdateServicePage:
   """Boundary class for handling service update operations"""
   
   def __init__(self):
       """Initialize with controller """
       self.controller = CleanerUpdateServiceController()


update_page = CleanerUpdateServicePage()

# Flask routes
@update_service_bp.route('/update-service/<service_id>', methods=['GET', 'POST'])
def update_service(service_id):
    """Handle service update requests"""
    cleaner_id = request.args.get('cleaner_id', request.form.get('cleaner_id', '1'))
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get form data
        service_name = request.form.get('service_name', '')
        category_id = request.form.get('category_id', '')
        
        # Validate category ID first
        if not update_page.controller.validateCategoryId(category_id):
            flash(f"Category ID '{category_id}' does not exist in the database", "error")
            # Get current service details to redisplay the form
            service = update_page.controller.getServiceDetails(service_id, cleaner_id)
            if not service:
                flash("Service not found or you don't have permission to update it", "error")
                return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
                
            return render_template(
                'update_services.html',
                service=service,
                cleaner_id=cleaner_id
            )
        
        # Call the controller to update service
        result = update_page.controller.cleanerUpdateService(service_id, service_name, cleaner_id, category_id)
        
        if result:
            flash("Service updated successfully", "success")
        else:
            flash("Failed to update service", "error")
        
        # Redirect to the update service page to view changes
        return redirect(url_for('update_service.update_service', service_id=service_id, cleaner_id=cleaner_id))
    
    # Handle GET request (display form)
    else:
        # Get service details from controller
        service = update_page.controller.getServiceDetails(service_id, cleaner_id)
        
        if not service:
            flash("Service not found or you don't have permission to update it", "error")
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
        
        # Render template with service details
        return render_template(
            'update_services.html',
            service=service,
            cleaner_id=cleaner_id
        )