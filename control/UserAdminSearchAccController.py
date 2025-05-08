from entity.UserAccount import UserAccount

class UserAdminSearchAccController:
    def searchUserAccount(username):
        return UserAccount.searchUser(username)