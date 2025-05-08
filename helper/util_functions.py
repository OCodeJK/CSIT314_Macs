from db_config import db_connection

def get_all_profiles():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT profileid, profilename FROM profile ORDER BY profileid ASC")
    profiles = cur.fetchall()
    cur.close()
    conn.close()
    return profiles


def get_user_by_id(userid):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM account WHERE userid = %s", (userid,))
    user = cur.fetchone()
    conn.close()
    return user

def get_profile_by_id(profileid):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profile WHERE profileid = %s", (profileid,))
    profile = cur.fetchone()
    conn.close()
    cur.close()
    return profile

def userReturnUID(username, password, profileid):  
        conn = db_connection()
        cur = conn.cursor()
        
        
        #login when not suspended
        cur.execute(
            """SELECT userid, username, password, account.profileid from account INNER JOIN profile 
            ON account.profileid = profile.profileid 
            WHERE account.username=%s AND account.password=%s AND profile.profileid=%s AND account.suspend=FALSE"""
            ,(username, password, profileid)
        )
        
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            userid, username, password, profileid = row
            return userid
        else:
            return None
        
        
        
def check_if_user_suspended(username, password, profileid):
    conn = db_connection()
    cur = conn.cursor()
    
    #check if account is suspended
    cur.execute("""
        SELECT suspend from account 
        WHERE username = %s AND password = %s AND profileid = %s""", (username, password, profileid)
    )
    account_result = cur.fetchone()
    
    if account_result is None:
            cur.close()
            conn.close()
            return None
        
        
    account_is_suspended = account_result[0]
    if account_is_suspended is True:
        #Account is suspended
        cur.close()
        conn.close()
        return "suspended"