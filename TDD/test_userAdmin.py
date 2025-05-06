import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserAccount import UserAccount
from db_config import db_connection

# Helper function to clear test users between test runs
def clear_test_user(username):
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM cleaner where cleanerid in (SELECT userid FROM account WHERE username = %s)", (username,))
        cur.execute("DELETE FROM homeowner WHERE homeownerid IN (SELECT userid FROM account WHERE username = %s)", (username,))
        cur.execute("DELETE FROM account WHERE username = %s", (username,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Cleanup error: ", e)

# Assertion test cases
def test_createUserAccount():
    username = "test_cleaner"
    password = "pass123"
    profileid = 2 # Cleaner
    clear_test_user(username)
    
    account = UserAccount(username, password, profileid)
    result = account.createUserAccount()

    assert result == True, "Failed to create user account."

def test_createDuplicateAccount():
    username = "jk"
    password = "123"
    profileid = "1" # User Admin
    
    account = UserAccount(username, password, profileid)
    
    with pytest.raises(ValueError, match="Username already exists."):
        account.createUserAccount()