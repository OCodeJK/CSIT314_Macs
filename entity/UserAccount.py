import psycopg2
from db_config import db_connection

#1 is for User Admin
#2 is for Cleaner
#3 is for Homeowner
#4 is for Platform Management

class UserAccount:
    def __init__(self, username, password, profileid):
        self.__username = username
        self.__password = password
        self.__profileid = profileid
        
        
    #Getters
    def get_username(self):
        return self.__username

    def get_profileid(self):
        if (self.__profileid == 1):
            return "User Admin"
        else:
            None
    

    #Create account (username, password and profile)
    def createUserAccount(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO account (username, password, profileid) VALUES (%s, %s, %s) RETURNING userid"
                        , (self.__username, self.__password, self.__profileid))
            userid = cur.fetchone()[0]
            conn.commit()
            
            #If the profile_id is for example 1, insert into useradmin table
            if self.__profileid == "1": 
                cur.execute(
                    "INSERT INTO useradmin (userid) VALUES (%s)", (userid,)
                )
                conn.commit()
                
            return True
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("Username already exists.")
        except Exception as e:
            print("DB Error:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    
    #Login (username, password and profile/role)    
    @staticmethod
    def Authenticate(username, password, profileid):  
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT username, password, account.profileid from account INNER JOIN profile 
            ON account.profileid = profile.profileid 
            WHERE account.username=%s AND account.password=%s AND profile.profileid=%s"""
            , (username, password, profileid)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            username, password, profileid = row
            return UserAccount(username, password, profileid)
        else:
            return None
