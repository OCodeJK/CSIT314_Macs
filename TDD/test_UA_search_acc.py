import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserAccount import UserAccount

def test_searchUser_exists():
    results = UserAccount.searchUser("jk")
    assert results is not None
    returned_usernames = [row[1] for row in results]
    
    assert "jk" in returned_usernames
    

def test_searchUser_not_exists():
    result = UserAccount.searchUser(None)
    assert result == []