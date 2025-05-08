from entity.Reports import Report

class PMSearchMonthlyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchMonthlyReports(self, year, month, category_name):
        return self.entity.SearchMonthlyReport(year, month, category_name)
