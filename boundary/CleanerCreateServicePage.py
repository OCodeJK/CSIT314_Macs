from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from control.CleanerCreateServiceController import CleanerCreateServiceController

create_service_bp = Blueprint('create_service', __name__)

class CleanerCreateService:
    def __init__(self):
        self.controller = CleanerCreateServiceController()
    
    def process_service_creation(self, serviceId, cleanerId):
        # Process the service creation request
        result = self.controller.cleanersCreateService(serviceId, cleanerId)
        return result


# Flask routes
@create_service_bp.route('/create-service', methods=['POST'])
def create_service_submit():
    # Get form data
    cleanerId = request.form.get('cleaner_id', current_app.config.get('DEFAULT_CLEANER_ID', '1'))
    serviceId = request.form.get('service_id')
    
    # Validate input
    if not serviceId:
        flash("Invalid Input", "error")
        return redirect(url_for('view_service.view_services'))
    
    # Process creation
    service_page = CleanerCreateService()
    result = service_page.process_service_creation(serviceId, cleanerId)
    
    if result:
        flash("Service added successfully", "success")
    else:
        flash("Service addition failed, please try again.", "error")
    
    return redirect(url_for('view_service.view_services'))