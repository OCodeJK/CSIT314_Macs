from db_config import db_connection
from datetime import datetime

class HistoryRecord:
    def __init__(self, cleanerId=None, serviceId=None, startDate=None, endDate=None):
        self.cleanerId = cleanerId
        self.serviceId = serviceId
        self.startDate = startDate
        self.endDate = endDate
    
    @staticmethod
    def create_record(cleanerId, serviceId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                INSERT INTO history_record (cleanerId, serviceId, startDate, endDate)
                VALUES (%s, %s, %s, NULL)
                """,
                (cleanerId, serviceId, datetime.now().date())
            )
            return True
    
    @staticmethod
    def end_service(cleanerId, serviceId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                UPDATE history_record 
                SET endDate = %s 
                WHERE cleanerId = %s AND serviceId = %s AND endDate IS NULL
                """,
                (datetime.now().date(), cleanerId, serviceId)
            )
            return True
    
    @staticmethod
    def get_history(cleanerId):
        with ConnectionFromPool() as cursor:
            cursor.execute(
                """
                SELECT hr.*, s.serviceName 
                FROM history_record hr
                JOIN service s ON hr.serviceId = s.serviceId
                WHERE hr.cleanerId = %s
                ORDER BY hr.startDate DESC
                """,
                (cleanerId,)
            )
            history = cursor.fetchall()
            return history

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