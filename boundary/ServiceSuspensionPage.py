from flask import Blueprint, request, redirect, url_for, flash
from control.ServiceSuspensionController import ServiceSuspensionController

# Create the blueprint
suspend_service_bp = Blueprint('suspend_service', __name__, url_prefix='/suspend-service')

class ServiceSuspensionPage:
    
    def __init__(self):
        """Initialize with controller"""
        self.controller = ServiceSuspensionController()
suspend_page = ServiceSuspensionPage()


# Flask routes
@suspend_service_bp.route('/<serviceId>', methods=['POST'])
def suspend_service_submit(serviceId):

    cleaner_id = request.form.get('cleaner_id', request.args.get('cleaner_id'))
    # Initialize controller directly
    
    # Process suspension via controller
    result = suspend_page.controller.suspendService(cleaner_id, serviceId)
    
    # Handle result
    if result:
        flash(f"Service has been suspended", "success")
    else:
        flash("Failed to suspend service. Service may already be suspended.", "error")
    
    # Redirect back to the services page
    return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))