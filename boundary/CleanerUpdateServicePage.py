from flask import Blueprint, render_template, request, redirect, url_for, flash
from control.CleanerUpdateServiceController import CleanerUpdateServiceController
from helper.util_functions import getServiceWithDetails

# Create the blueprint instance
update_service_bp = Blueprint('update_service', __name__)

class CleanerUpdateServicePage:
    
    def __init__(self):
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
        service_name = request.form.get('service_name', '').strip()
        category_id = request.form.get('category_id', '')
        
        # Process update through controller
        result = update_page.controller.cleanerUpdateService(
            serviceId=service_id,
            serviceName=service_name,
            cleanerId=cleaner_id,
            categoryId=category_id
        )
        
        # Handle controller response
        if result:
            flash("Service updated successfully", "success")
        else:
            flash("Failed to update service. Please check your input.", "error")
        
        return redirect(url_for('update_service.update_service', service_id=service_id, cleaner_id=cleaner_id))
    
    # Handle GET request (display form)
    else:
        service = getServiceWithDetails(service_id, cleaner_id)
        
        if service:

            return render_template(
                'update_services.html',
                service=service,
                cleaner_id=cleaner_id
            )
        else:
            flash("Service not found or you don't have permission to update it", "error")
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))