import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserAccount import UserAccount

def test_Authenticate_success():
    existing_username = "jk"
    existing_password = "123"
    profileid = 1

    account = UserAccount(existing_username, existing_password, profileid)
    result = account.Authenticate()
    
    # assert the return is UserAccount object
    assert isinstance(result, UserAccount)
    
    
def test_Authenticate_failed():
    username = "squidward"
    password = "2223"
    profileid = 2
    
    account = UserAccount(username, password, profileid)
    result = account.Authenticate()
    
    assert result is None