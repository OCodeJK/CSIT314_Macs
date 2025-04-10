import psycopg2
from db_config import db_connection


class UserProfile:
    @staticmethod
    def createUserProfile(profilename):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO profiles (profilename) VALUES (%s)", (profilename,))
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