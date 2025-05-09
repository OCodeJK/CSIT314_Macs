from entity.UserProfile import UserProfile

class UserAdminSearchProfController:
    def searchUserProfile(profilename):
        return UserProfile.searchProfile(profilename)