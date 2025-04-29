from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from control.PMCreateServCatController import PMCreateServCatController

createservcat_bp = Blueprint('createservcat', __name__)

def is_platform_management():
    return session.get('profileid') == "Platform Management"

@createservcat_bp.route('/platformmanagement/create_service_category', methods=['GET', 'POST'])
def create_service_category():
    if not is_platform_management():
        flash("Unauthorized: Only Platform Management can access this page.")
        return redirect(url_for('login_ui.Login'))

    controller = PMCreateServCatController()

    if request.method == 'POST':
        category_name = request.form.get('category_name', '').strip()
        result = controller.CreateServCat(category_name)
        flash(result)
        if result == "Service category created":
            return redirect(url_for('createservcat.create_service_category'))

    return render_template('create_service_category.html')


