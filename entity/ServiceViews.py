from db_config import db_connection

class ServiceViews:
    
    @staticmethod
    def getViewCount(cleanerId, serviceId):
        
        conn = db_connection()
        cur = conn.cursor()
        cleanerId = int(cleanerId)
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
    
