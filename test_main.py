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
    assert p.name
    assert p.surname
    assert p.age
    assert p.job
    assert not p.isDead