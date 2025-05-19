from entity.Category import Category

class PMSuspendServCatController:
    def __init__(self):
        self.entity = Category()

    def SuspendServCat(self, category_id: int, suspend: bool):
        return self.entity.SuspendServCat(category_id, suspend)


