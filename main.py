from flask import Flask
from boundary.LoginPage import login_ui
from boundary.UserAdminCreateAccountPage import register_ui
from boundary.UserAdminCreateProfilePage import register_profile_ui


app = Flask(__name__)
app.register_blueprint(login_ui)
app.register_blueprint(register_ui)
app.register_blueprint(register_profile_ui)


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)