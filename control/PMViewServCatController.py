from entity.ServiceCategory import ServiceCategory

class PMViewServCatController:
    def __init__(self):
        self.entity = ServiceCategory()

    def SearchServCat(self, category_name: str = ""):
        return self.entity.SearchServCat(category_name)