from flask import Blueprint, render_template, request, redirect, url_for
from control.UserAdminViewAccController import UserAdminViewAccController
from control.UserAdminSearchAccController import UserAdminSearchAccController
from control.UserAdminSuspendAccController import UserAdminSuspendAccController
from helper.util_functions import get_all_profiles

view_acc = Blueprint('view_acc', __name__)

@view_acc.route('/admin/view_accounts')
def display_all_users():
    
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        users = UserAdminSearchAccController.searchUserAccount(search_query)
    else:
        users = UserAdminViewAccController.userAdminViewAcc()
    
    profiles = get_all_profiles()
    return render_template('view_account.html', users=users, profiles=profiles)

@view_acc.route("/admin/suspend_user/<int:userid>", methods=["POST"])
def SuspendUser(userid):
    result = UserAdminSuspendAccController.userAdminSuspendAcc(userid)
    print("Suspend result:", result)
    
    if result is True:
        return redirect(url_for("view_acc.display_all_users", message="User suspended successfully"))
    else:
        return redirect(url_for("view_acc.display_all_users", message="Suspension failed: User already suspended.."))

