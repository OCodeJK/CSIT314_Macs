from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.PMSearchServCatController import PMSearchServCatController

view_category_bp = Blueprint('view_category', __name__)

def is_platform_management():
    return session.get('profileid') == "Platform Management"

@view_category_bp.route('/admin/view_category', methods=['GET'])
def view_category():
    if not is_platform_management():
        flash("Unauthorized: Only Platform Management can access this page.")
        return redirect(url_for('login_ui.Login'))

    search_term = request.args.get('search', '').strip()
    controller = PMSearchServCatController()
    categories = controller.SearchServCat(search_term)

    if search_term and (categories is None or len(categories) == 0):
        flash(f'No categories found matching \"{search_term}\".')

    return render_template('view_service_category.html', categories=categories or [], search_term=search_term)
