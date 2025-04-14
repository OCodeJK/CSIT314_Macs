from flask import Blueprint, render_template
from control.UserAdminViewAccController import UserAdminViewAccController

view_acc = Blueprint('view_acc', __name__)

@view_acc.route('/admin/view_accounts')
def display_all_users():
    users = UserAdminViewAccController.UserAdminViewAcc()
    return render_template('view_account.html', users=users)