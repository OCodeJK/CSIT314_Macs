from flask import Flask
from boundary.LoginPage import login_ui
from boundary.UserAdminCreateAccountPage import register_ui
from boundary.UserAdminCreateProfilePage import register_profile_ui
from boundary.UserAdminViewAccPage import view_acc
from boundary.UserAdminViewProfilePage import view_prof
from boundary.UserAdminUpdateAccPage import update_user_ui
from boundary.PMCreateServCat import createservcat_bp


app = Flask(__name__)

app.secret_key = 'not-secret'

app.register_blueprint(login_ui)
app.register_blueprint(register_ui)
app.register_blueprint(register_profile_ui)
app.register_blueprint(view_acc)
app.register_blueprint(update_user_ui)
app.register_blueprint(view_prof)
app.register_blueprint(createservcat_bp)


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)