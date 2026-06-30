from src.models.Exercise import Exercise

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
                "note": exercise_data["note"]
            } for exercise_data in exercises_data]
        return cls(name=data_dict["name"], exercises = exercises)

    def add_exercise(self, exercise, sets, reps, note):
        self.exercises.append({"exercise": exercise.get_name(), "sets": sets, "reps": reps, "note": note})

if __name__ == '__main__':
    workout_data = {
        "name": "Bench",
        "exercises": [{
                "exercise": "bench_press",
                "sets": 3,
                "reps": "5-8",
                "note": "Al fallo"},
            {
                "exercise": "deadlift",
                "sets": 2,
                "reps": "1",
                "note": "PR"    
            }]
    }
    
    exercise_map = {"bench_press": Exercise("bench_press", ["pec"], ["triceps", "shoulder"]), "deadlift": Exercise("deadlift", ["hamstrings", "lower_back"], ["quadriceps", "traps"])}
    workout = Workout.from_json(workout_data, exercise_map)
    print(workout.exercises)