#Some name
#For now, Tram dilemma

import threading
import time
from dataclasses import dataclass
from typing import Dict, Type
from abc import ABC, abstractmethod
import random
#---------------------------------------------
class Person():
    _nameList = ["John", "Rowland", "Vivian", "Alfred", "Martha", "Dick", "George", "Gustaw", "Iwona", "Katarzyna", "Peter", "Amanda", "Carmen", "Ola"]
    _surnameList = ["Wong", "Smith", "Johnson", "Brown", "Weiß", "Müller", "Frank", "Tomczak", "Kowalski", "Wolf", "Russell", "Sturm", "Heintze", "Bower"]
    _ageList = [i for i in range(26, 65)]
    _jobList = ["Wildlife rehabilitator", "Data analyst", "Drone operator", "Sommelier", "Solar panel installer", "UX writer", "Stunt coordinator", "Urban beekeeper", "Voice-over artist", "Culinary scientist", "Genetic counselor", "Museum registrar", "Bicycle courier", "Sound engineer", "Comedy scriptwriter", "Ethical hacker", "Toy designer", "Hydrologist", "Yoga therapist", "E-sports coach"]

    def __init__(self, name, surname, age, job):
        self.name = name
        self.surname = surname
        self.age = age
        self.job = job
        self.isDead = False

    def death(self):
        self.isDead = True

    @classmethod
    def generate(cls):
        name = random.choice(cls._nameList)
        surname = random.choice(cls._surnameList)
        age = random.choice(cls._ageList)
        job = random.choice(cls._jobList)
        return cls(name, surname, age, job)

class Volunteer(Person):
    pass

class Passenger(Person):
    pass
    
def generatePeople(n, cls):
    return [cls.generate() for _ in range(n)]

# class Tram():
#     def __init__(self):
#         pass
#--------------------------------------------
@dataclass
class ProblemResult:
    choice: str
    tr_left: int
    leftTrack: list
    tr_right: int
    rightTrack: list
    numbOfPsngrs: int
    passengers: list
    remainingTime: float
#--------------------------------------------
class EpilogueWriter():
    def __init__(self, result: ProblemResult):
        self.result = result
    
    def write(self):
        everyone = self.result.leftTrack + self.result.rightTrack + self.result.passengers
        for person in everyone:
            if person.isDead == True:
                scribe_expecta(f"{person.name} {person.surname} ({person.age}, {person.job}) died in result of your actions", 1.5)
            else:
                scribe_expecta(f"{person.name} {person.surname} ({person.age}, {person.job}) survived and can come back to their families", 1.5)
#--------------------------------------------
class Problem():
    registry: Dict[str, "Problem"] = {}

    def __init__(self, *,name, levelID, style, tr_left, tr_right = 0, numbOfPsngrs, description=None, time = 10, writer_cls=EpilogueWriter):
        self.name = name
        self.levelID = str(levelID)
        self.style = style
        self.tr_left = tr_left
        self.tr_right = tr_right
        self.numbOfPsngrs = numbOfPsngrs
        self.description = description
        self.time = time
        self._timer = None
        self._choice = None
        self.leftTrack = (generatePeople(self.tr_left, Volunteer))
        self.rightTrack = (generatePeople(self.tr_right, Volunteer))
        self.passengers = (generatePeople(self.numbOfPsngrs, Passenger))
        self.writer_cls = writer_cls

        if self.levelID in Problem.registry:
            raise ValueError("Duplicate levelID", self.levelID)
        Problem.registry[self.levelID] = self

    def _time(self):
        if self._choice is None:
            print("You were thinking for too long")
            print("The tram has already passed the lever")
            self._choice = "not pull"

    def play(self):
        print("You are playing", self.name)
        print()
        print(self.description)
        print()

        self._startTime = time.monotonic()
        self._timer = threading.Timer(self.time, self._time)
        self._timer.start()

        self._choice = input("What will you do? Pull or not pull or ...? ").strip().lower()
        self._timer.cancel()
        endTime = time.monotonic() - self._startTime
        remainingTime = self.time - endTime

        result = ProblemResult(self._choice, self.tr_left, self.leftTrack, self.tr_right, self.rightTrack, self.numbOfPsngrs, self.passengers, remainingTime)

        chosenCls = CONSEQUENCE_STYLES[self.style]
        chosenCls(result).consequence()

        self.writer_cls(result).write() 
    
    @classmethod
    def get(cls, levelID) -> "Problem":
        return cls.registry[levelID]
#--------------------------------------------
def scribe_expecta(line = "", delay = 0.0):
    print(line)
    time.sleep(delay)
#---------------------------------------------


class Consequence(ABC):
    def __init__(self, result: ProblemResult):
        self.result = result

    @abstractmethod
    def consequence(self):
        pass

class ClassicConsequence(Consequence):

    _synonims = {
        "pull": ["pull", "pull the lever"],
        "not pull": ["not pull", "not", "not pull the lever"],
        "run": ["run", "run away"]
    }

    def consequence(self):
        syn_found = None
        for syn, synonyms in self._synonims.items():
            if self.result.choice in synonyms:
                syn_found = syn
                break

        if syn_found is None:
            scribe_expecta("Sorry, didn't get that")
            syn_found = "not pull"

        mapping = {
            "pull": self._pull,
            "not pull": self._notPull,
            "run": self._run
        }
        mapping[syn_found]()

    def _pull(self):
        if 0 < self.result.remainingTime < 3:
            scribe_expecta("You have pulled the lever exactly between front and back wheels", 2)
            scribe_expecta("The tram has fallent on its side", 2)
            scribe_expecta("Killing all 'valunteers' and passengers")
            for person in self.result.leftTrack:
                person.death()
            for person in self.result.rightTrack:
                person.death()
            for person in self.result.passengers:
                person.death()
        else:
            scribe_expecta("You have pulled the lever", 2)
            scribe_expecta("The tram has changed its route", 2)
            scribe_expecta(f"The tram has killed {self.result.tr_left} valunteers")
            for person in self.result.rightTrack:
                person.death()
            

    def _notPull(self):
        scribe_expecta("You desided not to pull the lever", 2)
        scribe_expecta("The tram has not changed its route", 2)
        scribe_expecta(f"The tram has killed {self.result.tr_left} valunteers")
        for person in self.result.leftTrack:
            person.death()

    def _run(self):
        scribe_expecta("You decided to run away", 2)
        scribe_expecta("The tram has not changed its route", 2)
        scribe_expecta(f"{self.result.tr_left} valunteers still died", 2)
        for person in self.result.leftTrack:
            person.death()
        scribe_expecta("But you got scared and ran away", 2)
        scribe_expecta("It's ok", 2)
        scribe_expecta("You are not a bad person", 2)
        scribe_expecta("It's not your fault", 2)
        scribe_expecta(f"You are not responsible for the deaths of {self.result.tr_left} valunteers", 2)
        scribe_expecta("It's some psycho that tied them to the rails", 2)
        scribe_expecta("Not you", 5)

class FatManConsequence(Consequence):

    _synonims = {
        "pull": ["pull", "pull the lever"],
        "not pull": ["not pull", "not pull the lever"],
        "run": ["run", "run away"],
        "push": ["push"],
        "not push": ["not push", "not"],
    }

    fatGuy = Person("Fat", "Guy", 45, "Fat Guy")

    def consequence(self):
        syn_found = None
        for syn, synonyms in self._synonims.items():
            if self.result.choice in synonyms:
                syn_found = syn
                break

        if syn_found is None:
            scribe_expecta("Sorry, didn't get that")
            syn_found = "not push"

        mapping = {
            "run": self._run,
            "push": self._push,
            "not push": self._notPush
        }
        mapping[syn_found]()
        
    def _run(self):
        scribe_expecta("You decided to run away", 2)
        scribe_expecta("The tram is not going to stop", 2)
        scribe_expecta("The tram is going right to kill all those people", 2)
        if random.random() < 0.9:
            scribe_expecta("The guy next to also got scared", 2)
            scribe_expecta("He just stayed there in shock", 2)
            #bla bla bla
            for person in self.result.leftTrack:
                person.death()
        else:
            scribe_expecta("Oh wait", 1)
            scribe_expecta("The guy next to decided to stop the tram", 0.75)
            scribe_expecta("He jumps in front of the tram", 0.75)
            scribe_expecta("He is so fat that he stopped the tram!", 2)
            scribe_expecta(f"All {self.result.tr_left} valunteers are saved thanks to him", 2)
            scribe_expecta("But unfortunately", 2)
            scribe_expecta("The day hasn't beed without a loss", 2)
            scribe_expecta("The guy died on the spot", 2)
            self.fatGuy.death()
            scribe_expecta("But he will be remembered as a hero", 5)

    def _push(self):
        scribe_expecta("You decided to push the guy in front of the tram", 2)
        scribe_expecta("The tram hits him and stops", 2)
        scribe_expecta(f"All {self.result.tr_left} valunteers are saved thanks to his absolutely own decision to sacrifice himself", 2)
        for person in self.result.leftTrack:
            person.death()
        scribe_expecta("But because the tram was going so fast", 0.75)
        scribe_expecta("And it stopped so suddenly", 0.75)
        scribe_expecta("Passengers also had a hard time surviving", 0.75)
        randnumb = random.randint(1, self.result.numbOfPsngrs)
        scribe_expecta(f"Unfortunately, {randnumb} {" passengers " if randnumb != 1 else " passenger "} died")
        i = 0
        while i < randnumb:
            self.result.passengers[i].death()
            i += 1
        time.sleep(2)

    def _notPush(self):
        scribe_expecta("you have not pushed the guy") #bla bla bla, later !!!!!!DO NOT FORGET!!!!!!
        for person in self.result.leftTrack:
            person.death()

CONSEQUENCE_STYLES: Dict[str, Type[Consequence]] = {
    "classic": ClassicConsequence,
    "fatMan": FatManConsequence
 }
#--------------------------------------------
classic = Problem(
        name="Classic",
        levelID=1,
        style="classic",
        numbOfPsngrs=5,
        tr_left=3,
        tr_right=1,
        description=(
            "You are standing next to a lever that controls a tram.\n"
            "If you do nothing it will hit 3 people on the left track.\n"
            "Pulling the lever diverts it onto a track where 1 person is tied.\n"
        ),
        time=10
    )
fatMan = Problem(
        name="The Fat Man",
        levelID="fat",
        style="fatMan",
        numbOfPsngrs=5,
        tr_left=3,
        tr_right=0,
        description=(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In non cursus urna.\n"
            "Ut sed rutrum velit. Vestibulum sit amet gravida urna. Maecenas accumsan justo quis nibh pharetra semper.\n"
            "Donec turpis nec."
        ),
        time=10
    )

classic.play()
fatMan.play()