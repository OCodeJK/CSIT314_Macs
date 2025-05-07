from entity.User import User

class PMViewDailyReportsController:
    def __init__(self):
        self.entity = User()

    def ViewDailyReports(self, date_str):
        return self.entity.ViewDailyReport(date_str)
