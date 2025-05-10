from db_config import db_connection

class Report:
    # --- Service Existence Check (supports single or multiple) ---
    def services_exist(self, service_names):
        if isinstance(service_names, str):
            service_names = [service_names]
        if not service_names:
            return True, []
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT LOWER(servicename) FROM service WHERE LOWER(servicename) = ANY(%s)",
                    (list(map(str.lower, service_names)),)
                )
                found = [row[0] for row in cur.fetchall()]
        not_found = [name for name in map(str.lower, service_names) if name not in found]
        return len(not_found) == 0, not_found

    # --- Daily ---
    def ViewDailyReport(self, date_str):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT s.servicename, hr.startdate::date AS record_date, COUNT(*) AS total_records
                    FROM historyrecord hr
                    JOIN service s ON hr.serviceid = s.serviceid
                    WHERE hr.startdate::date = %s
                    GROUP BY s.servicename, hr.startdate::date
                    ORDER BY record_date;
                """
                cur.execute(query, (date_str,))
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def SearchDailyReport(self, date_str, service_names):
        if isinstance(service_names, str):
            service_names = [service_names]
        exists, not_found = self.services_exist(service_names)
        if not exists:
            return False, f"Input service(s) '{', '.join(not_found)}' not valid", None

        with db_connection() as conn:
            with conn.cursor() as cur:
                if len(service_names) == 1:
                    query = """
                        SELECT s.servicename, hr.startdate::date AS record_date, COUNT(*) AS total_records
                        FROM historyrecord hr
                        JOIN service s ON hr.serviceid = s.serviceid
                        WHERE hr.startdate::date = %s AND LOWER(s.servicename) = LOWER(%s)
                        GROUP BY s.servicename, hr.startdate::date
                        ORDER BY record_date;
                    """
                    cur.execute(query, (date_str, service_names[0]))
                else:
                    query = """
                        SELECT s.servicename, hr.startdate::date AS record_date, COUNT(*) AS total_records
                        FROM historyrecord hr
                        JOIN service s ON hr.serviceid = s.serviceid
                        WHERE hr.startdate::date = %s AND LOWER(s.servicename) = ANY(%s)
                        GROUP BY s.servicename, hr.startdate::date
                        ORDER BY record_date;
                    """
                    cur.execute(query, (date_str, [name.lower() for name in service_names]))
                columns = [desc[0] for desc in cur.description]
                data = [dict(zip(columns, row)) for row in cur.fetchall()]
                if not data:
                    return False, f"No reports for '{', '.join(service_names)}' found.", None
                return True, None, data

    # --- Weekly ---
    def ViewWeeklyReport(self, year, week):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT s.servicename, EXTRACT(YEAR FROM hr.startdate) AS year,
                        EXTRACT(WEEK FROM hr.startdate) AS week_number, COUNT(*) AS total_records
                    FROM historyrecord hr
                    JOIN service s ON hr.serviceid = s.serviceid
                    WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(WEEK FROM hr.startdate) = %s
                    GROUP BY s.servicename, EXTRACT(YEAR FROM hr.startdate), EXTRACT(WEEK FROM hr.startdate)
                    ORDER BY year, week_number;
                """
                cur.execute(query, (year, week))
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def SearchWeeklyReport(self, year, week, service_names):
        if isinstance(service_names, str):
            service_names = [service_names]
        exists, not_found = self.services_exist(service_names)
        if not exists:
            return False, f"Input service(s) '{', '.join(not_found)}' not valid", None

        with db_connection() as conn:
            with conn.cursor() as cur:
                if len(service_names) == 1:
                    query = """
                        SELECT s.servicename, EXTRACT(YEAR FROM hr.startdate) AS year,
                            EXTRACT(WEEK FROM hr.startdate) AS week_number, COUNT(*) AS total_records
                        FROM historyrecord hr
                        JOIN service s ON hr.serviceid = s.serviceid
                        WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(WEEK FROM hr.startdate) = %s
                            AND LOWER(s.servicename) = LOWER(%s)
                        GROUP BY s.servicename, EXTRACT(YEAR FROM hr.startdate), EXTRACT(WEEK FROM hr.startdate)
                        ORDER BY year, week_number;
                    """
                    cur.execute(query, (year, week, service_names[0]))
                else:
                    query = """
                        SELECT s.servicename, EXTRACT(YEAR FROM hr.startdate) AS year,
                            EXTRACT(WEEK FROM hr.startdate) AS week_number, COUNT(*) AS total_records
                        FROM historyrecord hr
                        JOIN service s ON hr.serviceid = s.serviceid
                        WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(WEEK FROM hr.startdate) = %s
                            AND LOWER(s.servicename) = ANY(%s)
                        GROUP BY s.servicename, EXTRACT(YEAR FROM hr.startdate), EXTRACT(WEEK FROM hr.startdate)
                        ORDER BY year, week_number;
                    """
                    cur.execute(query, (year, week, [name.lower() for name in service_names]))
                columns = [desc[0] for desc in cur.description]
                data = [dict(zip(columns, row)) for row in cur.fetchall()]
                if not data:
                    return False, f"No reports for '{', '.join(service_names)}' found.", None
                return True, None, data

    # --- Monthly ---
    def ViewMonthlyReport(self, year, month):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT s.servicename, EXTRACT(YEAR FROM hr.startdate) AS year,
                        EXTRACT(MONTH FROM hr.startdate) AS month, COUNT(*) AS total_records
                    FROM historyrecord hr
                    JOIN service s ON hr.serviceid = s.serviceid
                    WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(MONTH FROM hr.startdate) = %s
                    GROUP BY s.servicename, EXTRACT(YEAR FROM hr.startdate), EXTRACT(MONTH FROM hr.startdate)
                    ORDER BY year, month;
                """
                cur.execute(query, (year, month))
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def SearchMonthlyReport(self, year, month, service_names):
        if isinstance(service_names, str):
            service_names = [service_names]
        exists, not_found = self.services_exist(service_names)
        if not exists:
            return False, f"Input service(s) '{', '.join(not_found)}' not valid", None

        with db_connection() as conn:
            with conn.cursor() as cur:
                if len(service_names) == 1:
                    query = """
                        SELECT s.servicename, EXTRACT(YEAR FROM hr.startdate) AS year,
                            EXTRACT(MONTH FROM hr.startdate) AS month, COUNT(*) AS total_records
                        FROM historyrecord hr
                        JOIN service s ON hr.serviceid = s.serviceid
                        WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(MONTH FROM hr.startdate) = %s
                            AND LOWER(s.servicename) = LOWER(%s)
                        GROUP BY s.servicename, EXTRACT(YEAR FROM hr.startdate), EXTRACT(MONTH FROM hr.startdate)
                        ORDER BY year, month;
                    """
                    cur.execute(query, (year, month, service_names[0]))
                else:
                    query = """
                        SELECT s.servicename, EXTRACT(YEAR FROM hr.startdate) AS year,
                            EXTRACT(MONTH FROM hr.startdate) AS month, COUNT(*) AS total_records
                        FROM historyrecord hr
                        JOIN service s ON hr.serviceid = s.serviceid
                        WHERE EXTRACT(YEAR FROM hr.startdate) = %s AND EXTRACT(MONTH FROM hr.startdate) = %s
                            AND LOWER(s.servicename) = ANY(%s)
                        GROUP BY s.servicename, EXTRACT(YEAR FROM hr.startdate), EXTRACT(MONTH FROM hr.startdate)
                        ORDER BY year, month;
                    """
                    cur.execute(query, (year, month, [name.lower() for name in service_names]))
                columns = [desc[0] for desc in cur.description]
                data = [dict(zip(columns, row)) for row in cur.fetchall()]
                if not data:
                    return False, f"No reports for '{', '.join(service_names)}' found.", None
                return True, None, data

    def get_all_services(self):
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT servicename FROM service ORDER BY servicename;")
                return [row[0] for row in cur.fetchall()]
