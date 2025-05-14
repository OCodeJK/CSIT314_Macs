from flask import Blueprint, render_template, request, redirect, url_for, flash
from control.CleanerCreateServiceController import CleanerCreateServiceController
from helper.util_functions import get_available_services  


create_service_bp = Blueprint('create_service', __name__)

class CleanerCreateService:
    def __init__(self):
        self.controller = CleanerCreateServiceController()

create_sv_page = CleanerCreateService()


@create_service_bp.route('/add-service', methods=['POST'])
def create_service():
    try:
        cleaner_id = request.form.get('cleaner_id')
        service_id = request.form.get('service_id')
        
        result = create_sv_page.controller.cleanerCreateService(service_id, cleaner_id)
        
        if result:
            flash("Service created successfully!", "success")
        else:
            flash("Failed to create service. The service may not be available or is already assigned to a cleaner.", "error")
        
        return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))
    except Exception as e:
        print(f"Error creating service: {e}")
        flash("An error occurred while creating the service", "error")
        return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))

@create_service_bp.route('/available-services/<cleaner_id>', methods=['GET'])
def get_available_services_route(cleaner_id):   
    try:
        available_services = get_available_services()
        
        formatted_available = []
        if available_services:   
            for service in available_services:
                formatted_available.append({
                    'serviceId': service[0],
                    'serviceName': service[1],
                    'categoryId': service[2],
                    'price': service[4] if len(service) > 4 else None,
                })
        
        return render_template(
            'create_service.html',
            cleaner_id=cleaner_id,
            available_services=formatted_available
        )
    except Exception as e:
        print(f"Error getting available services: {e}")
        flash("An error occurred while retrieving available services", "error")
        return redirect(url_for('view_service.view_services', cleaner_id=cleaner_id))