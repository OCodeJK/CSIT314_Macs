from entity.Reports import Report

class PMViewMonthlyReportsController:
    def ViewMonthlyReport(self, year, month):
        return Report.ViewMonthlyReport(year, month)
