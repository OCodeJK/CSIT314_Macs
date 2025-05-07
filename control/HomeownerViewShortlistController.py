from entity.Shortlist import Shortlist

class HomeownerViewShortlistController:
    def homeownerViewShortlist(userid):
        ResultSet = Shortlist.viewShortlistForHomeowner(userid)
        return ResultSet