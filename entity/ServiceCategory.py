import psycopg2
from db_config import db_connection

class ServiceCategory:
    def SearchServCat(self, category_name: str = ""):
        with db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT categoryid, categoryname, suspend 
                    FROM public.category 
                    WHERE LOWER(categoryname) LIKE LOWER(%s)
                    ORDER BY categoryid
                """
                cur.execute(query, (f'%{category_name.lower()}%',))
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                return results if results else None  # Return None if no results

    def UpdateServCat(self, category_id: int, new_name: str) -> bool:
        """
        Updates the name of a service category.
        Returns True if update is successful, False otherwise.
        """
        if not new_name or not new_name.strip():
            return False  # Invalid name

        try:
            with db_connection() as conn:
                with conn.cursor() as cur:
                    # Check for duplicate name
                    cur.execute(
                        "SELECT 1 FROM public.category WHERE LOWER(categoryname) = LOWER(%s) AND categoryid != %s",
                        (new_name, category_id)
                    )
                    if cur.fetchone():
                        return False  # Duplicate name

                    cur.execute(
                        "UPDATE public.category SET categoryname = %s WHERE categoryid = %s",
                        (new_name, category_id)
                    )
                conn.commit()
                return cur.rowcount == 1
        except Exception as e:
            # Optionally log e
            return False

    def SuspendServCat(self, category_id: int, suspend: bool) -> bool:
        """
        Sets the suspend flag for a category.
        If suspend=True, suspends the category; if False, unsuspends.
        Returns True if successful, False otherwise.
        """
        try:
            with db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE public.category SET suspend = %s WHERE categoryid = %s",
                        (suspend, category_id)
                    )
                conn.commit()
                return cur.rowcount == 1
        except Exception as e:
            # Optionally log e
            return False

    def GetCategoryById(self, category_id: int):
        """
        Fetch a single category by its ID.
        """
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT categoryid, categoryname, suspend FROM public.category WHERE categoryid = %s",
                    (category_id,)
                )
                row = cur.fetchone()
                if row:
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, row))
                return None
