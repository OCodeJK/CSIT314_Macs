import psycopg2
from db_config import db_connection

class UserAccount:
    def __init__(self, username, password, profilename):
        self.__username = username
        self.__password = password
        self.__profilename = profilename
        
        
    #Getters
    def get_username(self):
        return self.__username

    def get_profilename(self):
        return self.__profilename
    

    #Create account (username, password and profile)
    def createUserAccount(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO account (username, password, profileid) VALUES (%s, %s, %s)"
                        , (self.__username, self.__password, self.__profilename))
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
    
    
    #Login (username, password and profile)    
    @staticmethod
    def Authenticate(username, password, profilename):  
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT username, password, profilename from account INNER JOIN profile 
            ON account.profileid = profile.profileid 
            WHERE account.username=%s AND account.password=%s AND profile.profilename=%s"""
            ,(username, password, profilename)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            username, password, profilename = row
            return UserAccount(username, password, profilename)
        else:
            return None
