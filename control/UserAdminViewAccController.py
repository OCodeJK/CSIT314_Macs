from entity.UserAccount import UserAccount

class UserAdminViewAccController:
    @staticmethod
    def view_all_user_accounts():
        return UserAccount.ViewUserDetails()