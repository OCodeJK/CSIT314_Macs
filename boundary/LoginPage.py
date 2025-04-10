from flask import Blueprint, request, render_template, request, redirect, url_for
from control.LoginAccountController import LoginAccountController

login_ui = Blueprint("login_ui", __name__)
controller = LoginAccountController()

@login_ui.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if controller.AuthenticateDetails(username, password, role):
            if role == "User Admin":
                return redirect(url_for('register_ui.createUserAccount'))
            elif role == "Cleaner":
                #implement cleaner page here
                print("this is cleaner page")
            elif role == "Homeowner":
                #implement Homeowner page here
                print("this is homeowner")
            elif role == "Platform Management":
                #implement Platform Management page here
                print("this is platform management page")
            else:
                return render_template("login.html", message=f"✅ {username} exists but not for {role}.")
        else:
            return render_template("login.html", message="❌ Invalid credentials or role.")
    
    return render_template("login.html", message=None)