import psycopg2
from db_config import db_connection


class UserProfile:
    def __init__(self, profilename):
        self.__profilename = profilename
        
    def get_profilename(self):
        return self.__profilename
    
    def createUserProfile(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO profile (profilename) VALUES (%s)", (self.__profilename,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("Profile already exists.")
        except Exception as e:
            print("DB Error:", e)
            conn.rollback()
            return False
        
    @staticmethod
    def viewUserProfile():
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT profileid, profilename FROM profile ORDER BY profileid")
            profiles = cur.fetchall()
            return profiles
        except Exception as e:
            print("DB error:", e)
            return None
        finally:
            cur.close()
            conn.close()
    
    
    @staticmethod
    def SearchProfile(profilename):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT profileid, profilename FROM profile
                WHERE profilename ILIKE %s
            """, (f"%{profilename}%",))
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()
            return ResultSet
        except Exception as e:
            print("DB error:", e)
            return None  