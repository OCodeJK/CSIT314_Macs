from entity.category import Category

class PMCreateServCatController:
    def __init__(self):
        # No parameters needed; entity manages DB connection internally
        pass

    def CreateServCat(self, category_name: str) -> str:
        if not category_name or not category_name.strip():
            return "Failed to create service category: Name required"

        category_entity = Category()

        if category_entity.checkServCatExists(category_name):
            return "Failed to create service category"

        if category_entity.CreateServCat(category_name):
            return "Service category created successfully"

        return "Failed to create service category"