from entity.category import Category

class PMUpdateServCatController:
    def __init__(self):
        self.entity = Category()

    def UpdateServCat(self, category_id: int, new_name: str) -> (bool, str):
        """
        Returns (success, message)
        """
        if not new_name or not new_name.strip():
            return False, "Invalid category name."
        
        updated = self.entity.UpdateServCat(category_id, new_name)
        if updated:
            return True, "Service Category updated successfully."
        else:
            return False, "Failed to update service category. The name may already exist or be invalid."

    def GetCategoryById(self, category_id: int):
        return self.entity.GetCategoryById(category_id)
