from flask import Blueprint, render_template, request
from control.CleanerSearchServiceController import CleanerSearchServiceController
from entity.cleaner import Cleaner
from entity.service import Service   

search_service_bp = Blueprint('search_service', __name__)

class CleanerSearchServicePage:
    
    def __init__(self):
        self.controller = CleanerSearchServiceController()

# Flask routes
@search_service_bp.route('/search-services', methods=['GET'])
def search_services():
    cleaner_id = request.args.get('cleaner_id')
    search_query = request.args.get('search_query', '')

    
    # Initialize boundary and controller
    page = CleanerSearchServicePage()
    
    # Search for services
    results = page.controller.searchCleanerService(cleaner_id, search_query)
    
    # Format the results for display
    formatted_services = []
    for service in results:
        suspended = False
        if len(service) > 5:
            suspended = service[5]
        
        formatted_services.append({
            'serviceId': service[0],
            'serviceName': service[1],
            'categoryId': service[2],
            'cleanerId': service[3],
            'price': service[4],
            'suspended': suspended
        })
    
    # Get cleaner information
    cleaner = Cleaner.get_by_id(cleaner_id)
    
    # Get available services for the "Add Service" section
    available_services = Service.get_available_services()
    formatted_available = []
    for service in available_services:
        formatted_available.append({
            'serviceId': service[0],
            'serviceName': service[1],
            'categoryId': service[2],
            'cleanerId': service[3],
            'price': service[4]
        })
    
    # Use the services.html template instead of search_result.html
    return render_template(
        'services.html',
        cleaner=cleaner,
        services=formatted_services,
        available_services=formatted_available,
        search_query=search_query  # Pass search query to template
    )