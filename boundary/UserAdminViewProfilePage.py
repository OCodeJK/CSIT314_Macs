from flask import Blueprint, render_template, request
from control.UserAdminViewProfController import UserAdminViewProfController
from control.UserAdminSearchProfController import UserAdminSearchProfController

view_prof = Blueprint("view_prof", __name__)

@view_prof.route("/admin/view_profiles")
def display_profiles():
    
    search_query = request.args.get('search', '') #get the search input from the URL
    
    if search_query:
        profiles = UserAdminSearchProfController.SearchUserProfile(search_query)
    else:
        profiles = UserAdminViewProfController.userAdminViewProf()
        
    return render_template("view_profile.html", profiles=profiles)
