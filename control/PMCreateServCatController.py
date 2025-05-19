from entity.Category import Category

class PMCreateServCatController:
    def __init__(self):
        self.entity = Category()

    def CreateServCat(self, category_name: str):
        return self.entity.CreateServCat(category_name)
