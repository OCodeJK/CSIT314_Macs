from flask import Flask
from boundary.LoginPage import login_ui
from boundary.UserAdminCreateAccountPage import register_ui
from boundary.UserAdminCreateProfilePage import register_profile_ui
from boundary.UserAdminViewAccPage import view_acc
from boundary.UserAdminViewProfilePage import view_prof
from boundary.UserAdminUpdateAccPage import update_user_ui
from boundary.UserAdminUpdateProfPage import update_profile_ui
from boundary.CleanerViewServicePage import view_service_bp
from boundary.CleanerCreateServicePage import create_service_bp
from boundary.ServiceSuspensionPage import suspend_service_bp
from boundary.HomeownerViewCleanerPage import view_cleaner_bp
from boundary.HomeownerViewShortlistPage import view_shortlist_bp
from boundary.HomeownerViewCompletedServicePage import view_completedservice_bp
import secret # for access secret key -- SESSION



app = Flask(__name__)
app.register_blueprint(login_ui)
app.register_blueprint(register_ui)
app.register_blueprint(register_profile_ui)
app.register_blueprint(view_acc)
app.register_blueprint(update_user_ui)
app.register_blueprint(view_prof)
app.register_blueprint(update_profile_ui)
app.register_blueprint(view_service_bp)
app.register_blueprint(create_service_bp)
app.register_blueprint(suspend_service_bp)
app.register_blueprint(view_cleaner_bp)
app.register_blueprint(view_shortlist_bp)
app.register_blueprint(view_completedservice_bp)
app.secret_key = secret.SECRET_KEY # SESSION RELATED

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)