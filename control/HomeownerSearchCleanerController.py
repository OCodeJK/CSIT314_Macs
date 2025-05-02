from entity.Cleaner import Cleaner

class HomeownerSearchCleanerController:
    def homeownerSearchCleaner(cleanerid):
        return Cleaner.searchCleanerForHomeowner(cleanerid)