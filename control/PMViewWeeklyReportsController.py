from entity.Reports import Report

class PMViewWeeklyReportsController:
    def __init__(self):
        self.entity = Report()

    def ViewWeeklyReports(self, year, week):
        return self.entity.ViewWeeklyReport(year, week)
