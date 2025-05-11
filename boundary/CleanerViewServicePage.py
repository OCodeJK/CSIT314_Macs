from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from control.CleanerViewServiceController import CleanerViewServiceController
from helper.util_functions import get_profile_by_id

# Create blueprint
view_service_bp = Blueprint('view_service', __name__)

class CleanerViewServicePage:
   """Boundary class for handling cleaner service view UI operations"""
   
   def __init__(self):
       """Initialize with controllers for business logic"""
       self.controller = CleanerViewServiceController()
   
   def displayServiceList(self, cleaner_id):
       # Get services for the cleaner
       db_services = self.controller.getServiceList(cleaner_id)
       
       # Get available services
       available_services = self.controller.getAvailableServices()
       
       # Format services for the template
       formatted_services = []
       
       if db_services:
           for service in db_services:
               # Format service data
               service_id = service[0]
               formatted_service = {
                   'serviceId': service_id,
                   'serviceName': service[1],
                   'categoryId': service[2],
                   'cleanerId': service[3],
                   'price': service[4],
                   'suspended': service[5] if len(service) > 5 else False
               }
               formatted_services.append(formatted_service)
       
       # Format available services
       formatted_available = []
       if available_services:
           for service in available_services:
               formatted_available.append({
                   'serviceId': service[0],
                   'serviceName': service[1],
                   'categoryId': service[2],
                   'price': service[4] if len(service) > 4 else None,
               })
       
       # Get cleaner object
       cleaner = {"cleanerId": cleaner_id}
       
       return render_template(
           "services.html",
           services=formatted_services,
           search_query=None,
           available_services=formatted_available,
           cleaner_id=cleaner_id,
           cleaner=cleaner,
           service_views={},
           shortlist_counts={}
       )

@view_service_bp.route('/services/<cleaner_id>')
def view_services(cleaner_id):
   # Create page instance and display services
   page = CleanerViewServicePage()
   return page.displayServiceList(cleaner_id)