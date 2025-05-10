from db_config import db_connection

class Service:
    def __init__(self, serviceId=None, serviceName=None, categoryId=None, cleanerId=None, price=None):
        self.serviceId = serviceId
        self.serviceName = serviceName
        self.categoryId = categoryId
        self.cleanerId = cleanerId
        self.price = price
    
    @staticmethod
    def get_all():
        with ConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM service")
            services = cursor.fetchall()
            return services
    
    @staticmethod
    def get_available_services():
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT * FROM service 
                WHERE cleanerId IS NULL OR cleanerId = ''
                """
            )
            services = cursor.fetchall()
            return services
    
    @staticmethod
    def get_by_id(serviceId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT * FROM service 
                WHERE serviceId = %s
                """,
                (serviceId,)
            )
            service = cursor.fetchone()
            return service

    @staticmethod
    def viewServiceForHomeowner(): #display all service
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
    def searchServiceForHomeowner(servicename): #display all service of individual cleaner
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
            