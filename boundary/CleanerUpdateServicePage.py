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
    # Get cleaner_id from query params or form
    cleaner_id = request.args.get('cleaner_id') or request.form.get('cleaner_id')
    
    # Validate cleaner_id
    if not cleaner_id or cleaner_id.strip() == '':
        flash("Invalid cleaner ID", "error")
        return redirect(url_for('login_ui.Login'))
    
    try:
        cleaner_id = int(cleaner_id)
    except ValueError:
        flash("Invalid cleaner ID", "error")
        return redirect(url_for('login_ui.Login'))
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get form data
        service_name = request.form.get('service_name', '').strip()
        category_id = request.form.get('category_id', '')
        
        # Validate inputs
        if not service_name:
            flash("Service name is required", "error")
            return redirect(url_for('update_service.update_service', service_id=service_id, cleaner_id=cleaner_id))
        
        if not category_id:
            flash("Category ID is required", "error")
            return redirect(url_for('update_service.update_service', service_id=service_id, cleaner_id=cleaner_id))
        
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
        
        return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
    
    # Handle GET request (display form)
    else:
        service = getServiceWithDetails(service_id)
        
        if not service:
            flash("Service not found", "error")
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
        
        # Verify that cleaner owns this service
        if service.get('cleanerId') != cleaner_id:
            flash("You don't have permission to update this service", "error")
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
        
        return render_template(
            'update_services.html',
            service=service,
            cleaner_id=cleaner_id
        )