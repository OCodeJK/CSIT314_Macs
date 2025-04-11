from flask import Blueprint, request, render_template, request, redirect, url_for
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
        profilename = request.form["profile_name"]
        
        user = controller.AuthenticateDetails(username, password, profilename)

        if user:
            if user.get_profilename() == "User Admin":
                return redirect(url_for('register_ui.createUserAccount'))
            elif user.get_profilename() == "Cleaner":
                #implement cleaner page here
                print("this is cleaner page")
            elif user.get_profilename() == "Homeowner":
                #implement Homeowner page here
                print("this is homeowner")
            elif user.get_profilename() == "Platform Management":
                #implement Platform Management page here
                print("this is platform management page")
            else:
                return render_template("login.html", message=f"✅ {user.get_username()} exists but not for {user.get_profilename()}.", profiles=profiles)
        else:
            return render_template("login.html", message="❌ Invalid credentials or role.", profiles=profiles)
    
    return render_template("login.html", message=None, profiles=profiles)