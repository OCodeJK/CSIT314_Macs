import psycopg2
from db_config import db_connection


class UserProfile:
    def __init__(self, profilename):
        self.__profilename = profilename
        
    def get_profilename(self):
        return self.__profilename
    
    # Create Profile (profilename)
    def createUserProfile(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            cur.execute("INSERT INTO profile (profilename) VALUES (%s)", (self.__profilename,))
            conn.commit()
            
            return True
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return False
        except Exception as e:
            print("DB Error:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
        
    @staticmethod
    def viewUserProfile():
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT profileid, profilename, suspend FROM profile ORDER BY profileid")
            profiles = cur.fetchall()
            return profiles
        except Exception as e:
            print("DB error:", e)
            return None
        finally:
            cur.close()
            conn.close()
            
    @staticmethod
    def updateUserProfile(profileid, profilename):
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            # check if username exists in the database before update
            cur.execute("""
                SELECT profilename FROM profile 
                WHERE profilename = %s AND profileid != %s
            """, (profilename, profileid)) 
            
            result = cur.fetchone()
            
            if result:
                return False
            
            cur.execute("""
                UPDATE profile
                SET profilename = %s
                WHERE profileid = %s            
            """, (profilename, profileid))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("DB error:", e)
            return False
    
    
    @staticmethod
    def searchProfile(profilename):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT profileid, profilename, suspend FROM profile
                WHERE profilename ILIKE %s
            """, (f"%{profilename}%",))
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()
            return ResultSet
        except Exception as e:
            print("DB error:", e)
            return None
        
        
        
    @staticmethod
    def suspendProfile(profileid):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT suspend FROM profile WHERE profileid= %s", (profileid,))
            current_status = cur.fetchone()
            
            if current_status[0] is True:
                return False # Already suspended
            
            #suspend the account
            cur.execute("UPDATE profile set suspend=TRUE WHERE profileid = %s", (profileid,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print("DB error:", e)
            return False