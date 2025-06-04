import pytest
from main import *

@pytest.fixture(autouse=True)
def deterministic_random(monkeypatch):
    """Freeze RNG so tests are repeatable."""
    monkeypatch.setattr(random, "random", lambda: 0.42)
    monkeypatch.setattr(random, "randint", lambda a, b: a)  # always lowest

def test_random_returns_person():
    p = Person.generate()
    assert isinstance(p, Person)
    assert isinstance(p.name, str)
    assert isinstance(p.surname, str)
    assert isinstance(p.age, int)
    assert isinstance(p.job, str)
    assert isinstance(p.isDead, bool)

def test_death():
    p = Person.generate()
    assert not p.isDead
    p.death()
    assert p.isDead

def test_track_generation_counts_and_types_Classic():
    n_left = 3
    n_right = 1
    n_pass = 5

    testProblem = Problem(
        name="Test Problem",
        levelID="test1",
        style="classic",
        tr_left=n_left,
        tr_right=n_right,
        numbOfPsngrs=n_pass,
        time = 1,
    )
    assert len(testProblem.leftTrack) == n_left
    assert len(testProblem.rightTrack) == n_right
    assert len(testProblem.passengers) == n_pass

    assert all(isinstance(p, Volunteer) for p in testProblem.leftTrack)
    assert all(isinstance(p, Volunteer) for p in testProblem.rightTrack)
    assert all(isinstance(p, Passenger) for p in testProblem.passengers)

    ids = {id(p) for p in (testProblem.leftTrack + testProblem.rightTrack + testProblem.passengers)}
    assert len(ids) == n_left + n_right + n_pass

def test_track_generation_counts_and_types_AllZero():
    n_left = 0
    n_right = 0
    n_pass = 0

    testProblem = Problem(
        name="Test Problem",
        levelID="test2",
        style="classic",
        tr_left=n_left,
        tr_right=n_right,
        numbOfPsngrs=n_pass,
        time = 1,
    )
    assert len(testProblem.leftTrack) == n_left
    assert len(testProblem.rightTrack) == n_right
    assert len(testProblem.passengers) == n_pass

    assert all(isinstance(p, Volunteer) for p in testProblem.leftTrack)
    assert all(isinstance(p, Volunteer) for p in testProblem.rightTrack)
    assert all(isinstance(p, Passenger) for p in testProblem.passengers)

    ids = {id(p) for p in (testProblem.leftTrack + testProblem.rightTrack + testProblem.passengers)}
    assert len(ids) == n_left + n_right + n_pass

def test_track_generation_counts_and_types_BigNumbers():
    n_left = 300
    n_right = 1
    n_pass = 5000

    testProblem = Problem(
        name="Test Problem",
        levelID="test3",
        style="classic",
        tr_left=n_left,
        tr_right=n_right,
        numbOfPsngrs=n_pass,
        time = 1,
    )
    assert len(testProblem.leftTrack) == n_left
    assert len(testProblem.rightTrack) == n_right
    assert len(testProblem.passengers) == n_pass

    assert all(isinstance(p, Volunteer) for p in testProblem.leftTrack)
    assert all(isinstance(p, Volunteer) for p in testProblem.rightTrack)
    assert all(isinstance(p, Passenger) for p in testProblem.passengers)

    ids = {id(p) for p in (testProblem.leftTrack + testProblem.rightTrack + testProblem.passengers)}
    assert len(ids) == n_left + n_right + n_pass