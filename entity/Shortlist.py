from db_config import db_connection
from datetime import datetime

class Shortlist:
    """Entity class for managing shortlisted services"""
    
    def __init__(self, id=None, cleanerId=None, homeownerId=None, serviceId=None):
        """Initialize a new Shortlist instance"""
        self.id = id
        self.cleanerId = cleanerId
        self.homeownerId = homeownerId
        self.serviceId = serviceId
    
    @staticmethod
    def numberOfShortlistedTime(cleanerId, serviceId=None):
        """Count how many times a cleaner's service has been shortlisted"""
        try:
            # Establish database connection
            conn = db_connection()
            cur = conn.cursor()
            cleanerId = str(cleanerId)
            
            if serviceId:
                # Count shortlists for specific service
                cur.execute(
                    """
                    SELECT COUNT(*) 
                    FROM shortlist sl
                    JOIN service s ON sl.serviceid = s.serviceid
                    WHERE s.cleanerid = %s AND sl.serviceid = %s
                    """,
                    (cleanerId, serviceId)
                )
            else:
                # Count all shortlists for the cleaner
                cur.execute(
                    """
                    SELECT COUNT(*) 
                    FROM shortlist sl
                    JOIN service s ON sl.serviceid = s.serviceid
                    WHERE s.cleanerid = %s
                    """,
                    (cleanerId,)
                )
            
            result = cur.fetchone()
            
            # Close cursor and connection
            cur.close()
            conn.close()
            
            return result[0] if result else 0
                
        except Exception as e:
            print(f"Error in numberOfShortlistedTime: {str(e)}")
            # Ensure connection is closed even if an error occurs
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            return 0
    
    
    @staticmethod
    def viewShortlistForHomeowner(userid):
        """Get all shortlisted services for a homeowner"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.servicename, a.username, c.categoryname, s.price
                FROM service s
                INNER JOIN account a on s.cleanerid = a.userid
                INNER JOIN category c on s.categoryid = c.categoryid
                INNER JOIN shortlist sl on s.serviceid = sl.serviceid
                WHERE sl.homeownerid = %s
            """,(userid,))
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()

            return ResultSet
        except Exception as e:
            print("Error fetching shortlisted cleaner accounts:", e)
            return None

    @staticmethod
    def searchShortlistForHomeowner(userid, servicename):
        """Search shortlisted services by name for a homeowner"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.servicename, a.username, c.categoryname, s.price
                FROM service s
                INNER JOIN account a on s.cleanerid = a.userid
                INNER JOIN category c on s.categoryid = c.categoryid
                INNER JOIN shortlist sl on s.serviceid = sl.serviceid
                WHERE sl.homeownerid = %s AND s.servicename ILIKE %s
            """, (userid, f"%{servicename}%"))
            
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()

            return ResultSet
        except Exception as e:
            print("Error displaying cleaner accounts:", e)
            return None 

    @staticmethod
    def createShortlistForHomeowner(serviceid, homeownerid):
        """Add a service to homeowner's shortlist"""
        try:
            conn = db_connection()
            cur = conn.cursor()
                
            cur.execute("INSERT INTO shortlist (serviceid, homeownerid) VALUES (%s, %s)"
                        , (serviceid, homeownerid))
                
            conn.commit()
                    
            return True
        except Exception as e:
            print("DB Error:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()