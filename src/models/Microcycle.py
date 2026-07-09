class Microcycle:
    def __init__(self, microcycle_id, week_index, length, workouts = None, note = ""):
        self.id = microcycle_id
        self.week = week_index
        self.length = length
        self.workouts = workouts if workouts else [None for _ in range(length)]
        self.note = note
    
    def __repr__(self):
        return f"<Microcycle {self.id}>"

    @classmethod
    def from_json(cls, data_dict, workout_map):
        workout_names = data_dict["workouts"]
        workouts = [(workout_map[name] if name else None) for name in workout_names]
        return cls(microcycle_id=data_dict["id"], week_index=data_dict["week"], length=data_dict["length"], workouts=workouts, note=data_dict["note"])
    
    def to_json(self):
        return {
            "id": self.id,
            "week": self.week,
            "length": self.length,
            "workouts": self.normalize_workouts(self.workouts),
            "note": self.note
        }

    def normalize_workouts(self, workouts):
        for i in range(len(workouts)):
            workout = workouts[i]
            if workout:
                workouts[i] = workout.get_name()
        return workouts

    def clear_workouts(self):
        self.workouts = [None for _ in range(self.length)]
        return True

    def get_muscle_sets(self):
        muscle_sets = {}
        for workout in self.workouts:
            if workout:
                muscle_sets.update(workout.get_muscle_sets(muscle_sets))
        return muscle_sets

    def set_workout(self, workout, day_index):
        self.workouts[day_index] = workout
    def set_note(self, note):
        self.note = note

    def get_id(self):
        return self.id
    def get_workouts(self):
        return self.workouts
    def get_note(self):
        return self.note