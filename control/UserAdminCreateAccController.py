from entity.UserAccount import UserAccount

class UserAdminCreateAccController:
    def userCreateAccount(self, username, password, profile_id):
        try:
            user = UserAccount(username, password, profile_id)
            return user.createUserAccount()
        except ValueError as ve:
            return str(ve)
        except Exception:
            return False