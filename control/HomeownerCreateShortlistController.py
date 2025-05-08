from entity.Shortlist import Shortlist

class HomeownerCreateShortlistController:
    def homeownerCreateShortlist(cleanerid, homeownerid):
        return Shortlist.createShortlistForHomeowner(cleanerid, homeownerid)