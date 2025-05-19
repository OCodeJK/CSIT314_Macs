from entity.Category import Category

class PMCreateServCatController:
    def __init__(self):
        # No parameters needed; entity manages DB connection internally
        pass

    def CreateServCat(self, category_name: str):
        category_entity = Category()
        # Let the entity handle all logic and just return its result
        return category_entity.CreateServCat(category_name)
