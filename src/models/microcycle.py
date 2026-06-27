class Microcycle:
    def __init__(self, week_index, length):
        self.week = week_index
        self.length = length
        self.workouts = [None * length]
    
    def add_workout(self, workout, day_index):
        self.workouts[day_index] = workout