from src.models.Muscle import Muscle

class Workout:
    def __init__(self, name, exercises = []):
        self.name = name
        self.exercises = exercises

    def __repr__(self):
        return f"<Workout {self.name}>"

    @classmethod
    def from_json(cls, data_dict, exercise_map):
        exercises_data = [exercise for exercise in data_dict["exercises"]]
        exercises = [{
                "exercise": exercise_map[exercise_data["exercise"]],
                "sets": exercise_data["sets"],
                "reps": exercise_data["reps"],
                "muscles": exercise_map[exercise_data["exercise"]].get_primary_muscles(),
                "note": exercise_data["note"]
            } for exercise_data in exercises_data]
        return cls(name=data_dict["name"], exercises = exercises)

    def to_json(self):
        return {
            "name": self.name,
            "exercises": [{
                    "exercise": exercise["exercise"].get_name(),
                    "sets": exercise["sets"],
                    "reps": exercise["reps"],
                    "muscles": Muscle.to_name_list(exercise["muscles"]),
                    "note": exercise["note"]
                } for exercise in self.exercises]
        }

    def get_muscle_sets(self, muscle_sets={}):
        for exercise in self.exercises:
            for muscle in exercise["muscles"]:
                muscle_name = muscle.get_name().replace("_", " ").title()
                if muscle_sets.get(muscle_name):
                    muscle_sets[muscle_name] += exercise["sets"]
                else:
                    muscle_sets[muscle_name] = exercise["sets"]
            secondary_muscles = exercise["exercise"].get_secondary_muscles()
            for muscle in secondary_muscles:
                muscle_name = muscle.get_name().replace("_", " ").title()
                if muscle_sets.get(muscle_name):
                    muscle_sets[muscle_name] += exercise["sets"] * 0.5
                else:
                    muscle_sets[muscle_name] = exercise["sets"] * 0.5
        return muscle_sets

    def add_exercise(self, exercise, sets, reps, note):
        self.exercises.append({"exercise": exercise, "sets": sets, "reps": reps, "muscles": exercise.get_primary_muscles(), "note": note})

    def get_name(self):
        return self.name

    def get_exercises(self):
        return self.exercises
    
    def set_exercises(self, exercises):
        self.exercises = exercises

    @staticmethod
    def get_exercise_stat_value(exercise, stat):
        value = exercise[stat]
        if value is None:
            return 0
        
        if stat == "reps" and type(value) == str:
            digits = [int(x) for x in value.split("-")]
            return sum(digits) // len(digits) if digits else 0
        if type(value) == int:
            return value
        return 1

    @staticmethod
    def exercise_from_json(exercise_map, exercise_data=None):
        return {
            "exercise": exercise_map[exercise_data["exercise"]],
            "sets": exercise_data["sets"],
            "reps": exercise_data["reps"],
            "muscles": exercise_map[exercise_data["exercise"]].get_primary_muscles(),
            "note": exercise_data["note"]
        }

    @staticmethod
    def to_name_list(workouts_list):
        workout_names = []
        for workout in workouts_list:
            workout_names.append(workout.get_name())
        return workout_names