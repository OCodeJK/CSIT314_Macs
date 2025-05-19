from entity.Reports import Report

class PMViewWeeklyReportsController:
    def ViewWeeklyReport(self, year, week):
        return Report.ViewWeeklyReport(year, week)
