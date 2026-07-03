class Microcycle:
    def __init__(self, week_index, length, workouts = None):
        self.week = week_index
        self.length = length
        self.workouts = workouts if workouts else [None * length]
    
    def __repr__(self):
        return f"<Microcycles {self.name}>"

    @classmethod
    def from_json(cls, data_dict):
        return cls(week_index=data_dict["week"], length=data_dict["length"], workouts=data_dict["workouts"])
    
    def to_json(self):
        return {
            "week": self.week,
            "length": self.length,
            "workouts": self.workouts
        }
        

    def add_workout(self, workout, day_index):
        self.workouts[day_index] = workout
