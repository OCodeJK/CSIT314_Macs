from entity.Shortlist import Shortlist

class HomeownerSearchShortlistController:
    def homeownerSearchShortlist(userid, servicename):
        ResultSet = Shortlist.searchShortlistForHomeowner(userid, servicename)
        return ResultSet