import psycopg2
from db_config import db_connection

class Category:
    def checkServCatExists(self, category_name: str) -> bool:
        """
        Check if a service category with the given name exists (case-insensitive).
        """
        query = """
            SELECT 1 FROM public.category 
            WHERE LOWER(categoryname) = LOWER(%s)
        """
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (category_name,))
                return cur.fetchone() is not None

    def CreateServCat(self, category_name: str) -> bool:
        """
        Create a new service category with the given name.
        Returns True if successful, False otherwise.
        """
        insert_query = """
            INSERT INTO public.category (categoryname) VALUES (%s)
        """
        try:
            with db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (category_name,))
                conn.commit()
                return True
        except Exception as e:
            # Optionally log the exception e here
            return False
