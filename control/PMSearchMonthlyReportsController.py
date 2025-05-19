from entity.Reports import Report

class PMSearchMonthlyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchMonthlyReports(self, year, month, services_name):
        return self.entity.SearchMonthlyReport(year, month, services_name)
