import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserProfile import UserProfile

def test_searchProfile_exists():
    results = UserProfile.searchProfile("User Admin")
    assert results is not None
    returned_profiles = [row[1] for row in results]
    
    assert "User Admin" in returned_profiles
    

def test_searchProfile_not_exists():
    result = UserProfile.searchProfile("jk")
    assert result == []