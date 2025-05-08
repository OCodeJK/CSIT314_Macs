import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserAccount import UserAccount

# Define 5 test users
test_users = [
    ("jk", "123", 1),
    ("led", "123", 1),
    ("boom", "123", 2),
    ("greentea", "123", 3),
    ("coffee", "123", 4)
]

def test_viewUserDetails_5_users():
    results = UserAccount.viewUserDetails()
    assert results is not None
    
    returned_usernames = [row[1] for row in results]  # row[1] is username
    for username, _, _ in test_users:
        assert username in returned_usernames
    