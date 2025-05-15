from db_config import db_connection

class Cleaner:
    """Entity class representing a Cleaner in the system"""
    
    def __init__(self, cleanerId=None):
        self.cleanerId = cleanerId

