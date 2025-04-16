from entity.UserAccount import UserAccount

class UserAdminSearchAccController:
    def SearchUserAccount(username):
        return UserAccount.SearchUser(username)