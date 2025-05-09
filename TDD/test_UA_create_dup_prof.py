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
        
def test_createUserProfile_duplicate():
    profilename = "User Admin"

    # The insertion should fail (return false) because duplicate
    profile = UserProfile(profilename)
    result = profile.createUserProfile()
    
    assert result is False
    