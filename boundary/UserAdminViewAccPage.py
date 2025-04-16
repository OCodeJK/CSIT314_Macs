from flask import Blueprint, render_template, request
from control.UserAdminViewAccController import UserAdminViewAccController
from control.UserAdminSearchAccController import UserAdminSearchAccController

view_acc = Blueprint('view_acc', __name__)

@view_acc.route('/admin/view_accounts')
def display_all_users():
    
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        users = UserAdminSearchAccController.SearchUserAccount(search_query)
    else:
        users = UserAdminViewAccController.UserAdminViewAcc()
    
    return render_template('view_account.html', users=users)