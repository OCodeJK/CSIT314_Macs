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
        elif(self.__profileid == 2):
            return "Cleaner"
        elif(self.__profileid == 3):
            return "Homeowner"
        elif(self.__profileid == 4):
            return "Platform Management"
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
        
        #check if account is suspended
        cur.execute("""
            SELECT suspend from account 
            WHERE username = %s AND password = %s AND profileid = %s""", (username, password, profileid)
        )
        result = cur.fetchone()
        
        if result is None:
            cur.close()
            conn.close()
            return None
        
        is_suspended = result[0]
        if is_suspended is True:
            #Account is suspended
            cur.close()
            conn.close()
            return "suspended"
        
        #login when not suspended
        cur.execute(
            """SELECT username, password, account.profileid from account INNER JOIN profile 
            ON account.profileid = profile.profileid 
            WHERE account.username=%s AND account.password=%s AND profile.profileid=%s AND account.suspend=FALSE"""
            ,(username, password, profileid)
        )
        
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            username, password, profileid = row
            return UserAccount(username, password, profileid)
        else:
            return None
    
    #View all accounts from the accounts database joined with profile
    @staticmethod
    def viewUserDetails():
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT a.userid, a.username, p.profilename, a.suspend 
                FROM account a 
                INNER JOIN profile p ON a.profileid = p.profileid
            """)
            users = cur.fetchall()
            cur.close()
            conn.close()
            return users
        except Exception as e:
            print("Error fetching user accounts:", e)
            return None
        
    @staticmethod
    def UpdateUserAccount(userid, username, password, profileid):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE account
                SET username = %s, password = %s, profileid = %s
                WHERE userid = %s            
            """, (username, password, profileid, userid))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("DB error:", e)
            return False
        
        
    @staticmethod
    def searchUser(username):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT a.userid, a.username, p.profilename, a.suspend
                FROM account a
                JOIN profile p ON a.profileid = p.profileid
                WHERE a.username ILIKE %s
            """, (f"%{username}%",))
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()
            return ResultSet
        except Exception as e:
            print("DB error:", e)
            return None    

    @staticmethod
    def suspendUser(userid):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT suspend FROM account WHERE userid= %s", (userid,))
            current_status = cur.fetchone()
            
            if current_status[0] is True:
                return False # Already suspended
            
            #suspend the account
            cur.execute("UPDATE account set suspend=TRUE WHERE userid = %s", (userid,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print("DB error:", e)
            return False