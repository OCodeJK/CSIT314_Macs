from entity.UserProfile import UserProfile

class UserAdminProfileController:
    def createUserProfileController(self, profilename):
        try:
            return UserProfile.createUserProfile(profilename)
        except ValueError as ve:
            return str(ve)
        except Exception:
            return False