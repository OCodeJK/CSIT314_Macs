from entity.Category import Category

class PMCreateServCatController:
    def CreateServCat(self, category_name: str):
        return Category.CreateServCat(category_name)
