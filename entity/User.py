from db_config import db_connection

class User:
    def ViewDailyReport(self, date_str):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT c.categoryname, hr.startdate::date AS record_date, COUNT(*) AS total_records
                    FROM historyrecord hr
                    JOIN service s ON hr.serviceid = s.serviceid
                    JOIN category c ON s.categoryid = c.categoryid
                    WHERE hr.startdate::date = %s
                    GROUP BY c.categoryname, hr.startdate::date
                    ORDER BY record_date;
                """
                cur.execute(query, (date_str,))
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def ViewWeeklyReport(self, year, week):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT c.categoryname, EXTRACT(YEAR FROM hr.startdate) AS year,
                        EXTRACT(WEEK FROM hr.startdate) AS week_number, COUNT(*) AS total_records
                    FROM historyrecord hr
                    JOIN service s ON hr.serviceid = s.serviceid
                    JOIN category c ON s.categoryid = c.categoryid
                    WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(WEEK FROM hr.startdate) = %s
                    GROUP BY c.categoryname, EXTRACT(YEAR FROM hr.startdate), EXTRACT(WEEK FROM hr.startdate)
                    ORDER BY year, week_number;
                """
                cur.execute(query, (year, week))
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def ViewMonthlyReport(self, year, month):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT c.categoryname, EXTRACT(YEAR FROM hr.startdate) AS year,
                        EXTRACT(MONTH FROM hr.startdate) AS month, COUNT(*) AS total_records
                    FROM historyrecord hr
                    JOIN service s ON hr.serviceid = s.serviceid
                    JOIN category c ON s.categoryid = c.categoryid
                    WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(MONTH FROM hr.startdate) = %s
                    GROUP BY c.categoryname, EXTRACT(YEAR FROM hr.startdate), EXTRACT(MONTH FROM hr.startdate)
                    ORDER BY year, month;
                """
                cur.execute(query, (year, month))
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
