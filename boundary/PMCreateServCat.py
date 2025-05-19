from flask import Blueprint, request, flash, redirect, url_for
from control.PMCreateServCatController import PMCreateServCatController

createservcat_bp = Blueprint('createservcat', __name__)

@createservcat_bp.route('/platformmanagement/create_service_category', methods=['POST'])  # Remove GET
def create_service_category():
    controller = PMCreateServCatController()
    category_name = request.form.get('category_name', '').strip()
    
    # Process creation
    result = controller.CreateServCat(category_name)
    if result is True:
        flash("Service category created successfully")
    else:
        flash("Failed to create service category. Service category already exists.")

    # Always redirect back to view categories page
    return redirect(url_for('view_category.view_category'))
