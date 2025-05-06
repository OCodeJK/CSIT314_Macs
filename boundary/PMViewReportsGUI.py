from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.PMViewReportsController import PMViewReportsController
import datetime

view_reports_bp = Blueprint('view_reports', __name__)

def is_platform_management():
    return session.get('profileid') == "Platform Management"

def get_daily_options():
    start_date = datetime.date(2024, 1, 1)
    today = datetime.date.today()
    delta = today - start_date
    return [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

def get_weekly_options():
    start_date = datetime.date(2024, 1, 1)
    today = datetime.date.today()
    # Find first Monday on or after start_date
    first_monday = start_date + datetime.timedelta(days=(7 - start_date.weekday()) % 7)
    weeks = []
    current = first_monday
    while current <= today:
        iso_year, iso_week, _ = current.isocalendar()
        weeks.append({'label': current.strftime('%Y-%m-%d'), 'value': f'{iso_year}-{iso_week:02d}'})
        current += datetime.timedelta(days=7)
    return weeks

def get_monthly_options():
    start_year, start_month = 2024, 1
    end_year, end_month = 2025, 12
    months = []
    year, month = start_year, start_month
    while (year < end_year) or (year == end_year and month <= end_month):
        months.append(f"{year}-{month:02d}")
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    return months

@view_reports_bp.route('/admin/view_report', methods=['GET', 'POST'])
def view_report():
    if not is_platform_management():
        flash("Unauthorized: Only Platform Management can access this page.")
        return redirect(url_for('login_ui.Login'))

    report_data = None
    selected_daily = None
    selected_weekly = None
    selected_monthly = None
    report_type = None

    daily_options = get_daily_options()
    weekly_options = get_weekly_options()
    monthly_options = get_monthly_options()

    if request.method == 'POST':
        controller = PMViewReportsController()
        if 'view_daily' in request.form:
            selected_daily = request.form.get('daily')
            report_data = controller.PMViewReports('daily', selected_daily)
            report_type = 'daily'
            if not report_data:
                flash("No records found for the selected period.")
        elif 'view_weekly' in request.form:
            selected_weekly = request.form.get('weekly')
            report_data = controller.PMViewReports('weekly', selected_weekly)
            report_type = 'weekly'
            if not report_data:
                flash("No records found for the selected period.")
        elif 'view_monthly' in request.form:
            selected_monthly = request.form.get('monthly')
            report_data = controller.PMViewReports('monthly', selected_monthly)
            report_type = 'monthly'
            if not report_data:
                flash("No records found for the selected period.")

    return render_template(
        'view_reports.html',
        daily_options=daily_options,
        weekly_options=weekly_options,
        monthly_options=monthly_options,
        report_data=report_data,
        selected_daily=selected_daily,
        selected_weekly=selected_weekly,
        selected_monthly=selected_monthly,
        report_type=report_type
    )
