
from db_config import db_connection
from datetime import datetime

class HistoryRecord:
    def __init__(self, id=None, serviceId=None, startDate=None, endDate=None, cleanerId=None):
        self.id = id
        self.serviceId = serviceId
        self.startDate = startDate
        self.endDate = endDate
        self.cleanerId = cleanerId

        
    @staticmethod
    def searchService(searchName, cleanerId):
        try:
            if not searchName or searchName.strip() == "":
                return []
            
            conn = db_connection()
            cur = conn.cursor()
            
            query = """
                SELECT h.historyid, h.serviceid, h.startdate, h.enddate, h.cleanerid, s.servicename 
                FROM historyrecord h
                JOIN service s ON h.serviceid = s.serviceid
                WHERE h.cleanerid = %s 
                AND s.servicename ILIKE %s
                ORDER BY h.startdate DESC
            """
            
            search_pattern = f"%{searchName}%"
            cur.execute(query, (cleanerId, search_pattern))
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"[HistoryRecord] Error in searchService: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return []

    @staticmethod
    def cleanerViewConfirmedMatches(cleanerId) -> list:
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            cur.execute(
                """
                SELECT h.historyid, h.serviceid, h.startdate, h.enddate, h.cleanerid, s.servicename 
                FROM historyrecord h
                JOIN service s ON h.serviceid = s.serviceid
                ORDER BY h.startdate DESC
                """, 
                (cleanerId,)
            )
            
            matches = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return matches
                
        except Exception as e:
            print(f"Error getting confirmed matches: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return []
        
    @staticmethod
    def cleanerFilterHistory(cleanerId, startDate, endDate):
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            # If both dates are None, fetch all history records
            if startDate is None and endDate is None:
                cur.execute(
                    """
                    SELECT h.historyid, h.serviceid, h.startdate, h.enddate, h.cleanerid, s.servicename 
                    FROM historyrecord h
                    LEFT JOIN service s ON h.serviceid = s.serviceid
                    WHERE h.cleanerid = %s 
                    ORDER BY h.startdate DESC
                    """,
                    (cleanerId,)
                )
            else:
                # Use date conditions only when dates are provided
                start = startDate if startDate is not None else datetime(2000, 1, 1).date()
                end = endDate if endDate is not None else datetime.now().date()
                
                cur.execute(
                    """
                    SELECT h.historyid, h.serviceid, h.startdate, h.enddate, h.cleanerid, s.servicename 
                    FROM historyrecord h
                    LEFT JOIN service s ON h.serviceid = s.serviceid
                    WHERE h.cleanerid = %s 
                    AND (
                        (h.startdate BETWEEN %s AND %s) OR
                        (h.enddate BETWEEN %s AND %s) OR
                        (h.startdate <= %s AND (h.enddate IS NULL OR h.enddate >= %s))
                    )
                    ORDER BY h.startdate DESC
                    """,
                    (cleanerId, start, end, start, end, start, end)
                )
            
            # fetchall() returns a list of tuples
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return results
                
        except Exception as e:
            print(f"Error in cleanerFilterHistory: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return []

 
    @staticmethod
    def viewCompletedServiceForHomeowner(userid):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT h.historyid, a.username, s.servicename, c.categoryname, s.price, h.startdate, h.enddate
                FROM historyrecord h
                INNER JOIN service s on h.serviceid = s.serviceid
                INNER JOIN account a on h.cleanerid = a.userid
                INNER JOIN category c on s.categoryid = c.categoryid
                WHERE h.homeownerid = %s
            """,(userid,))
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()

            return ResultSet

        except Exception as e:
            print("Error fetching shortlisted cleaner accounts:", e)
            return None
 


    @staticmethod
    def searchCompletedServiceForHomeowner(userid, service, date): #main
        #search only
        if service and not date:
            try:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT h.historyid, a.username, s.servicename, c.categoryname, s.price, h.startdate, h.enddate
                    FROM historyrecord h
                    INNER JOIN service s on h.serviceid = s.serviceid
                    INNER JOIN account a on h.cleanerid = a.userid
                    INNER JOIN category c on s.categoryid = c.categoryid
                    WHERE h.homeownerid = %s AND s.servicename ILIKE %s
                """, (userid, f"%{service}%"))
                
                ResultSet = cur.fetchall()
                cur.close()
                conn.close()

                return ResultSet
            except Exception as e:
                print("Error displaying cleaner accounts:", e)
                return None
        #date only
        elif not service and date:
            # Tokenize and convert to proper format for SQL (YYYY-MM-DD)
            start_str, end_str = [d.strip() for d in date.split('-')]
            start_date = datetime.strptime(start_str, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_str, "%m/%d/%Y").date()

            try:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT h.historyid, a.username, s.servicename, c.categoryname, s.price, h.startdate, h.enddate
                    FROM historyrecord h
                    INNER JOIN service s ON h.serviceid = s.serviceid
                    INNER JOIN account a ON h.cleanerid = a.userid
                    INNER JOIN category c ON s.categoryid = c.categoryid
                    WHERE h.homeownerid = %s AND h.startdate >= %s AND h.enddate <= %s;
                """, (userid, start_date, end_date))
                
                ResultSet = cur.fetchall()
                cur.close()
                conn.close()

                return ResultSet
            except Exception as e:
                print("Error displaying cleaner accounts:", e)
                return None
        #both 
        elif service and date:
            # Tokenize and convert to proper format for SQL (YYYY-MM-DD)
            start_str, end_str = [d.strip() for d in date.split('-')]
            start_date = datetime.strptime(start_str, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_str, "%m/%d/%Y").date()

            try:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT h.historyid, a.username, s.servicename, c.categoryname, s.price, h.startdate, h.enddate
                    FROM historyrecord h
                    INNER JOIN service s ON h.serviceid = s.serviceid
                    INNER JOIN account a ON h.cleanerid = a.userid
                    INNER JOIN category c ON s.categoryid = c.categoryid
                    WHERE h.homeownerid = %s AND s.servicename ILIKE %s AND h.startdate >= %s AND h.enddate <= %s;
                """, (userid, f"%{service}%", start_date, end_date))
                
                ResultSet = cur.fetchall()
                cur.close()
                conn.close()

                return ResultSet
            except Exception as e:
                print("Error displaying cleaner accounts:", e)
                return None 
        