import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from entity.UserAccount import UserAccount
from db_config import db_connection

def clear_test_user(username):
    """Helper to remove test users between test runs."""
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM cleaner WHERE cleanerid IN (SELECT userid FROM account WHERE username = %s)", (username,))
        cur.execute("DELETE FROM homeowner WHERE homeownerid IN (SELECT userid FROM account WHERE username = %s)", (username,))
        cur.execute("DELETE FROM account WHERE username = %s", (username,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Cleanup error:", e)

def test_createUserAccount_success():
    username = "test_cleaner"
    password = "pass123"
    profileid = 2
    clear_test_user(username)
    
    account = UserAccount(username, password, profileid)
    result = account.createUserAccount()
    
    assert result is True

def test_createUserAccount_duplicate():
    existing_username = "jk"
    existing_password = "123"
    profileid = 1

    account = UserAccount(existing_username, existing_password, profileid)

    with pytest.raises(ValueError, match="Username already exists."):
        account.createUserAccount()