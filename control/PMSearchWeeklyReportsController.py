from entity.Reports import Report

class PMSearchWeeklyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchWeeklyReports(self, year, week, category_name):
        return self.entity.SearchWeeklyReport(year, week, category_name)