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
        flash("Category suspension updated successfully.")
    elif result == "already_suspended":
        flash("Category is already suspended.")
    elif result is False or result is None:
        flash("Failed to update category suspension.")
    else:
        flash("Unknown result from suspension operation.")

    return redirect(url_for('view_category.view_category'))
