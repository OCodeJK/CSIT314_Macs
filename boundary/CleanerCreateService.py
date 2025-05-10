from flask import Blueprint, render_template, request, redirect, url_for, flash
from control.CleanerCreateServiceController import CleanerCreateServiceController

create_service_bp = Blueprint('create_service', __name__)

class CleanerCreateService:
    
    def __init__(self):
        self.controller = CleanerCreateServiceController()
    
    def cleanerCreateService(self):
        pass


@create_service_bp.route('/add-service', methods=['POST'])
def add_service():
    """Route to add a service to a cleaner"""
    try:
        # Get form data
        cleaner_id = request.form.get('cleaner_id')
        service_id = request.form.get('service_id')
        
        # Initialize the controller directly
        controller = CleanerCreateServiceController()
        
        # Use the controller to perform the actual operation
        result = controller.cleanerCreateService(service_id, cleaner_id)
        
        if result:
            flash("Service added successfully!", "success")
        else:
            flash("Failed to add service. The service may not be available or is already assigned to a cleaner.", "error")
        
        return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
    except Exception as e:
        print(f"Error adding service: {e}")
        flash("An error occurred while adding the service", "error")
        return redirect(url_for('view_service.index'))