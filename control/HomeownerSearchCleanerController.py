from entity.Cleaner import Cleaner

class HomeownerSearchCleanerController:
    def homeownerSearchCleaner(cleaneruser):
        ResultSet = Cleaner.searchCleanerForHomeowner(cleaneruser)
        return ResultSet