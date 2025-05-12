from entity.Reports import Report

class PMViewDailyReportsController:
    def __init__(self):
        self.entity = Report()

    def ViewDailyReport(self, date_str):
        return self.entity.ViewDailyReport(date_str)
