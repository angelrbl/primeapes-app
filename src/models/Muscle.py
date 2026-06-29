from src.utils.files import check_file
import json

class Muscle:
    def __init__(self, name, categories = []):
        self.name = name
        self.categories = categories
    
    def __repr__(self):
        return f"<Muscle {self.name}>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(name=data_dict["name"], categories=data_dict["categories"])
    
    def to_json(self):
        return {"name": self.name, "categories": self.categories}
    
    @classmethod
    def from_name(self, name, user):
        MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
        with open(MUSCLES_FILE, "r") as f:
            muscles_data = json.load(f)
        for muscle_data in muscles_data:
            if muscle_data["name"] == name:
                return Muscle.from_json(muscle_data)
        return None

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

    @staticmethod
    def to_list(muscle_list):
        muscle_names = []
        for muscle in muscle_list:
            muscle_names.append(muscle.get_name())
        return muscle_names
    
    @staticmethod
    def get_name_list(user):
        MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
        muscle_list = []
        with open(MUSCLES_FILE, "r") as f:
            muscles_data = json.load(f)
        for muscle in muscles_data:
            muscle_list.append(Muscle.from_json(muscle))
        return muscle_list

    @staticmethod
    def list_to_obj(muscle_name_list, user):
        muscle_list = []
        for muscle_name in muscle_name_list:
            muscle = Muscle.from_name(muscle_name, user)
            if muscle:
                muscle_list.append(muscle)
        return muscle_list

    def get_name(self):
        return self.name
    def get_categories(self):
        return self.categories
    def set_categories(self, categories):
        self.categories = [category.lower().replace(" ", "_") for category in categories]
        return True
    

# INTRODUZCO UNA LISTA DE NOMBRES DE MUSCULOS
# RECIBO UNA LISTA DE OBJETOS DE MUSCULOS