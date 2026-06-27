class Workout:
    def __init__(self, name):
        self.name = name
        self.exercises = []

    def add_exercise(self, exercise, sets, reps, note):
        self.exercises.append({"Exercise": exercise.get_name(), "Sets": sets, "Reps": reps, "Note": note})