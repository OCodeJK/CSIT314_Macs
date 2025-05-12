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
    def get_by_id(serviceId):
        """Get a service by ID"""
        conn = db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            SELECT * FROM service 
            WHERE serviceId = %s
            """,
            (serviceId,)
        )
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return result
    
    @staticmethod
    def getServiceName(cleanerId):
        """Get all services for a specific cleaner"""
        conn = db_connection()
        cur = conn.cursor()
        cleanerId = str(cleanerId)
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
        """Update a cleaner's service details and create a history record"""
        if not serviceId or not serviceName or not cleanerId or not categoryId:
            return False

        conn = db_connection()
        cur = conn.cursor()

        try:
            # Update the service
            cur.execute(
                """
                UPDATE service
                SET serviceName = %s, categoryId = %s
                WHERE serviceId = %s
                """,
                (serviceName, categoryId, serviceId)
            )

        
            cur.execute(
                """
                INSERT INTO historyrecord (cleanerId, serviceId, startDate, endDate, homeownerid)
                VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE, %s)
                """,
                (cleanerId, serviceId, 22)  
            )
            
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
            results = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return results
            
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
        
        # If no exact matches and the query has spaces, try word-by-word search
        if not results and ' ' in searchQuery:
            # Split the search term into words
            search_words = searchQuery.split()
            # Create conditions for each word (they must all match)
            conditions = []
            params = [cleanerId]
            
            for word in search_words:
                conditions.append("serviceName ILIKE %s")
                params.append(f"%{word}%")
            
            # Combine all conditions with AND
            condition_str = " AND ".join(conditions)
            
            # Build and execute the query
            query = f"""
                SELECT * FROM service
                WHERE cleanerId = %s
                AND {condition_str}
                ORDER BY serviceName
            """
            
            cur.execute(query, params)
            results = cur.fetchall()
            
        # If still no results, use a partial match
        elif not results:
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
            
        cur.close()
        conn.close()
        
        return results
    
    @staticmethod
    def checkCategoryExists(categoryId):
        """Check if a category exists in the database"""
        conn = db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            SELECT COUNT(*) FROM category 
            WHERE categoryId = %s
            """,
            (categoryId,)
        )
        
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return count > 0
    
    @staticmethod
    def viewServiceForHomeowner():
        """Display all services with cleaner and category information"""
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.serviceid, s.servicename, a.username, c.categoryname, s.price
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
    def incViewCount(serviceid):
        #check to see if serviceid exist in serviceviews table
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM serviceviews
            WHERE serviceid = %s
        """,(serviceid,))
        ResultSet = cur.fetchall()
        cur.close()
        conn.close()

        #create new column for serviceid if serviceid does not exist in table
        if not ResultSet:
            try:
                conn = db_connection()
                cur = conn.cursor()
                    
                cur.execute("INSERT INTO serviceviews (serviceid, viewcount) VALUES (%s, %s)"
                            , (serviceid, 1))
                    
                conn.commit()
                        
                return True
            except Exception as e:
                print("DB Error1:", e)
                conn.rollback()
                return False
            finally:
                cur.close()
                conn.close()

        #increase viewcount if serviceid exists
        elif ResultSet:
            try:
                conn = db_connection()
                cur = conn.cursor()
                    
                cur.execute("UPDATE serviceviews SET viewcount = viewcount + 1 WHERE serviceid = %s"
                            , (serviceid,))
                    
                conn.commit()
                        
                return True
            except Exception as e:
                print("DB Error2:", e)
                conn.rollback()
                return False
            finally:
                cur.close()
                conn.close()