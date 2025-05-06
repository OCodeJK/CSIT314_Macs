from entity.Shortlist import Shortlist

class HomeownerViewShortlistController:
    def homeownerViewShortlist(userid):
        return Shortlist.viewShortlistForHomeowner(userid)