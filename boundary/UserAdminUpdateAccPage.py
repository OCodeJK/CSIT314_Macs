from flask import Blueprint, request, render_template, redirect
from control.UserAdminUpdateAccController import UserAdminUpdateAccController
from helper.util_functions import get_user_by_id

update_user_ui = Blueprint("update_user_ui", __name__)
controller = UserAdminUpdateAccController()

@update_user_ui.route("/admin/update_user/<int:userid>", methods=["GET"])
def update_user_form(userid):
    user = get_user_by_id(userid)  # check helper function
    if not user:
        return "User not found", 404
    return render_template("update_account.html", user=user)

@update_user_ui.route("/admin/update_user/<int:userid>", methods=["POST"])
def submitUpdateUserInfo(userid):
    username = request.form["username"]
    password = request.form["password"]
    profileid = request.form["profileid"]
    
    success = controller.UserAdminUpdateAcc(userid, username, password, profileid)
    
    if success:
        return redirect("/admin/view_accounts")
    else:
        return render_template("update_account.html", user=[userid, username, None, profileid],
                               message = "❌ Failed to update user.")
    
