from flask import Blueprint, render_template
from control.UserAdminViewProfController import UserAdminViewProfController

view_prof = Blueprint("view_prof", __name__)

@view_prof.route("/admin/view_profiles")
def display_profiles():
    profiles = UserAdminViewProfController.UserAdminViewProf()
    return render_template("view_profile.html", profiles=profiles)
