#Some name
#For now, Tram dilemma

import threading

class People():
    def __init__(self):
        pass
    def isDead(self):
        pass

class Volunteer(People):
    pass

class Passenger(People):
    pass

class Tram():
    def __init__(self):
        pass

class Problem():
    def __init__(self, name, tr_left, tr_right, description=None, user_input=["pull", "not pull"]):
        self.name = name
        self.tr_left = tr_left
        self.tr_right = tr_right
        self.description = description

    def play(self):
        print(self.description)
        threading.Timer(10, timer)        
        choice = input("What will you do? ").strip().lower()
        # if choice in self.user_input:
        #     match choice:
        #         case "pull":
        #             print("You desided to pull the lever")
        #             print("The tram has changed its route")
        #             print()

class ProblemResult(Problem):
    def __init__(self):
        pass


def timer():
    pass