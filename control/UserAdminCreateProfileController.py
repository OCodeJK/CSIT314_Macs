from entity.UserProfile import UserProfile

class UserAdminProfileController:
    def createUserProfileController(self, profilename):
        try:
            profile = UserProfile(profilename)
            return profile.createUserProfile()
        except ValueError as ve:
            return str(ve)
        except Exception:
            return False