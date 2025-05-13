from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.PMViewDailyReportsController import PMViewDailyReportsController
from control.PMViewWeeklyReportsController import PMViewWeeklyReportsController
from control.PMViewMonthlyReportsController import PMViewMonthlyReportsController
from control.PMSearchDailyReportsController import PMSearchDailyReportsController
from control.PMSearchWeeklyReportsController import PMSearchWeeklyReportsController
from control.PMSearchMonthlyReportsController import PMSearchMonthlyReportsController
from helper.util_functions import get_all_services, get_daily_options, get_weekly_options, get_monthly_options
import datetime

view_reports_bp = Blueprint('view_reports', __name__)

@view_reports_bp.route('/admin/view_report', methods=['GET', 'POST'])
def view_report():

    # Use the controller to get all services
    options_controller = PMSearchDailyReportsController()
    all_services = get_all_services()
    daily_options = get_daily_options()
    weekly_options = get_weekly_options()
    monthly_options = get_monthly_options()

    selected_daily = None
    selected_weekly = None
    selected_monthly = None
    selected_services = []
    report_data = None
    report_type = None

    if request.method == 'POST':
        selected_services = request.form.getlist('services')

        if 'view_daily' in request.form:
            selected_daily = request.form.get('daily')
            if selected_services:
                controller = PMSearchDailyReportsController()
                success, message, report_data = controller.SearchDailyReports(selected_daily, selected_services)
                if not success:
                    flash(message)
            else:
                controller = PMViewDailyReportsController()
                report_data = controller.ViewDailyReport(selected_daily)
            report_type = 'daily'

        elif 'view_weekly' in request.form:
            selected_weekly = request.form.get('weekly')
            year, week = map(int, selected_weekly.split('-'))
            if selected_services:
                controller = PMSearchWeeklyReportsController()
                success, message, report_data = controller.SearchWeeklyReports(year, week, selected_services)
                if not success:
                    flash(message)
            else:
                controller = PMViewWeeklyReportsController()
                report_data = controller.ViewWeeklyReport(year, week)
            report_type = 'weekly'

        elif 'view_monthly' in request.form:
            selected_monthly = request.form.get('monthly')
            year, month = map(int, selected_monthly.split('-'))
            if selected_services:
                controller = PMSearchMonthlyReportsController()
                success, message, report_data = controller.SearchMonthlyReports(year, month, selected_services)
                if not success:
                    flash(message)
            else:
                controller = PMViewMonthlyReportsController()
                report_data = controller.ViewMonthlyReport(year, month)
            report_type = 'monthly'

        if not selected_services and (report_data is None or len(report_data) == 0):
            flash("No records found for the selected period.")

    return render_template(
        'view_reports.html',
        daily_options=daily_options,
        weekly_options=weekly_options,
        monthly_options=monthly_options,
        datetime = datetime,
        all_services=all_services,
        selected_daily=selected_daily,
        selected_weekly=selected_weekly,
        selected_monthly=selected_monthly,
        selected_services=selected_services,
        report_data=report_data,
        report_type=report_type
    )