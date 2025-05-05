from db_config import db_connection
from datetime import datetime

class Shortlist:
    @staticmethod
    def viewShortlistForHomeowner(userid):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.cleanerid, a.username, s.serviceid, s.servicename, c.categoryname, s.price
                FROM service s
                INNER JOIN account a on s.cleanerid = a.userid
                INNER JOIN category c on s.categoryid = c.categoryid
                INNER JOIN shortlist sl on s.cleanerid = sl.cleanerid
                WHERE sl.homeownerid = %s
            """,(userid,))
            shortlist = cur.fetchall()
            cur.close()
            conn.close()

            ResultSet = {}
            for cleaner in shortlist:
                cleanerid = cleaner[0]
                serviceid = cleaner[2]
                service_data = cleaner[2:]  # (serviceid, servicename, categoryname, price)

                if cleanerid not in ResultSet:
                    # Start a new inner dict for services per cleaner
                    ResultSet[cleanerid] = {
                        "cleanerid": cleaner[0],
                        "cleanername": cleaner[1],
                        "services": {}
                    }

                ResultSet[cleanerid]["services"][serviceid] = service_data


            return ResultSet
        except Exception as e:
            print("Error fetching shortlisted cleaner accounts:", e)
            return None

    @staticmethod
    def searchShortlistForHomeowner(userid, cleaneruser): #display all service of individual cleaner
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.cleanerid, a.username, s.serviceid, s.servicename, c.categoryname, s.price
                FROM service s
                INNER JOIN account a on s.cleanerid = a.userid
                INNER JOIN category c on s.categoryid = c.categoryid
                INNER JOIN shortlist sl on s.cleanerid = sl.cleanerid
                WHERE sl.homeownerid = %s AND a.username ILIKE %s
            """, (userid, f"%{cleaneruser}%"))
            
            shortlist = cur.fetchall()
            cur.close()
            conn.close()

            ResultSet = {}
            for cleaner in shortlist:
                cleanerid = cleaner[0]
                serviceid = cleaner[2]
                service_data = cleaner[2:]  # (serviceid, servicename, categoryname, price)

                if cleanerid not in ResultSet:
                    # Start a new inner dict for services per cleaner
                    ResultSet[cleanerid] = {
                        "cleanerid": cleaner[0],
                        "cleanername": cleaner[1],
                        "services": {}
                    }

                ResultSet[cleanerid]["services"][serviceid] = service_data

            return ResultSet
        except Exception as e:
            print("Error displaying cleaner accounts:", e)
            return None 

    @staticmethod
    def createShortlistForHomeowner(cleanerid, homeownerid):
        try:
            conn = db_connection()
            cur = conn.cursor()
                
            cur.execute("INSERT INTO shortlist (cleanerid, homeownerid) VALUES (%s, %s)"
                        , (cleanerid, homeownerid))
                
            conn.commit()
                    
            return True
        except Exception as e:
            print("DB Error:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()