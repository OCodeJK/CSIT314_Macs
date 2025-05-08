from entity.UserProfile import UserProfile

class UserAdminSuspendProfController:
    def userAdminSuspendProf(profileid):
        return UserProfile.suspendProfile(profileid)