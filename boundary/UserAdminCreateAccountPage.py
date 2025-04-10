from flask import Blueprint, render_template, request
from control.UserAdminCreateAccController import UserAdminCreateAccController
from helper.util_functions import get_all_profiles

# Define a Blueprint to register with the Flask app
register_ui = Blueprint("register_ui", __name__)
controller = UserAdminCreateAccController()


@register_ui.route("/create_user", methods=["GET", "POST"])
def createUserAccount():
    profiles = get_all_profiles()
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        profile_id = request.form["profile_id"]

        result = controller.userCreateAccount(username, password, profile_id)

        if result is True:
            message = "✅ Account created!"
        elif isinstance(result, str):
            message = f"⚠️ {result}"
        else:
            message = "❌ Failed to create account."
            
        
        return render_template("register_account.html", message=message, profiles=profiles)

    #If user visit pages via GET
    return render_template("register_account.html", message=None, profiles=profiles)
