from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.PMViewDailyReportsController import PMViewDailyReportsController
from control.PMViewWeeklyReportsController import PMViewWeeklyReportsController
from control.PMViewMonthlyReportsController import PMViewMonthlyReportsController
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
    # ... (auth, option generation as before) ...
    report_data = None
    report_type = None

    if request.method == 'POST':
        if 'view_daily' in request.form:
            date_str = request.form.get('daily')
            controller = PMViewDailyReportsController()
            report_data = controller.ViewDailyReports(date_str)
            report_type = 'daily'
        elif 'view_weekly' in request.form:
            weekly_val = request.form.get('weekly')  # e.g. "2024-03"
            year, week = map(int, weekly_val.split('-'))
            controller = PMViewWeeklyReportsController()
            report_data = controller.ViewWeeklyReports(year, week)
            report_type = 'weekly'
        elif 'view_monthly' in request.form:
            monthly_val = request.form.get('monthly')  # e.g. "2024-05"
            year, month = map(int, monthly_val.split('-'))
            controller = PMViewMonthlyReportsController()
            report_data = controller.ViewMonthlyReports(year, month)
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
