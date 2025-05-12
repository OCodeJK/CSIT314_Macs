from entity.Reports import Report

class PMSearchDailyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchDailyReports(self, date_str, services_name):
        return self.entity.SearchDailyReport(date_str, services_name)

    def GetAllServices(self):
        return self.entity.get_all_services()

    def GetDailyOptions(self):
        return self.entity.get_daily_options()

    def GetWeeklyOptions(self):
        return self.entity.get_weekly_options()

    def GetMonthlyOptions(self):
        return self.entity.get_monthly_options()
