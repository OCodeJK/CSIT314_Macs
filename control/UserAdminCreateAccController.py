from entity.UserAccount import UserAccount

class UserAdminCreateAccController:
    def userCreateAccount(self, username, password, profileid):
        try:
            user = UserAccount(username, password, profileid)
            return user.createUserAccount()
        except ValueError as ve:
            return str(ve)
        except Exception:
            return False