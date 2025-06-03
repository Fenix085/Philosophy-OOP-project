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