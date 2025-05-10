from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.PMViewDailyReportsController import PMViewDailyReportsController
from control.PMViewWeeklyReportsController import PMViewWeeklyReportsController
from control.PMViewMonthlyReportsController import PMViewMonthlyReportsController
from control.PMSearchDailyReportsController import PMSearchDailyReportsController
from control.PMSearchWeeklyReportsController import PMSearchWeeklyReportsController
from control.PMSearchMonthlyReportsController import PMSearchMonthlyReportsController
import datetime

view_reports_bp = Blueprint('view_reports', __name__)

def get_daily_options():
    start_date = datetime.date(2024, 1, 1)
    today = datetime.date.today()
    delta = today - start_date
    return [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

def get_weekly_options():
    start_date = datetime.date(2024, 1, 1)
    today = datetime.date.today()
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

    # Use the controller to get all categories
    category_controller = PMSearchDailyReportsController()
    all_categories = category_controller.GetAllCategories()

    daily_options = get_daily_options()
    weekly_options = get_weekly_options()
    monthly_options = get_monthly_options()

    selected_daily = None
    selected_weekly = None
    selected_monthly = None
    selected_categories = []
    report_data = None
    report_type = None

    if request.method == 'POST':
        selected_categories = request.form.getlist('categories')

        if 'view_daily' in request.form:
            selected_daily = request.form.get('daily')
            if selected_categories:
                controller = PMSearchDailyReportsController()
                success, message, report_data = controller.SearchDailyReports(selected_daily, selected_categories)
                if not success:
                    flash(message)
            else:
                controller = PMViewDailyReportsController()
                report_data = controller.ViewDailyReports(selected_daily)
            report_type = 'daily'

        elif 'view_weekly' in request.form:
            selected_weekly = request.form.get('weekly')
            year, week = map(int, selected_weekly.split('-'))
            if selected_categories:
                controller = PMSearchWeeklyReportsController()
                success, message, report_data = controller.SearchWeeklyReports(year, week, selected_categories)
                if not success:
                    flash(message)
            else:
                controller = PMViewWeeklyReportsController()
                report_data = controller.ViewWeeklyReports(year, week)
            report_type = 'weekly'

        elif 'view_monthly' in request.form:
            selected_monthly = request.form.get('monthly')
            year, month = map(int, selected_monthly.split('-'))
            if selected_categories:
                controller = PMSearchMonthlyReportsController()
                success, message, report_data = controller.SearchMonthlyReports(year, month, selected_categories)
                if not success:
                    flash(message)
            else:
                controller = PMViewMonthlyReportsController()
                report_data = controller.ViewMonthlyReports(year, month)
            report_type = 'monthly'

        if not selected_categories and (report_data is None or len(report_data) == 0):
            flash("No records found for the selected period.")

    return render_template(
        'view_reports.html',
        daily_options=daily_options,
        weekly_options=weekly_options,
        monthly_options=monthly_options,
        all_categories=all_categories,
        selected_daily=selected_daily,
        selected_weekly=selected_weekly,
        selected_monthly=selected_monthly,
        selected_categories=selected_categories,
        report_data=report_data,
        report_type=report_type
    )