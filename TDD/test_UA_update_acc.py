import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserAccount import UserAccount

def test_updateUserAcc():
    userid = "28"
    change_username = "john333"
    change_password = "abcd222"
    change_profileid = 2
    
    result = UserAccount.UpdateUserAccount(userid, change_username, change_password, change_profileid)
    
    assert result is True