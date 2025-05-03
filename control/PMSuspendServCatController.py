from entity.ServiceCategory import ServiceCategory

class PMSuspendServCatController:
    def __init__(self):
        self.entity = ServiceCategory()

    def SuspendServCat(self, category_id: int, suspend: bool) -> (bool, str):
        """
        Returns (success, message)
        """
        result = self.entity.SuspendServCat(category_id, suspend)
        if result:
            return True, (
                "Service Category unsuspended successfully."
                if not suspend else
                "Service Category suspended successfully."
            )
        else:
            return False, "Failed to update suspension status. Please try again."
