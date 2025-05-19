from entity.Category import Category

class PMViewServCatController:
    def SearchServCat(self, category_name: str = ""):
        return Category.SearchServCat(category_name)