from entity.Cleaner import Cleaner

class HomeownerSearchCleanerController:
    def homeownerSearchCleaner(cleaneruser):
        return Cleaner.searchCleanerForHomeowner(cleaneruser)