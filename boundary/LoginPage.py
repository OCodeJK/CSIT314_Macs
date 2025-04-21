from flask import Blueprint, request, render_template, redirect, url_for
from control.LoginAccountController import LoginAccountController
from helper.util_functions import get_all_profiles

login_ui = Blueprint("login_ui", __name__)
controller = LoginAccountController()


@login_ui.route("/", methods=["GET", "POST"])
def Login():
    profiles = get_all_profiles()
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        profileid = request.form["profile_id"]
        
        user = controller.AuthenticateDetails(username, password, profileid)
        
        # ✅ Check for suspension FIRST
        if user == "suspended":
            return render_template("login.html", message="❌ Your account has been suspended.", profiles=profiles)
        
        # Handle string errors returned
        if isinstance(user, str):
            return render_template("login.html", message=f"⚠️ {user}", profiles=profiles)
        
        # If the login happen check role to load appropriate page
        if user:
            if user.get_profileid() == "User Admin":
                #redirect to admin page (create account page for now)
                return redirect(url_for('register_ui.createUserAccount'))
            
            elif user.get_profileid() == "Cleaner":
                #implement cleaner page here
                print("this is cleaner page")
            elif user.get_profileid() == "Homeowner":
                #implement Homeowner page here
                print("this is homeowner")
            elif user.get_profileid() == "Platform Management":
                #implement Platform Management page here
                print("this is platform management page")
            
        else:
            return render_template("login.html", message="❌ Invalid credentials or role.", profiles=profiles)
    
    return render_template("login.html", message=None, profiles=profiles)