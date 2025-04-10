import psycopg2
from db_config import db_connection

class UserAccount:
    @staticmethod
    def createUserAccount(username, password, profile_id):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO user_accounts (username, password, profileid) VALUES (%s, %s, %s)", (username, password, profile_id))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("Username already exists.")
        except Exception as e:
            print("DB Error:", e)
            conn.rollback()
            return False
        
    @staticmethod
    def Authenticate(username, password, role):
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT username, password, profilename from user_accounts INNER JOIN profiles 
            ON user_accounts.profileid = profiles.profileid 
            WHERE user_accounts.username=%s AND user_accounts.password=%s AND profiles.profilename=%s"""
            ,(username, password, role)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user is not None

