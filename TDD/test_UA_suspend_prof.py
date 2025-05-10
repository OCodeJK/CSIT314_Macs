import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserProfile import UserProfile

def test_suspendProfile():
    profileid = 4
    
    # suspend user profile with id 4 if its not suspended 
    result = UserProfile.suspendProfile(profileid)
    
    # return true if suspension goes through (suspend = false to true)
    assert result is True