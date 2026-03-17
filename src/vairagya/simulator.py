"""Generate realistic simulated usage data for testing and demos."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from vairagya.models import AppCategory, UsageSession


class UsageSimulator:
    """Simulate realistic phone usage patterns for testing."""

    # Typical apps with their categories and average session durations
    APP_PROFILES: list[dict] = [
        {"name": "Instagram", "category": AppCategory.SOCIAL_MEDIA, "avg_min": 15, "sessions_day": 8},
        {"name": "TikTok", "category": AppCategory.SOCIAL_MEDIA, "avg_min": 25, "sessions_day": 5},
        {"name": "Twitter", "category": AppCategory.SOCIAL_MEDIA, "avg_min": 10, "sessions_day": 10},
        {"name": "Reddit", "category": AppCategory.SOCIAL_MEDIA, "avg_min": 20, "sessions_day": 4},
        {"name": "YouTube", "category": AppCategory.ENTERTAINMENT, "avg_min": 30, "sessions_day": 3},
        {"name": "Netflix", "category": AppCategory.ENTERTAINMENT, "avg_min": 60, "sessions_day": 1},
        {"name": "WhatsApp", "category": AppCategory.COMMUNICATION, "avg_min": 5, "sessions_day": 15},
        {"name": "Slack", "category": AppCategory.COMMUNICATION, "avg_min": 8, "sessions_day": 10},
        {"name": "Gmail", "category": AppCategory.COMMUNICATION, "avg_min": 3, "sessions_day": 8},
        {"name": "Chrome", "category": AppCategory.BROWSING, "avg_min": 10, "sessions_day": 6},
        {"name": "Apple News", "category": AppCategory.NEWS, "avg_min": 12, "sessions_day": 3},
        {"name": "Amazon", "category": AppCategory.SHOPPING, "avg_min": 8, "sessions_day": 2},
    ]

    # Hour-of-day usage probability weights (higher = more likely)
    HOURLY_WEIGHTS = {
        0: 0.1, 1: 0.05, 2: 0.02, 3: 0.01, 4: 0.01, 5: 0.02,
        6: 0.3, 7: 0.6, 8: 0.8, 9: 0.9, 10: 0.7, 11: 0.6,
        12: 0.8, 13: 0.7, 14: 0.6, 15: 0.5, 16: 0.6, 17: 0.7,
        18: 0.8, 19: 0.9, 20: 1.0, 21: 0.9, 22: 0.7, 23: 0.3,
    }

    def simulate_day(
        self,
        date: datetime | None = None,
        intensity: str = "moderate",
    ) -> list[UsageSession]:
        """Simulate one day of phone usage.

        Args:
            date: The date to simulate. Defaults to today.
            intensity: Usage intensity - "light", "moderate", or "heavy".
        """
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        multiplier = {"light": 0.5, "moderate": 1.0, "heavy": 1.8}.get(intensity, 1.0)
        sessions: list[UsageSession] = []

        for profile in self.APP_PROFILES:
            num_sessions = max(1, int(profile["sessions_day"] * multiplier * random.uniform(0.5, 1.5)))

            for _ in range(num_sessions):
                hour = self._pick_hour()
                minute = random.randint(0, 59)

                start = date.replace(hour=hour, minute=minute)
                duration = max(
                    1,
                    int(profile["avg_min"] * random.uniform(0.3, 2.5)),
                )
                end = start + timedelta(minutes=duration)

                # Don't extend past midnight
                midnight = date + timedelta(days=1)
                if end > midnight:
                    end = midnight - timedelta(minutes=1)
                    duration = (end - start).total_seconds() / 60

                notifications = random.randint(0, 10) if profile["category"] in {
                    AppCategory.SOCIAL_MEDIA,
                    AppCategory.COMMUNICATION,
                } else random.randint(0, 3)

                sessions.append(
                    UsageSession(
                        app_name=profile["name"],
                        category=profile["category"],
                        start_time=start,
                        end_time=end,
                        duration_minutes=round(max(1, duration), 1),
                        notifications_received=notifications,
                        pickups=random.randint(1, 3),
                    )
                )

        sessions.sort(key=lambda s: s.start_time)
        return sessions

    def simulate_week(
        self,
        start_date: datetime | None = None,
        intensity: str = "moderate",
    ) -> list[list[UsageSession]]:
        """Simulate one week of usage data."""
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_date -= timedelta(days=start_date.weekday())  # Start from Monday

        week: list[list[UsageSession]] = []
        for day_offset in range(7):
            day = start_date + timedelta(days=day_offset)
            # Weekends tend to be heavier
            day_intensity = (
                "heavy" if day_offset >= 5 else intensity
            )
            week.append(self.simulate_day(day, day_intensity))

        return week

    def _pick_hour(self) -> int:
        """Pick an hour weighted by typical usage patterns."""
        hours = list(self.HOURLY_WEIGHTS.keys())
        weights = list(self.HOURLY_WEIGHTS.values())
        return random.choices(hours, weights=weights, k=1)[0]

    def simulate_doom_scrolling_day(self, date: datetime | None = None) -> list[UsageSession]:
        """Simulate a day with heavy doom scrolling behavior."""
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        sessions = self.simulate_day(date, intensity="heavy")

        # Add several long social media sessions
        doom_apps = ["Instagram", "TikTok", "Reddit", "Twitter"]
        for app in random.sample(doom_apps, 2):
            for hour in [10, 14, 21]:
                start = date.replace(hour=hour, minute=random.randint(0, 30))
                duration = random.randint(40, 90)
                sessions.append(
                    UsageSession(
                        app_name=app,
                        category=AppCategory.SOCIAL_MEDIA,
                        start_time=start,
                        end_time=start + timedelta(minutes=duration),
                        duration_minutes=duration,
                        notifications_received=random.randint(5, 20),
                        pickups=1,
                    )
                )

        sessions.sort(key=lambda s: s.start_time)
        return sessions

    def simulate_late_night_day(self, date: datetime | None = None) -> list[UsageSession]:
        """Simulate a day with significant late-night usage."""
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        sessions = self.simulate_day(date, intensity="moderate")

        # Add late night sessions
        late_night_apps = [
            ("Instagram", AppCategory.SOCIAL_MEDIA),
            ("YouTube", AppCategory.ENTERTAINMENT),
            ("Reddit", AppCategory.SOCIAL_MEDIA),
        ]
        for app_name, category in late_night_apps:
            hour = random.choice([22, 23, 0, 1])
            start = date.replace(hour=hour, minute=random.randint(0, 59))
            if hour < 6:
                start += timedelta(days=1)
            duration = random.randint(20, 60)
            sessions.append(
                UsageSession(
                    app_name=app_name,
                    category=category,
                    start_time=start,
                    end_time=start + timedelta(minutes=duration),
                    duration_minutes=duration,
                    notifications_received=random.randint(0, 5),
                    pickups=1,
                )
            )

        sessions.sort(key=lambda s: s.start_time)
        return sessions
