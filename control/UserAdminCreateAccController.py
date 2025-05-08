from entity.UserAccount import UserAccount

class UserAdminCreateAccController:
    def userCreateAccount(self, username, password, profileid):
        if not username or not password:
            return "Username and password cannot be empty."
        try:
            user = UserAccount(username, password, profileid)
            return user.createUserAccount()
        except Exception:
            return False
