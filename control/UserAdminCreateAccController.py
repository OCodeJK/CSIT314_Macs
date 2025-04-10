from entity.UserAccount import UserAccount

class UserAdminCreateAccController:
    def userCreateAccount(self, username, password, profile_id):
        try:
            return UserAccount.createUserAccount(username, password, profile_id)
        except ValueError as ve:
            return str(ve)
        except Exception:
            return False