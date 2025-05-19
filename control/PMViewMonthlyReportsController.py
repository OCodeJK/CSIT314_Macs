from entity.Reports import Report

class PMViewMonthlyReportsController:
    def __init__(self):
        self.entity = Report()

    def ViewMonthlyReport(self, year, month):
        return self.entity.ViewMonthlyReport(year, month)
