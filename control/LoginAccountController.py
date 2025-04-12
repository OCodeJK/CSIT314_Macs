from entity.UserAccount import UserAccount

class LoginAccountController:
    def AuthenticateDetails(self, username, password, profileid):
        return UserAccount.Authenticate(username, password, profileid)