from flask import Blueprint, render_template, request
from control.UserAdminCreateProfileController import UserAdminProfileController

#Define a blueprint for flask
register_profile_ui = Blueprint("register_profile_ui", __name__)
controller = UserAdminProfileController()

@register_profile_ui.route("/admin/create_profile", methods=["GET", "POST"])
def createUserProfile():
    if request.method == "POST":
        profile_name = request.form["profile_name"]
        
        result = controller.createUserProfileController(profile_name)
        
        if result is True:
            message = "✅ Profile created successfully!"
        elif isinstance(result, str):
            message = f"⚠️ {result}"
        else:
            message = "❌ Could not create profile." + profile_name
            
        return render_template("register_profile.html", message=message)
    
    return render_template("register_profile.html", message=None)