import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserAccount import UserAccount

def test_suspendUser():
    userid = 28
    
    # suspend user account with id 28 if its not suspended 
    result = UserAccount.suspendUser(userid)
    
    # return true if suspension goes through (suspend = false to true)
    assert result is True