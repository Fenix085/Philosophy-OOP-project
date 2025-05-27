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

class Volunteer(Person):
    @classmethod
    def generate(cls):
        name = random.choice(cls._nameList)
        surname = random.choice(cls._surnameList)
        age = random.choice(cls._ageList)
        job = random.choice(cls._jobList)
        return cls(name, surname, age, job)

class Passenger(Person):
    @classmethod
    def generate(self):
        name = random.choice(self._nameList)
        surname = random.choice(self._surnameList)
        age = random.choice(self._ageList)
        job = random.choice(self._jobList)
        return self(name, surname, age, job)
    
def generatePeople(n, cls):
    return [cls.generate() for _ in range(n)]

class Tram():
    def __init__(self):
        pass
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
        cntr = 0
        for person in self.result.leftTrack + self.result.rightTrack + self.result.passengers:
            if person.isDead == True:
                print(f"{person.name} {person.surname} ({person.age}, {person.job}) died in result of you actions")
                time.sleep(1)
                cntr += 1
        if cntr == 0:
            print("No one died in result of your actions")
            time.sleep(1)
            return
        cntr = 0
        print("But")
        for person in self.result.leftTrack + self.result.rightTrack + self.result.passengers:
            if person.isDead == False:
                print(f"{person.name} {person.surname} ({person.age}, {person.job}) survived and can come back to their families")
                time.sleep(1)
                cntr += 1
        if cntr == 0:
            print("No one survived in result of your actions")
            time.sleep(1)
            return
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
            print("Sorry, didn't get that")
            syn_found = "not pull"

        mapping = {
            "pull": self._pull,
            "not pull": self._notPull,
            "run": self._run
        }
        mapping[syn_found]()

    def _pull(self):
        if 0 < self.result.remainingTime < 3:
            print("You have pulled the lever exactly between front and back wheels")
            time.sleep(2)
            print("The tram has fallent on its side")
            time.sleep(2)
            print("Killing all 'valunteers' and passengers")
            for person in self.result.leftTrack:
                person.death()
            for person in self.result.rightTrack:
                person.death()
            for person in self.result.passengers:
                person.death()
        else:
            print("You have pulled the lever")
            time.sleep(2)
            print("The tram has changed its route")
            time.sleep(2)
            print("The tram has killed", self.result.tr_right, "valunteers")
            for person in self.result.rightTrack:
                person.death()
            

    def _notPull(self):
        print("You desided not to pull the lever")
        time.sleep(2)
        print("The tram has not changed its route")
        time.sleep(2)
        print("The tram has killed", self.result.tr_left, "valunteers")
        for person in self.result.leftTrack:
            person.death()

    def _run(self):
        print("You decided to run away")
        time.sleep(2)
        print("The tram has not changed its route")
        time.sleep(2)
        print(self.result.tr_left, "valunteers still died")
        for person in self.result.leftTrack:
            person.death()
        time.sleep(2)
        print("But you got scared and ran away")
        time.sleep(2)
        print("It's ok")
        time.sleep(2)
        print("You are not a bad person")
        time.sleep(2)
        print("It's not your fault")
        time.sleep(2)
        print("You are not responsible for the deaths of", self.result.tr_left,"valunteers")
        time.sleep(2)
        print("It's some psycho that tied them to the rails")
        time.sleep(2)
        print("Not you")

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
            print("Sorry, didn't get that")
            syn_found = "not push"

        mapping = {
            "run": self._run,
            "push": self._push,
            "not push": self._notPush
        }
        mapping[syn_found]()
        
    def _run(self):
        print("You decided to run away")
        time.sleep(2)
        print("The tram is not going to stop")
        time.sleep(2)
        print("The tram is going right to kill all those people")
        time.sleep(2)
        if random.random() < 0.9:
            print("The guy next to also got scared")
            time.sleep(2)
            print("He just stayed there in shock")
            #bla bla bla
            for person in self.result.leftTrack:
                person.death()
        else:
            print("Oh wait")
            time.sleep(1)
            print("The guy next to decided to stop the tram")
            time.sleep(0.75)
            print("He jumps in front of the tram")
            time.sleep(0.75)
            print("He is so fat that he stopped the tram!")
            time.sleep(2)
            print("All", self.result.tr_left, "valunteers are saved thanks to him")
            time.sleep(2)
            print("But unfortunately")
            time.sleep(2)
            print("The day hasn't beed without a loss")
            time.sleep(2)
            print("The guy died on the spot")
            self.fatGuy.death()
            time.sleep(2)
            print("But he will be remembered as a hero")

    def _push(self):
        print("You decided to push the guy in front of the tram")
        time.sleep(2)
        print("The tram hits him and stops")
        time.sleep(2)
        print("All", self.result.tr_left, "valunteers are saved thanks to his absolutely own decision to sacrifice himself")
        for person in self.result.leftTrack:
            person.death()
        time.sleep(2)
        print("But because the tram was going so fast")
        time.sleep(0.75)
        print("And it stopped so suddenly")
        time.sleep(0.75)
        print("Passengers also had a hard time surviving")
        time.sleep(0.75)
        randnumb = random.randint(1, self.result.numbOfPsngrs)
        print("Unfortunately, ",randnumb , "passengers died")
        i = 0
        while i < randnumb:
            self.result.passengers[i].death()
            i += 1
        
        time.sleep(2)

    def _notPush(self):
        print("you have not pushed the guy") #bla bla bla, later !!!!!!DO NOT FORGET!!!!!!
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