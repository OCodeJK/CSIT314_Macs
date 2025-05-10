from db_config import db_connection
from datetime import datetime

class Shortlist:
    def viewShortlistForHomeowner(userid):
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
    def searchShortlistForHomeowner(userid, servicename): #display all service of individual cleaner
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