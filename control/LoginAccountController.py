from entity.UserAccount import UserAccount

class LoginAccountController:
    def AuthenticateDetails(self, username, password, profilename):
        return UserAccount.Authenticate(username, password, profilename)