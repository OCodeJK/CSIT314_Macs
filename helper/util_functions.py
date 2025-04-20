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