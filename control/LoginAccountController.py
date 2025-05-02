from entity.UserAccount import UserAccount

class LoginAccountController:
    def AuthenticateDetails(self, userid, username, password, profileid):
        if not username or not password:
            return "Username and password cannot be empty."
        
        # Create user object
        user = UserAccount(userid, username, password, profileid)
        
        # Call and return the instance method
        return user.Authenticate()