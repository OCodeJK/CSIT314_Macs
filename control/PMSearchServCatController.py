from entity.Category import Category

class PMSearchServCatController:
    def SearchServCat(self, category_name: str = ""):
        return Category.SearchServCat(category_name)
