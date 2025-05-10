from db_config import db_connection

class Cleaner:
    """Entity class representing a Cleaner in the system"""
    
    def __init__(self, cleanerId=None):
        self.cleanerId = cleanerId


    @classmethod
    def get_by_id(cls, cleanerId):
        """Get a cleaner by ID"""
        conn = db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM cleaner WHERE cleanerId = %s", (cleanerId,))
        c = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not c:
            return None
        
        return {'cleanerId': c[0]}