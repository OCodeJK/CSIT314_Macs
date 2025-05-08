from flask import Blueprint, render_template, request, redirect, url_for
from control.UserAdminCreateAccController import UserAdminCreateAccController

# Define a Blueprint to register with the Flask app
register_ui = Blueprint("register_ui", __name__)
controller = UserAdminCreateAccController()


@register_ui.route("/admin/create_user", methods=["GET", "POST"])
def createUserAccount():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        profile_id = request.form["profile_id"]


        result = controller.userCreateAccount(username, password, profile_id)

        if result is True:
            return redirect(url_for('view_acc.display_all_users', message="✅ Account created."))
        elif isinstance(result, str):
            return redirect(url_for('view_acc.display_all_users', message=f"⚠️ {result}"))
        else:
            return redirect(url_for('view_acc.display_all_users', message="❌ Account creation failed."))
            

    #If user visit pages via GET
    return redirect(url_for('view_acc.display_all_users'))
