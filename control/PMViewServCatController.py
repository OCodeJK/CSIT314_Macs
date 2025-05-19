from entity.Category import Category

class PMViewServCatController:
    def __init__(self):
        self.entity = Category()

    def SearchServCat(self, category_name: str = ""):
        return self.entity.SearchServCat(category_name)