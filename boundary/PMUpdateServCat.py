from flask import Blueprint, render_template, request, flash, redirect, url_for
from control.PMUpdateServCatController import PMUpdateServCatController
from helper.util_functions import GetCategoryById

update_category_bp = Blueprint('update_category', __name__)

@update_category_bp.route('/admin/update_category/<int:category_id>', methods=['GET', 'POST'])
def update_category_form(category_id):
    controller = PMUpdateServCatController()

    if request.method == 'POST':
        new_name = request.form.get('category_name', '').strip()
        result = controller.UpdateServCat(category_id, new_name)
        if result is True:
            flash("Service Category updated successfully.")
            return redirect(url_for('view_category.view_category'))
        elif result == "duplicate":
            flash("Failed to update: Name already exists.")
        elif result is False or result is None:
            flash("Failed to update: Invalid name or error.")
        else:
            flash("Failed to update service category.")

    # Optionally fetch current category name for display
    current_category = GetCategoryById(category_id)
    return render_template('update_service_category.html', category=current_category)
