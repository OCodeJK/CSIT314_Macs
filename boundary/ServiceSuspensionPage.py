from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from control.CleanerSuspendServiceController import ServiceSuspensionController

suspend_service_bp = Blueprint('suspend_service', __name__)

class ServiceSuspensionPage:
    def __init__(self):
        self.controller = ServiceSuspensionController()
    
    def suspend_service(self, cleanerId, serviceId):
        # Process the service suspension request
        result = self.controller.suspendService(cleanerId, serviceId)
        return result


# Flask routes
@suspend_service_bp.route('/suspend-service/<serviceId>', methods=['POST'])
def suspend_service_submit(serviceId):
    # Use default cleaner ID
    cleanerId = current_app.config.get('DEFAULT_CLEANER_ID', '1')
    
    # Process suspension
    suspension_page = ServiceSuspensionPage()
    result = suspension_page.suspend_service(cleanerId, serviceId)
    
    if result:
        flash("Service suspended successfully", "success")
    else:
        flash("Suspension failed; Service is already suspended.", "error")
    
    return redirect(url_for('view_service.view_services'))