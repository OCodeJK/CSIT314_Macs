from db_config import db_connection
from datetime import datetime

class CompletedService:
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
    def searchCompletedServiceForHomeowner(userid, service): 
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
            
            completedservice = cur.fetchall()
            cur.close()
            conn.close()

            return completedservice
        except Exception as e:
            print("Error displaying cleaner accounts:", e)
            return None 

    @staticmethod
    def searchCompletedServiceForHomeownerDateOnly(userid, date): 
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT h.historyid, a.username, s.servicename, c.categoryname, s.price, h.startdate, h.enddate
                FROM historyrecord h
                INNER JOIN service s ON h.serviceid = s.serviceid
                INNER JOIN account a ON h.cleanerid = a.userid
                INNER JOIN category c ON s.categoryid = c.categoryid
                WHERE h.homeownerid = %s AND %s::date BETWEEN h.startdate AND h.enddate;
            """, (userid, date))
            
            completedservice = cur.fetchall()
            cur.close()
            conn.close()

            return completedservice
        except Exception as e:
            print("Error displaying cleaner accounts:", e)
            return None 

    @staticmethod
    def searchCompletedServiceForHomeownerSearchNDate(userid, service, date): 
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT h.historyid, a.username, s.servicename, c.categoryname, s.price, h.startdate, h.enddate
                FROM historyrecord h
                INNER JOIN service s ON h.serviceid = s.serviceid
                INNER JOIN account a ON h.cleanerid = a.userid
                INNER JOIN category c ON s.categoryid = c.categoryid
                WHERE h.homeownerid = %s AND s.servicename ILIKE %s AND %s::date BETWEEN h.startdate AND h.enddate;
            """, (userid, f"%{service}%", date))
            
            completedservice = cur.fetchall()
            cur.close()
            conn.close()

            return completedservice
        except Exception as e:
            print("Error displaying cleaner accounts:", e)
            return None 