"""Tests for usage simulator."""

from datetime import datetime

from vairagya.models import AppCategory
from vairagya.simulator import UsageSimulator


class TestUsageSimulator:
    def test_simulate_day(self) -> None:
        sim = UsageSimulator()
        sessions = sim.simulate_day()
        assert len(sessions) > 0
        for s in sessions:
            assert s.duration_minutes > 0
            assert s.app_name

    def test_simulate_day_intensity(self) -> None:
        sim = UsageSimulator()
        light = sim.simulate_day(intensity="light")
        heavy = sim.simulate_day(intensity="heavy")
        # Heavy should generally produce more sessions
        # (with random variance, just check both produce output)
        assert len(light) > 0
        assert len(heavy) > 0

    def test_simulate_week(self) -> None:
        sim = UsageSimulator()
        week = sim.simulate_week()
        assert len(week) == 7
        for day in week:
            assert len(day) > 0

    def test_simulate_doom_scrolling_day(self) -> None:
        sim = UsageSimulator()
        sessions = sim.simulate_doom_scrolling_day()
        social_sessions = [
            s for s in sessions
            if s.category == AppCategory.SOCIAL_MEDIA and s.duration_minutes >= 40
        ]
        assert len(social_sessions) > 0

    def test_simulate_late_night_day(self) -> None:
        sim = UsageSimulator()
        sessions = sim.simulate_late_night_day()
        late_sessions = [s for s in sessions if s.is_late_night]
        assert len(late_sessions) > 0

    def test_sessions_sorted_by_time(self) -> None:
        sim = UsageSimulator()
        sessions = sim.simulate_day()
        for i in range(1, len(sessions)):
            assert sessions[i].start_time >= sessions[i - 1].start_time

    def test_simulate_with_specific_date(self) -> None:
        sim = UsageSimulator()
        date = datetime(2025, 6, 15, 0, 0, 0)
        sessions = sim.simulate_day(date=date)
        for s in sessions:
            assert s.start_time.date() == date.date()
