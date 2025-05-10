from entity.UserProfile import UserProfile

class UserAdminProfileController:
    def createUserProfileController(self, profilename):
        if not profilename:
            return "Invalid Input"
        try:
            profile = UserProfile(profilename)
            return profile.createUserProfile()
        except Exception:
            return False