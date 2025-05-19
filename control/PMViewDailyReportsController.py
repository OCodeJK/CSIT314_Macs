from entity.Reports import Report

class PMViewDailyReportsController:
    def ViewDailyReport(self, date_str):
        return Report.ViewDailyReport(date_str)
