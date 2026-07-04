class Microcycle:
    def __init__(self, microcycle_id, week_index, length, workouts = None):
        self.id = microcycle_id
        self.week = week_index
        self.length = length
        self.workouts = workouts if workouts else [None * length]
    
    def __repr__(self):
        return f"<Microcycle {self.name}>"

    @classmethod
    def from_json(cls, data_dict, workout_map):
        workout_names = data_dict["workouts"]
        workouts = [workout_map[name] for name in workout_names]
        return cls(microcycle_id=data_dict["id"], week_index=data_dict["week"], length=data_dict["length"], workouts=workouts)
    
    def to_json(self):
        return {
            "id": self.id,
            "week": self.week,
            "length": self.length,
            "workouts": self.workouts
        }

    def add_workout(self, workout, day_index):
        self.workouts[day_index] = workout

    def get_id(self):
        return self.id