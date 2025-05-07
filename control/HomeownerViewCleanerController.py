from entity.Cleaner import Cleaner

class HomeownerViewCleanerController:
    def homeownerViewCleaner():
        ResultSet = Cleaner.viewCleanerForHomeowner()
        return ResultSet