from entity.Shortlist import Shortlist

class HomeownerCreateShortlistController:
    def homeownerCreateShortlist(homeownerid, cleanerid):
        return Shortlist.createShortlistForHomeowner(homeownerid, cleanerid)