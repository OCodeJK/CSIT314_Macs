from entity.Shortlist import Shortlist

class HomeownerSearchShortlistController:
    def homeownerSearchShortlist(userid, cleanerid):
        return Shortlist.searchShortlistForHomeowner(userid, cleanerid)