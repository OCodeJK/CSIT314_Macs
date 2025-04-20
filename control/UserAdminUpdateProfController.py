from entity.UserProfile import UserProfile

class UserAdminUpdateProfController:
    def userAdminUpdateProf(self, profileid, profilename):
        return UserProfile.updateUserProfile(profileid, profilename)