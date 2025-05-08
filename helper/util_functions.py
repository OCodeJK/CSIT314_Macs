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