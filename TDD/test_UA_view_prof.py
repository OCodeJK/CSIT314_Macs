import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.UserProfile import UserProfile

# Define 5 test profiles (already inserted)
test_profiles = ["User Admin", "Cleaner", "Homeowner", "Platform Management"]

def test_viewUserProfiles():
    results = UserProfile.viewUserProfile()
    assert results is not None
    
    found_profiles = [row[1] for row in results]  # row[1] = profilename
    for name in test_profiles:
        assert name in found_profiles