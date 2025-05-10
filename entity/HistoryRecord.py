from db_config import db_connection
from datetime import datetime

class HistoryRecord:
    """
    Entity class representing a history record in the database
    Provides data access methods for history-related operations
    """
    def __init__(self, id=None, serviceId=None, startDate=None, endDate=None, cleanerId=None):
        """Initialize a new HistoryRecord instance"""
        self.id = id
        self.serviceId = serviceId
        self.startDate = startDate
        self.endDate = endDate
        self.cleanerId = cleanerId
    
    @staticmethod
    def create_record(cleanerId, serviceId):
        """Create a new history record for a service"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            cleanerId = str(cleanerId)
            
            cur.execute(
                """
                INSERT INTO historyrecord (cleanerId, serviceId, startDate, endDate)
                VALUES (%s, %s, %s, NULL)
                """,
                (cleanerId, serviceId, datetime.now().date())
            )
            
            conn.commit()
            cur.close()
            conn.close()
            
            return True
                
        except Exception as e:
            print(f"Error creating record: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return False
    
    @staticmethod
    def end_service(cleanerId, serviceId):
        """End an active service by setting the end date to current date"""
        try:
            # Get current date for the end date
            today = datetime.now().date()
            
            conn = db_connection()
            cur = conn.cursor()
            cleanerId = str(cleanerId)
            
            # Check if active history record exists
            cur.execute(
                "SELECT * FROM historyrecord WHERE cleanerId = %s AND serviceId = %s AND endDate IS NULL",
                (cleanerId, serviceId)
            )
            
            history = cur.fetchone()
            
            if history:
                # Update the end date
                cur.execute(
                    "UPDATE historyrecord SET endDate = %s WHERE cleanerId = %s AND serviceId = %s AND endDate IS NULL",
                    (today, cleanerId, serviceId)
                )
                
                conn.commit()
                cur.close()
                conn.close()
                return True
            else:
                cur.close()
                conn.close()
                return False
                
        except Exception as e:
            print(f"Error ending service: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return False
    
    @staticmethod
    def get_history(cleanerId):
        """Alias for get_cleaner_history"""
        return HistoryRecord.get_cleaner_history(cleanerId)
    
    @staticmethod
    def get_cleaner_history(cleanerId):
        """Get all history records for a specific cleaner"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            # Join with service to get service names
            cur.execute(
                """
                SELECT h.id, h.serviceId, h.startDate, h.endDate, h.cleanerId, s.serviceName 
                FROM historyrecord h
                LEFT JOIN service s ON h.serviceId = s.serviceId
                WHERE h.cleanerId = %s
                ORDER BY h.startDate DESC
                """,
                (cleanerId,)
            )
            
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return results
                
        except Exception as e:
            print(f"Error getting cleaner history: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return []
    
    @staticmethod
    def cleanerFilterHistory(cleanerId, startDate, endDate):
        """Filter history records by date range for a cleaner"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            # Complex query to handle different date scenarios
            cur.execute(
                """
                SELECT h.id, h.serviceId, h.startDate, h.endDate, h.cleanerId, s.serviceName 
                FROM historyrecord h
                LEFT JOIN service s ON h.serviceId = s.serviceId
                WHERE h.cleanerId = %s 
                AND (
                    (h.startDate BETWEEN %s AND %s) OR
                    (h.endDate BETWEEN %s AND %s) OR
                    (h.startDate <= %s AND (h.endDate IS NULL OR h.endDate >= %s))
                )
                ORDER BY h.startDate DESC
                """,
                (cleanerId, startDate, endDate, startDate, endDate, startDate, endDate)
            )
            
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return results
                
        except Exception as e:
            print(f"Error filtering history: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return []
    
    @staticmethod
    def getHistoryDetails(id, cleanerId):
        """Get detailed information about a specific history record"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            # Get record details
            cur.execute(
                """
                SELECT h.id, h.serviceId, h.startDate, h.endDate, h.cleanerId,
                       s.serviceName, s.categoryId, s.price 
                FROM historyrecord h
                LEFT JOIN service s ON h.serviceId = s.serviceId
                WHERE h.id = %s AND h.cleanerId = %s
                """,
                (id, cleanerId)
            )
            
            record = cur.fetchone()
            
            if record:
                # Get view count in separate query
                cur.execute(
                    """
                    SELECT viewcount 
                    FROM serviceviews 
                    WHERE serviceid = %s
                    """,
                    (record[1],)  # record[1] is serviceId
                )
                
                view_result = cur.fetchone()
                view_count = view_result[0] if view_result else 0
                
                cur.close()
                conn.close()
                
                # Return record with view count
                return record + (view_count,)
            else:
                cur.close()
                conn.close()
                return None
                
        except Exception as e:
            print(f"Error getting history details: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return None
    
    @staticmethod
    def cleanerVewConfirmedMatches(cleanerId: str) -> list:
        """View all active services (confirmed matches) for a cleaner"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            
            # Query to get active services (endDate is NULL)
            cur.execute(
                """
                SELECT h.id, h.serviceId, h.startDate, h.endDate, h.cleanerId, s.serviceName 
                FROM historyrecord h
                JOIN service s ON h.serviceId = s.serviceId
                WHERE h.cleanerId = %s 
                AND h.endDate IS NULL
                ORDER BY h.startDate DESC
                """, 
                (cleanerId,)
            )
            
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return results
                
        except Exception as e:
            print(f"Error getting confirmed matches: {e}")
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return []
    
    @staticmethod
    def getAllHistory(cleanerId):
        """Alias for get_cleaner_history"""
        return HistoryRecord.get_cleaner_history(cleanerId)
    
    @staticmethod
    def searchService(searchName, cleanerId):
        """
        Search for services by name in a cleaner's history
        
        Args:
            searchName (str): The name or partial name to search for (case-insensitive)
            cleanerId (str): The ID of the cleaner
            
        Returns:
            list: List of service records matching the search criteria
        """
        try:
            # Print debug info
            print(f"Searching for '{searchName}' for cleaner {cleanerId}")
            
            # If the search string is empty, return all records
            if not searchName or searchName.strip() == "":
                return HistoryRecord.get_cleaner_history(cleanerId)
            
            conn = db_connection()
            cur = conn.cursor()
            
            # Use ILIKE for case-insensitive matching with wildcards to find partial matches
            cur.execute(
                """
                SELECT h.id, h.serviceId, h.startDate, h.endDate, h.cleanerId, s.serviceName 
                FROM historyrecord h
                JOIN service s ON h.serviceId = s.serviceId
                WHERE h.cleanerId = %s 
                AND s.serviceName ILIKE %s
                ORDER BY h.startDate DESC
                """,
                (cleanerId, f"%{searchName}%")
            )
            
            results = cur.fetchall()
            print(f"ILIKE search results: {len(results)} records found")
            
            cur.close()
            conn.close()
            
            return results
                
        except Exception as e:
            print(f"Error searching service: {e}")
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
        