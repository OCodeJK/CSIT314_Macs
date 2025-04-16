from entity.UserAccount import UserAccount

class UserAdminSuspendAccController():
    def UserAdminSuspendAcc(userid):
        return UserAccount.SuspendUser(userid)