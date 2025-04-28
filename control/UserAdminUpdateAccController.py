from entity.UserAccount import UserAccount

class UserAdminUpdateAccController:
    def UserAdminUpdateAcc(self, userid, username, password, profileid):
        if not username:
            return "Username cannot be empty"
        
        return UserAccount.UpdateUserAccount(userid, username, password, profileid)