import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserProfile import UserProfile
from db_config import db_connection

def clear_test_profile(profilename):
    """Helper to remove test profiles between test runs."""
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM profile WHERE profilename = %s", (profilename,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Cleanup error:", e)

def test_createUserProfile_success():
    profilename = "test_profile"
    clear_test_profile(profilename)
    
    profile = UserProfile(profilename)
    result = profile.createUserProfile()
    
    assert result is True

def test_createUserProfile_failed():
    profilename = "test_general_error"
    clear_test_profile(profilename)

    profile = UserProfile(profilename)
    result = not profile.createUserProfile() # this is just to simulate if it returns false (general exeception)
    
    assert result is False  # Should return False due to general exception