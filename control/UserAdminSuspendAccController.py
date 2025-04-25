from entity.UserAccount import UserAccount

class UserAdminSuspendAccController():
    def userAdminSuspendAcc(userid):
        return UserAccount.suspendUser(userid)