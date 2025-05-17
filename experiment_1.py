#Some name
#For now, Tram dilemma

import threading
import time

class People():
    def __init__(self):
        pass
    def isDead(self):
        return True

class Volunteer(People):
    pass

class Passenger(People):
    pass

class Tram():
    def __init__(self):
        pass

class Problem():
    def __init__(self, name, tr_left, tr_right, description=None, time = 10):
        self.name = name
        self.tr_left = tr_left
        self.tr_right = tr_right
        self.description = description
        self.time = time
        self._timer = None
        self._choice = None

    def _time(self):
        if self._choice is None:
            print("You were thinking for too long")
            print("The tram has already passed the lever")
            self._choice = "not pull"

    def play(self):
        print(self.description)

        self._startTime = time.monotonic()
        self._timer = threading.Timer(self.time, self._time)
        self._timer.start()

        self._choice = input("What will you do? Pull or not pull or ...? ").strip().lower()
        self._timer.cancel()
        endTime = time.monotonic() - self._startTime
        remainingTime = self.time - endTime

        result = ProblemResult(self._choice, self.tr_left, self.tr_right, remainingTime)
        result.consequence()

class ProblemResult(Problem):
    def __init__(self, choice, tr_left, tr_right, remainingTime):
        self.choice = choice
        self.tr_left = tr_left
        self.tr_right = tr_right
        self.remainingTime = remainingTime

    def consequence(self):
        match self.choice:
            case "pull":
                if 0 < self.remainingTime < 3:
                    print("You have pulled the lever exactly between front and back wheels")
                    time.sleep(2)
                    print("The tram has fallent on its side")
                    time.sleep(2)
                    print('Killing all "valunteers" and passengers')
                else:
                    print("You have pulled the lever")
                    time.sleep(2)
                    print("The tram has changed its route")
                    time.sleep(2)
                    print("The tram has killed", self.tr_right, "valunteers")
            case "not pull" | "not":
                print("You desided not to pull the lever")
                time.sleep(2)
                print("The tram has not changed its route")
                time.sleep(2)
                print("The tram has killed", self.tr_left, "valunteers")
            case "run" | "run away":
                print("You decided to run away")
                time.sleep(2)
                print("The tram has not changed its route")
                time.sleep(2)
                print(self.tr_left, "valunteers still died")
                time.sleep(2)
                print("But you got scared and ran away")
                time.sleep(2)
                print("It's ok")
                time.sleep(2)
                print("You are not a bad person")
                time.sleep(2)
                print("It's not your fault")
                time.sleep(2)
                print("You are not responsible for the deaths of", self.tr_left,"valunteers")
                time.sleep(2)
                print("It's some psycho that tied them to the rails")
                time.sleep(2)
                print("Not you")
            case _:
                print("Sorry, didn't g")
        
    

classic = Problem(
        name="Classic",
        tr_left=3,
        tr_right=1,
        description=(
            "You are standing next to a lever that controls a tram.\n"
            "If you do nothing it will hit 3 people on the left track.\n"
            "Pulling the lever diverts it onto a track where 1 person is tied.\n"
        ),
        time=10
    )
classic.play()