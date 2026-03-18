"""Tests for Vairagya."""
from src.core import Vairagya
def test_init(): assert Vairagya().get_stats()["ops"] == 0
def test_op(): c = Vairagya(); c.manage(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Vairagya(); [c.manage() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Vairagya(); c.manage(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Vairagya(); r = c.manage(); assert r["service"] == "vairagya"
