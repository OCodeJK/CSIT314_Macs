from flask import Blueprint, request, render_template, redirect
from control.UserAdminUpdateProfController import UserAdminUpdateProfController
from helper.util_functions import get_profile_by_id

update_profile_ui = Blueprint("update_profile_ui", __name__)
controller = UserAdminUpdateProfController()

@update_profile_ui.route("/admin/update_profile/<int:profileid>", methods=["GET"])
def update_profile_form(profileid):
    profile = get_profile_by_id(profileid)  # check helper function
    if not profile:
        return "Profile not found", 404
    return render_template("update_profile.html", profile=profile)


@update_profile_ui.route("/admin/update_profile/<int:profileid>", methods=["POST"])
def submitUpdateProfInfo(profileid):
    profilename = request.form["profilename"]
    
    if not profilename:
        current_profile = get_profile_by_id(profileid)
        if current_profile:
            profilename = current_profile[1] # default profilename
        else:
            return render_template("update_profile.html", profile=[profileid, profilename], message="Something went wrong...")
    
    success = controller.userAdminUpdateProf(profileid, profilename)
    
    if success:
        return redirect("/admin/view_profiles?message=✅+Profile+details+updated+successfully.")
    else:
        return redirect("/admin/view_profiles?message=❌+Failed+to+update+profile+details.")