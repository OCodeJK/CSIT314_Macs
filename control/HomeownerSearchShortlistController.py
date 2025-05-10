from entity.Shortlist import Shortlist

class HomeownerSearchShortlistController:
    def homeownerSearchShortlist(userid, cleaneruser):
        ResultSet = Shortlist.searchShortlistForHomeowner(userid, cleaneruser)
        return ResultSet