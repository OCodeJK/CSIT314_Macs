from flask import Blueprint, request, redirect, url_for
from control.UserAdminCreateProfileController import UserAdminProfileController

#Define a blueprint for flask
register_profile_ui = Blueprint("register_profile_ui", __name__)
controller = UserAdminProfileController()

@register_profile_ui.route("/admin/create_profile", methods=["GET", "POST"])
def createUserProfile():
    if request.method == "POST":
        profilename = request.form["profile_name"]
        
        result = controller.createUserProfileController(profilename)
    
        if result is True:
            return redirect(url_for('view_prof.display_profiles', message="✅ Profile created."))
        elif isinstance(result, str):
            return redirect(url_for('view_prof.display_profiles', message=f"⚠️ {result}"))
        else:
            return redirect(url_for('view_prof.display_profiles', message="❌ Create not successful, please try again."))
    
    return redirect(url_for('view_prof.display_profiles'))