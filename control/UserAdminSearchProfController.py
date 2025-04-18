from entity.UserProfile import UserProfile

class UserAdminSearchProfController:
    def SearchUserProfile(profilename):
        return UserProfile.SearchProfile(profilename)