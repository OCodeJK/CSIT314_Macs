from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.PMSearchServCatController import PMSearchServCatController
from control.PMViewServCatController import PMViewServCatController

view_category_bp = Blueprint('view_category', __name__)

@view_category_bp.route('/admin/view_category', methods=['GET'])
def view_category():

    search_term = request.args.get('search', '').strip()
    
    if search_term:
        # Use the search controller for searching
        controller = PMSearchServCatController()
        categories = controller.SearchServCat(search_term)
        if categories is None or len(categories) == 0:
            flash(f'No categories found matching "{search_term}".')
    else:
        # Use the view controller for viewing all
        controller = PMViewServCatController()
        categories = controller.SearchServCat()  # Pass empty string to get all categories

    return render_template('view_service_category.html', categories=categories or [], search_term=search_term)
