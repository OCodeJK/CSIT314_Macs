from db_config import db_connection

def get_all_profiles():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT profileid, profilename FROM profile ORDER BY profileid ASC")
    profiles = cur.fetchall()
    cur.close()
    conn.close()
    return profiles