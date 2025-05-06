from entity.User import User

class PMViewReportsController:
    def __init__(self):
        self.entity = User()

    def PMViewReports(self, interval, value):
        return self.entity.ViewReport(interval, value)
