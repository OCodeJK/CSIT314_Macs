from entity.User import User

class PMViewWeeklyReportsController:
    def __init__(self):
        self.entity = User()

    def ViewWeeklyReports(self, year, week):
        return self.entity.ViewWeeklyReport(year, week)
