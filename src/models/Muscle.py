class Muscle:
    def __init__(self, name, categories):
        self.name = name
        self.categories = categories
    
    def __repr__(self):
        return f"<Muscle {self.name}>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(name=data_dict["name"], categories=data_dict["categories"])
    
    def to_json(self):
        return {"name": self.name, "categories": self.categories}
    
    def categories_to_string(self):
        categories = self.categories
        for category in categories:
            categories[categories.index(category)] = category.title().replace("_", " ")
        categories_string = ", ".join(categories)
        return categories_string

    @staticmethod
    def categories_to_list(categories_string):
        categories = categories_string.split(", ")
        for i in range(len(categories)):
            categories[i] = categories[i].lower().replace(" ", "_")
        return categories

    def add_category(self, category):
        self.categories.append(category)
        return True

    def get_name(self):
        return self.name
    def get_categories(self):
        return self.categories
    def set_categories(self, categories):
        self.categories = [category.lower().replace(" ", "_") for category in categories]
        return True