from flask import Blueprint, redirect, url_for, flash, request
from control.PMSuspendServCatController import PMSuspendServCatController

suspend_category_bp = Blueprint('suspend_category', __name__)

@suspend_category_bp.route('/admin/suspend_category/<int:category_id>', methods=['POST'])
def toggle_suspend(category_id):
    # Determine action from form or current state (you may pass as hidden input or infer)
    suspend_action = request.form.get('suspend_action', 'suspend')
    suspend = True if suspend_action == 'suspend' else False

    controller = PMSuspendServCatController()
    result = controller.SuspendServCat(category_id, suspend)
    if result is True:
        flash("Service Category suspended successfully.")
    else:
        flash("Service Category is already suspended.")

    return redirect(url_for('view_category.view_category'))
