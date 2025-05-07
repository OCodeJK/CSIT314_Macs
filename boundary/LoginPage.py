from flask import Blueprint, request, render_template, redirect, url_for, session
from control.LoginAccountController import LoginAccountController
from helper.util_functions import get_all_profiles, userReturnUID

login_ui = Blueprint("login_ui", __name__)
controller = LoginAccountController()


@login_ui.route("/", methods=["GET", "POST"])
def Login():
    profiles = get_all_profiles()
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        profileid = request.form["profile_id"]
        userid = 0
        
        user = controller.AuthenticateDetails(username, password, profileid)
        userid = userReturnUID(username, password, profileid)

        # ✅ Check for suspension FIRST
        if user == "suspended":
            return render_template("login.html", message="❌ Your account has been suspended.", profiles=profiles)
        if user == "profile_suspended":
            return render_template("login.html", message="❌ The profile has been suspended.", profiles=profiles)
        
        # Handle string errors returned
        if isinstance(user, str):
            return render_template("login.html", message=f"⚠️ {user}", profiles=profiles)
        
        # If the login happen check role to load appropriate page
        if user:
            session['userid'] = userid
            if user.get_profileid() == "User Admin":
                #redirect to admin page (create account page for now)
                return redirect(url_for('view_acc.display_all_users'))
            
            elif user.get_profileid() == "Cleaner":
                #implement cleaner page here
                print("This is cleaner page")
            elif user.get_profileid() == "Homeowner":
                #implement Homeowner page here
                return redirect(url_for('view_cleaner.homeowner_base'))
            elif user.get_profileid() == "Platform Management":
                #implement Platform Management page here
                print("this is platform management page")
            
        else:
            return render_template("login.html", message="❌ Invalid credentials or role.", profiles=profiles)
    
    return render_template("login.html", message=None, profiles=profiles)