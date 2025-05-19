from entity.Category import Category

class PMUpdateServCatController:
    def __init__(self):
        self.entity = Category()

    def UpdateServCat(self, category_id: int, new_name: str):
        return self.entity.UpdateServCat(category_id, new_name)

