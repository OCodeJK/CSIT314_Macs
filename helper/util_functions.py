from db_config import db_connection
import datetime

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

def get_all_services():
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT servicename FROM service ORDER BY servicename;")
            return [row[0] for row in cur.fetchall()]

def get_daily_options():
    start_date = datetime.date(2024, 1, 1)
    today = datetime.date.today()
    delta = today - start_date
    return [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

def get_weekly_options():
    start_date = datetime.date(2024, 1, 1)
    today = datetime.date.today()
    first_monday = start_date + datetime.timedelta(days=(7 - start_date.weekday()) % 7)
    weeks = []
    current = first_monday
    while current <= today:
        iso_year, iso_week, _ = current.isocalendar()
        weeks.append({'label': current.strftime('%Y-%m-%d'), 'value': f'{iso_year}-{iso_week:02d}'})
        current += datetime.timedelta(days=7)
    return weeks

def get_monthly_options():
    start_year, start_month = 2024, 1
    end_year, end_month = datetime.date.today().year, datetime.date.today().month
    months = []
    year, month = start_year, start_month
    while (year < end_year) or (year == end_year and month <= end_month):
        months.append(f"{year}-{month:02d}")
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    return months

def GetCategoryById(category_id: int):
    """
    Fetch a single category by its ID.
    """
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT categoryid, categoryname, suspend FROM public.category WHERE categoryid = %s",
                (category_id,)
            )
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

def viewServiceForHomeownerH():
        """Display all services with cleaner and category information"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.serviceid, s.servicename, a.username
                FROM service s
                INNER JOIN account a ON s.cleanerid = a.userid
                INNER JOIN category c ON s.categoryid = c.categoryid
            """)
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()

            return ResultSet
        except Exception as e:
            print("Error fetching cleaner accounts:", e)
            return None
        


@staticmethod
def get_all():
    """Get all services from the database"""
    conn = db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM service")
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return results
    
@staticmethod
def get_available_services():

    conn = db_connection()
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT * FROM service 
        WHERE (cleanerId IS NULL) 
        AND suspend = FALSE
        ORDER BY serviceName
        """
    )
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return results





@staticmethod
def get_by_id(cleanerId):
    """Get a cleaner by ID"""
    conn = db_connection()
    cur = conn.cursor()
    
    # Validate and convert cleanerId to int
    if not cleanerId or cleanerId == '':
        cur.close()
        conn.close()
        return None
    
    try:
        cleanerId = int(cleanerId)
    except (ValueError, TypeError):
        cur.close()
        conn.close()
        return None
    
    try:
        # Query cleaner table with cleanerId column (not serviceId)
        cur.execute("SELECT * FROM cleaner WHERE cleanerId = %s", (cleanerId,))
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not result:
            return None
        
        # Return cleaner data (adjust based on your cleaner table structure)
        return {
            'cleanerId': result[0],
            # Add other cleaner fields as needed
        }
        
    except Exception as e:
        print(f"Error in get_by_id: {str(e)}")
        cur.close()  
        conn.close()
        return None


@staticmethod
def getServiceWithDetails(serviceId):
    """Get service details with category information"""
    conn = db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            """
            SELECT s.serviceId, s.serviceName, s.categoryId, s.cleanerId, s.price, 
                    s.suspend, c.categoryName
            FROM service s
            LEFT JOIN category c ON s.categoryId = c.categoryId
            WHERE s.serviceId = %s
            """,
            (serviceId,)
        )
        
        result = cur.fetchone()
        
        if result:
            # Convert to dictionary for easier access
            service = {
                'serviceId': result[0],
                'serviceName': result[1],
                'categoryId': result[2],
                'cleanerId': result[3],
                'price': result[4],
                'suspend': result[5],
                'categoryName': result[6]
            }
            
            cur.close()
            conn.close()
            return service
        else:
            cur.close()
            conn.close()
            return None
            
    except Exception as e:
        print(f"Error in getServiceWithDetails: {str(e)}")
        cur.close()
        conn.close()
        return None
