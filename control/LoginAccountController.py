from entity.UserAccount import UserAccount

class LoginAccountController:
    def AuthenticateDetails(self, username, password, role):
        return UserAccount.Authenticate(username, password, role)