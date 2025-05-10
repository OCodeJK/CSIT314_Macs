from flask import Blueprint, render_template, request, redirect, url_for, flash
from control.CleanerUpdateServiceController import CleanerUpdateServiceController
from entity.Service import Service
from db_config import db_connection

# Create the blueprint instance
update_service_bp = Blueprint('update_service', __name__)

class CleanerUpdateServicePage:
    
    def __init__(self):
        self.controller = CleanerUpdateServiceController()
    
    def submitUpdateServiceInfo(self, serviceId, serviceName, cleanerId, categoryId):

        self.controller.cleanerUpdateService(serviceId, serviceName, cleanerId, categoryId)


# Flask routes
@update_service_bp.route('/update-service/<service_id>', methods=['GET', 'POST'])
def update_service(service_id):
    cleaner_id = request.args.get('cleaner_id', request.form.get('cleaner_id', '1'))
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get form data
        service_name = request.form.get('service_name', '')
        category_id = request.form.get('category_id', '')
        
        # Initialize page boundary
        page = CleanerUpdateServicePage()
        
        # Call the boundary method (void return)
        page.submitUpdateServiceInfo(service_id, service_name, cleaner_id, category_id)
        
        # Check result from controller directly for flash message
        controller = CleanerUpdateServiceController()
        result = controller.cleanerUpdateService(service_id, service_name, cleaner_id, category_id)
        
        if result:
            flash("Service updated successfully", "success")
        else:
            flash("Failed to update service", "error")
            
        # Redirect to the update service page to view changes
        return redirect(url_for('update_service.update_service', service_id=service_id, cleaner_id=cleaner_id))
    
    # Handle GET request (display form)
    else:
        # Get service details
        service = Service.get_by_id(service_id)
        
        if not service:
            flash("Service not found", "error")
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
        
        # Check if the service belongs to the cleaner
        if service[3] != cleaner_id:
            flash("You don't have permission to update this service", "error")
            return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
        
        # Format service for template
        formatted_service = {
            'serviceId': service[0],
            'serviceName': service[1],
            'categoryId': service[2],
            'cleanerId': service[3],
            'price': service[4]
        }
        

        
        return render_template(
            'update_services.html',
            service=formatted_service,
            cleaner_id=cleaner_id
        )