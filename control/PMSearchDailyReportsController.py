from entity.Reports import Report

class PMSearchDailyReportsController:
    def __init__(self):
        self.entity = Report()

    def SearchDailyReports(self, date_str, category_name):
        return self.entity.SearchDailyReport(date_str, category_name)

    def GetAllCategories(self):
        return self.entity.get_all_services()
