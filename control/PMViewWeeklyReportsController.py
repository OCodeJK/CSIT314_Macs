from entity.Reports import Report

class PMViewWeeklyReportsController:
    def __init__(self):
        self.entity = Report()

    def ViewWeeklyReport(self, year, week):
        return self.entity.ViewWeeklyReport(year, week)
