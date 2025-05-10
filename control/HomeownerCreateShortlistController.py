from entity.Shortlist import Shortlist

class HomeownerCreateShortlistController:
    def homeownerCreateShortlist(serviceid, homeownerid):
        return Shortlist.createShortlistForHomeowner(serviceid, homeownerid)