import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserProfile import UserProfile

def test_updateProfile():
    profileid = 2
    profilename = "cleaner_test"
    
    result = UserProfile.updateUserProfile(profileid, profilename)
    
    assert result is True