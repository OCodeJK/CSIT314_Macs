from entity.UserAccount import UserAccount

class LoginAccountController:
    def AuthenticateDetails(self, username, password, profileid):
        if not username or not password:
            return "Username and password cannot be empty."
        
        
        return UserAccount.Authenticate(username, password, profileid)