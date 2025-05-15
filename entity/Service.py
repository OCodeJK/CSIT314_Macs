from db_config import db_connection
from datetime import datetime

class Service:
    """Entity class representing a Service in the system"""
    
    def __init__(self, serviceId=None, serviceName=None, categoryId=None, cleanerId=None, price=None, suspend=False):
        """Initialize a new Service instance"""
        self.serviceId = serviceId
        self.serviceName = serviceName
        self.categoryId = categoryId
        self.cleanerId = cleanerId
        self.price = price
        self.suspend = suspend if suspend is not None else False
    
    @staticmethod
    def getServiceName(cleanerId):
        """Get all services for a specific cleaner"""
        conn = db_connection()
        cur = conn.cursor()
        cleanerId = cleanerId
        cur.execute(
            """
            SELECT s.serviceId, s.serviceName, s.categoryId, s.cleanerId, s.price, s.suspend
            FROM service s
            WHERE s.cleanerId = %s
            """,
            (cleanerId,)
        )
        
        result = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return result
    
    @staticmethod
    def createService(serviceId, cleanerId):
        """Assign an available service to a cleaner and create a history record"""
        conn = db_connection()
        cur = conn.cursor()
        
        # Check if service is available
        cur.execute(
            """
            SELECT * FROM service 
            WHERE serviceId = %s AND (cleanerId IS NULL)
            """,
            (serviceId,)
        )
        
        if not cur.fetchone():
            print(f"Service {serviceId} is not available")
            cur.close()
            conn.close()
            return False
            
        # Assign service to cleaner
        cur.execute(
            """
            UPDATE service
            SET cleanerId = %s
            WHERE serviceId = %s
            """,
            (cleanerId, serviceId)
        )
        
        # Create history record
        cur.execute(
            """
            INSERT INTO historyrecord (cleanerId, serviceId, startDate)
            VALUES (%s, %s, CURRENT_DATE)
            """,
            (cleanerId, serviceId)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return True
        
    @staticmethod
    def cleanerSuspendService(cleanerId, serviceId):

        conn = db_connection()
        cur = conn.cursor()
        
        # Check if the service belongs to the cleaner and is not already suspended
        cur.execute(
            """
            SELECT * FROM service 
            WHERE serviceId = %s AND cleanerId = %s AND suspend = FALSE
            """,
            (serviceId, cleanerId)
        )
        
        service = cur.fetchone()
        if not service:
            print(f"Service {serviceId} does not belong to cleaner {cleanerId} or is already suspended")
            cur.close()
            conn.close()
            return False
            
        # Update the service to suspended status
        cur.execute(
            """
            UPDATE service
            SET suspend = TRUE
            WHERE serviceId = %s
            """,
            (serviceId,)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return True
    
    @staticmethod
    def updateCleanerService(serviceId, serviceName, cleanerId, categoryId):
        """Update a cleaner's service details - only updates name and category ID"""
        conn = db_connection()
        cur = conn.cursor()
        
        try:
            # First check if the service belongs to the cleaner
            cur.execute(
                """
                SELECT cleanerId FROM service
                WHERE serviceId = %s
                """,
                (serviceId,)
            )
            
            result = cur.fetchone()
            if not result:
                print(f"Service {serviceId} not found")
                cur.close()
                conn.close()
                return False
            
            if result[0] != cleanerId:
                print(f"Service {serviceId} does not belong to cleaner {cleanerId}")
                cur.close()
                conn.close()
                return False
            
            # Update the service
            cur.execute(
                """
                UPDATE service
                SET serviceName = %s, categoryId = %s
                WHERE serviceId = %s
                """,
                (serviceName, categoryId, serviceId)
            )
            
            if cur.rowcount == 0:
                print(f"No rows affected when updating service {serviceId}")
                conn.rollback()
                cur.close()
                conn.close()
                return False
                        
            conn.commit()
            cur.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error in updateCleanerService: {str(e)}")
            conn.rollback()
            cur.close()
            conn.close()
            return False
            
    @staticmethod
    def getServices(cleanerId, searchQuery):
        """Search for services by name for a specific cleaner"""
        conn = db_connection()
        cur = conn.cursor()
        
        try:
            # If search query is empty, return all services for the cleaner
            if not searchQuery or searchQuery.strip() == "":
                cur.execute(
                    """
                    SELECT * FROM service
                    WHERE cleanerId = %s
                    ORDER BY serviceName
                    """,
                    (cleanerId,)
                )
            else:
                # First try exact match
                cur.execute(
                    """
                    SELECT * FROM service
                    WHERE cleanerId = %s
                    AND serviceName = %s
                    ORDER BY serviceName
                    """,
                    (cleanerId, searchQuery)
                )
                
                results = cur.fetchall()
                
                # If no results, use a partial match
                if not results:
                    cur.execute(
                        """
                        SELECT * FROM service
                        WHERE cleanerId = %s
                        AND serviceName ILIKE %s
                        ORDER BY serviceName
                        """,
                        (cleanerId, f"%{searchQuery}%")
                    )
                    results = cur.fetchall()
                
                return results
            
            # This line will only be reached when searchQuery is empty
            results = cur.fetchall()
            return results
            
        finally:
            cur.close()
            conn.close()
        

    @staticmethod
    def searchServiceForHomeowner(servicename):
        """Search services by name for homeowners"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.serviceid, s.servicename, a.username, c.categoryname, s.price
                FROM service s
                INNER JOIN account a ON s.cleanerid = a.userid
                INNER JOIN category c ON s.categoryid = c.categoryid
                WHERE s.servicename ILIKE %s
            """, (f"%{servicename}%",))
            ResultSet = cur.fetchall()
            cur.close()
            conn.close()

            return ResultSet
        except Exception as e:
            print("Error displaying cleaner accounts:", e)
            return None
        
    @staticmethod
    def viewServiceForHomeowner(serviceid):
        #check to see if serviceid exist in serviceviews table
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM serviceviews
            WHERE serviceid = %s
        """,(serviceid,))
        ResultSet1 = cur.fetchall()
        cur.close()
        conn.close()

        #create new column for serviceid if serviceid does not exist in table
        if not ResultSet1:
            try:
                conn = db_connection()
                cur = conn.cursor()
                    
                cur.execute("INSERT INTO serviceviews (serviceid, viewcount) VALUES (%s, %s)"
                            , (serviceid, 1))
                    
                conn.commit()
                cur.execute("""
                    SELECT s.serviceid, s.servicename, a.username, c.categoryname, s.price
                    FROM service s
                    INNER JOIN account a ON s.cleanerid = a.userid
                    INNER JOIN category c ON s.categoryid = c.categoryid
                    WHERE s.serviceid = %s
                """, (serviceid,))
                ResultSet = cur.fetchall()

                ResultSet = [] #return nothing
                        
                return ResultSet
            except Exception as e:
                print("DB Error1:", e)
                conn.rollback()
                return ResultSet
            finally:
                cur.close()
                conn.close()

        #increase viewcount if serviceid exists
        elif ResultSet1:
            try:
                conn = db_connection()
                cur = conn.cursor()
                    
                cur.execute("UPDATE serviceviews SET viewcount = viewcount + 1 WHERE serviceid = %s"
                            , (serviceid,))
                    
                conn.commit()

                cur.execute("""
                    SELECT s.serviceid, s.servicename, a.username, c.categoryname, s.price
                    FROM service s
                    INNER JOIN account a ON s.cleanerid = a.userid
                    INNER JOIN category c ON s.categoryid = c.categoryid
                    WHERE s.serviceid = %s
                """, (serviceid,))
                ResultSet = cur.fetchall()
                        
                return ResultSet
            except Exception as e:
                print("DB Error2:", e)
                conn.rollback()
                return ResultSet
            finally:
                cur.close()
                conn.close()