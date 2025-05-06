from entity.Shortlist import Shortlist

class HomeownerSearchShortlistController:
    def homeownerSearchShortlist(userid, cleaneruser):
        return Shortlist.searchShortlistForHomeowner(userid, cleaneruser)