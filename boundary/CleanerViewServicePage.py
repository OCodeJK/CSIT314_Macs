from flask import Blueprint, render_template, request, current_app
from control.CleanerViewServiceController import CleanerViewServiceController
from control.CleanerCreateServiceController import CleanerCreateServiceController

view_service_bp = Blueprint('view_service', __name__)

class CleanerViewServicePage:
    def __init__(self):
        self.view_controller = CleanerViewServiceController()
        self.create_controller = CleanerCreateServiceController()

    def getServiceList(self, cleanerId):
        # Get services from controller
        services = self.view_controller.getServiceList(cleanerId)
        return services
    
    def getAvailableServices(self):
        # Get available services that can be added
        available_services = self.create_controller.get_available_services()
        return available_services

    def displayServiceList(self, services):
        # Convert database tuples to dictionaries for template
        service_list = []
        for service in services:
            service_dict = {
                'serviceId': service[0],
                'serviceName': service[1],
                'categoryId': service[2],
                'cleanerId': service[3],
                'price': service[4]
            }
            service_list.append(service_dict)
        return service_list


# Flask routes
@view_service_bp.route('/services', methods=['GET', 'POST'])
def view_services():
    # Get cleaner ID from form or use default
    cleaner_id = request.form.get('cleaner_id', current_app.config.get('DEFAULT_CLEANER_ID', '1'))
    
    # Get services using the boundary class
    service_page = CleanerViewServicePage()
    services = service_page.getServiceList(cleaner_id)
    services_display = service_page.displayServiceList(services)
    
    # Get available services for adding
    available_services = service_page.getAvailableServices()
    available_services_display = service_page.displayServiceList(available_services)
    
    return render_template(
        'service.html', 
        cleaner_id=cleaner_id,
        services=services_display,
        available_services=available_services_display
    )