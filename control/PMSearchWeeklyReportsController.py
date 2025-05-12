from entity.Reports import Report

class PMSearchWeeklyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchWeeklyReports(self, year, week, services_name):
        return self.entity.SearchWeeklyReport(year, week, services_name)