from flask import Blueprint, render_template, request, redirect, url_for
from control.UserAdminViewProfController import UserAdminViewProfController
from control.UserAdminSearchProfController import UserAdminSearchProfController
from control.UserAdminSuspendProfController import UserAdminSuspendProfController

view_prof = Blueprint("view_prof", __name__)

@view_prof.route("/admin/view_profiles")
def display_profiles():
    
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        profiles = UserAdminSearchProfController.SearchUserProfile(search_query)
    else:
        profiles = UserAdminViewProfController.userAdminViewProf()
        
    return render_template("view_profile.html", profiles=profiles)


@view_prof.route("/admin/suspend_profile/<int:profileid>", methods=["POST"])
def SuspendProfile(profileid):
    result = UserAdminSuspendProfController.userAdminSuspendProf(profileid)
    print("Suspend result:", result)
    
    if result is True:
        return redirect(url_for("view_prof.display_profiles", message="✅ Profile suspended successfully"))
    else:
        return redirect(url_for("view_prof.display_profiles", message="❌ Suspension failed: Profile already suspended.."))
