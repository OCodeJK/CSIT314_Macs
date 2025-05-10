from flask import Flask
from boundary.LoginPage import login_ui
from boundary.UserAdminCreateAccountPage import register_ui
from boundary.UserAdminCreateProfilePage import register_profile_ui
from boundary.UserAdminViewAccPage import view_acc
from boundary.UserAdminViewProfilePage import view_prof
from boundary.UserAdminUpdateAccPage import update_user_ui
from boundary.UserAdminUpdateProfPage import update_profile_ui
# from boundary.HomeownerViewServicePage import view_hoservice_bp #homeowner
# from boundary.HomeownerViewShortlistPage import view_hoshortlist_bp #homeowner
from boundary.HomeownerViewCompletedServicePage import view_completedservice_bp #homeowner
from boundary.PMCreateServCat import createservcat_bp
from boundary.PMManageServCatGUI import view_category_bp
from boundary.PMUpdateServCat import update_category_bp
from boundary.PMSuspendServCat import suspend_category_bp
from boundary.PMViewReportsGUI import view_reports_bp
from boundary.CleanerConfirmedMatchesPg import confirmed_matches_bp
from boundary.CleanerFilterHistoryPg import filter_history_bp
from boundary.CleanerSearchHistoryPage import cleaner_search_history_bp
from boundary.ShortlistCountForCleanerPage import shortlist_bp
from boundary.ServiceViewsPage import service_views_bp
from boundary.ServiceSuspensionPage import suspend_service_bp
from boundary.CleanerSearchServicePage import search_service_bp
from boundary.CleanerViewServicePage import view_service_bp
from boundary.CleanerCreateService import create_service_bp
from boundary.CleanerUpdateServicePage import update_service_bp

import secret # for access secret key -- SESSION



app = Flask(__name__)

app.secret_key = 'not-secret'

app.register_blueprint(login_ui)
app.register_blueprint(register_ui)
app.register_blueprint(register_profile_ui)
app.register_blueprint(view_acc)
app.register_blueprint(update_user_ui)
app.register_blueprint(view_prof)
app.register_blueprint(update_profile_ui)
# app.register_blueprint(view_hoservice_bp)
# app.register_blueprint(view_hoshortlist_bp)
app.register_blueprint(view_completedservice_bp)
app.register_blueprint(createservcat_bp)
app.register_blueprint(view_category_bp)
app.register_blueprint(update_category_bp)
app.register_blueprint(suspend_category_bp)
app.register_blueprint(view_reports_bp)
app.register_blueprint(confirmed_matches_bp)
app.register_blueprint(shortlist_bp)
app.register_blueprint(service_views_bp)
app.register_blueprint(suspend_service_bp)
app.register_blueprint(search_service_bp)
app.register_blueprint(view_service_bp)
app.register_blueprint(create_service_bp)
app.register_blueprint(update_service_bp)
app.register_blueprint(filter_history_bp, name='cleaner_filter_history')
app.register_blueprint(cleaner_search_history_bp, name='cleaner_search_history')
app.secret_key = secret.SECRET_KEY # SESSION RELATED


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)