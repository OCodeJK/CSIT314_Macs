from flask import Blueprint, render_template, request
from control.CleanerSearchServiceController import CleanerSearchServiceController
from helper.util_functions import get_by_id


search_service_bp = Blueprint('search_service', __name__)

class CleanerSearchServicePage:
    def __init__(self):
        self.controller = CleanerSearchServiceController()

page = CleanerSearchServicePage()

@search_service_bp.route('/search-services', methods=['GET'])
def search_services():
    cleaner_id = request.args.get('cleaner_id')
    search_query = request.args.get('search_query', '')
    
    cleaner = get_by_id(cleaner_id)
    
    results = page.controller.searchCleanerService(cleaner_id, search_query)
    
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
    
    return render_template(
        'services.html',
        cleaner=cleaner,
        services=formatted_services,
        search_query=search_query
    )