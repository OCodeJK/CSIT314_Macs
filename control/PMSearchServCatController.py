from entity.category import Category

class PMSearchServCatController:
    def __init__(self):
        self.entity = Category()

    def SearchServCat(self, category_name: str = ""):
        return self.entity.SearchServCat(category_name)
