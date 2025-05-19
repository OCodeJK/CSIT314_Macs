from entity.Category import Category

class PMUpdateServCatController:
    def UpdateServCat(self, category_id: int, new_name: str):
        return Category.UpdateServCat(category_id, new_name)

