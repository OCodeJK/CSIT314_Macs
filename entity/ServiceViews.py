from db_config import db_connection

class ServiceViews:
    
    @staticmethod
    def getViewCount(cleanerId, serviceId=None):
        
        conn = db_connection()
        cur = conn.cursor()
        cleanerId = str(cleanerId)
        try:
            if serviceId:
                # Get view count for specific service
                cur.execute(
                    """
                    SELECT sv.viewcount 
                    FROM serviceviews sv
                    JOIN service s ON sv.serviceid = s.serviceid
                    WHERE s.cleanerid = %s AND s.serviceid = %s
                    """,
                    (cleanerId, serviceId)
                )
            else:
                # Get total views for all services of the cleaner
                cur.execute(
                    """
                    SELECT SUM(sv.viewcount) 
                    FROM serviceviews sv
                    JOIN service s ON sv.serviceid = s.serviceid
                    WHERE s.cleanerid = %s
                    """,
                    (cleanerId,)
                )
                
            result = cur.fetchone()
            return result[0] if result and result[0] else 0
                
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def increment_view_count(serviceId):
        conn = db_connection()
        cur = conn.cursor()
        
        try:
            # Check if a view record exists
            cur.execute(
                "SELECT viewcount FROM serviceviews WHERE serviceid = %s",
                (serviceId,)
            )
            
            if cur.fetchone():
                # Update existing record
                cur.execute(
                    "UPDATE serviceviews SET viewcount = viewcount + 1 WHERE serviceid = %s",
                    (serviceId,)
                )
            else:
                # Create new record
                cur.execute(
                    "INSERT INTO serviceviews (serviceid, viewcount) VALUES (%s, 1)",
                    (serviceId,)
                )
                
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error incrementing view count: {e}")
            conn.rollback()
            return False
            
        finally:
            cur.close()
            conn.close()