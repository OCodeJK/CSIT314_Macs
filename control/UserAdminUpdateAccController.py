from entity.UserAccount import UserAccount

class UserAdminUpdateAccController:
    def UserAdminUpdateAcc(self, userid, username, password, profileid):
        return UserAccount.UpdateUserAccount(userid, username, password, profileid)