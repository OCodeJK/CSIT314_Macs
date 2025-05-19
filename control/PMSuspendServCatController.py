from entity.Category import Category

class PMSuspendServCatController:
    def SuspendServCat(self, category_id: int, suspend: bool):
        return Category.SuspendServCat(category_id, suspend)


