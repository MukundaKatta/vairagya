"""Notification analysis and categorization."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from vairagya.models import AppCategory


class Notification(BaseModel):
    """A single notification event."""

    app_name: str
    category: AppCategory
    timestamp: datetime
    was_opened: bool = Field(default=False)
    response_time_seconds: Optional[float] = Field(default=None, ge=0)


class NotificationAnalyzer:
    """Analyze notification patterns to identify interruption costs."""

    NOTIFICATION_HEAVY_APPS = {
        "instagram": 25,
        "twitter": 30,
        "facebook": 20,
        "whatsapp": 40,
        "slack": 35,
        "email": 15,
        "gmail": 15,
        "tiktok": 20,
        "snapchat": 15,
        "discord": 25,
        "reddit": 10,
        "news": 10,
        "teams": 20,
    }

    # Average context-switching cost in minutes per notification opened
    CONTEXT_SWITCH_COST_MINUTES = 3.5

    def __init__(self) -> None:
        self.notifications: list[Notification] = []

    def add_notification(
        self,
        app_name: str,
        timestamp: datetime,
        category: AppCategory | None = None,
        was_opened: bool = False,
        response_time_seconds: float | None = None,
    ) -> Notification:
        """Log a notification event."""
        if category is None:
            from vairagya.monitor.screen_time import ScreenTimeTracker
            category = ScreenTimeTracker().categorize_app(app_name)

        notification = Notification(
            app_name=app_name,
            category=category,
            timestamp=timestamp,
            was_opened=was_opened,
            response_time_seconds=response_time_seconds,
        )
        self.notifications.append(notification)
        return notification

    def get_daily_count(self, date: datetime | None = None) -> int:
        """Count notifications for a specific day."""
        if date is None:
            date = datetime.now()
        return sum(
            1 for n in self.notifications if n.timestamp.date() == date.date()
        )

    def get_category_breakdown(self) -> dict[str, int]:
        """Break down notifications by category."""
        breakdown: dict[str, int] = {}
        for n in self.notifications:
            cat = n.category.value
            breakdown[cat] = breakdown.get(cat, 0) + 1
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))

    def get_app_breakdown(self) -> dict[str, int]:
        """Break down notifications by app."""
        breakdown: dict[str, int] = {}
        for n in self.notifications:
            breakdown[n.app_name] = breakdown.get(n.app_name, 0) + 1
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))

    def get_hourly_distribution(self) -> dict[int, int]:
        """Get notification counts by hour of day."""
        dist: dict[int, int] = {h: 0 for h in range(24)}
        for n in self.notifications:
            dist[n.timestamp.hour] += 1
        return dist

    def calculate_interruption_cost(self) -> dict:
        """Calculate the estimated productivity cost of notifications."""
        opened = [n for n in self.notifications if n.was_opened]
        total_opened = len(opened)
        total_notifications = len(self.notifications)

        open_rate = total_opened / total_notifications * 100 if total_notifications > 0 else 0
        estimated_lost_minutes = total_opened * self.CONTEXT_SWITCH_COST_MINUTES

        avg_response = 0.0
        responses = [n.response_time_seconds for n in opened if n.response_time_seconds is not None]
        if responses:
            avg_response = sum(responses) / len(responses)

        return {
            "total_notifications": total_notifications,
            "total_opened": total_opened,
            "open_rate_percent": round(open_rate, 1),
            "estimated_lost_minutes": round(estimated_lost_minutes, 1),
            "estimated_lost_hours": round(estimated_lost_minutes / 60, 1),
            "average_response_seconds": round(avg_response, 1),
            "top_interrupter": self._get_top_interrupter(),
        }

    def _get_top_interrupter(self) -> str:
        """Find the app that causes the most interruptions."""
        opened_by_app: dict[str, int] = {}
        for n in self.notifications:
            if n.was_opened:
                opened_by_app[n.app_name] = opened_by_app.get(n.app_name, 0) + 1
        if not opened_by_app:
            return "none"
        return max(opened_by_app, key=opened_by_app.get)  # type: ignore[arg-type]

    def get_peak_interruption_hours(self, top_n: int = 3) -> list[int]:
        """Find the hours with the most notifications."""
        dist = self.get_hourly_distribution()
        sorted_hours = sorted(dist.items(), key=lambda x: x[1], reverse=True)
        return [h for h, _ in sorted_hours[:top_n]]

    def analyze_response_patterns(self) -> dict:
        """Analyze how quickly the user responds to notifications."""
        opened = [n for n in self.notifications if n.was_opened and n.response_time_seconds is not None]
        if not opened:
            return {"pattern": "no_data", "avg_response_seconds": 0}

        response_times = [n.response_time_seconds for n in opened]
        avg = sum(response_times) / len(response_times)  # type: ignore[arg-type]

        if avg < 30:
            pattern = "compulsive_checker"
            description = "You respond to notifications almost immediately, suggesting compulsive checking behavior."
        elif avg < 120:
            pattern = "reactive"
            description = "You respond to most notifications fairly quickly."
        elif avg < 600:
            pattern = "moderate"
            description = "You take a reasonable time to respond to notifications."
        else:
            pattern = "mindful"
            description = "You practice healthy notification habits by not responding immediately."

        return {
            "pattern": pattern,
            "description": description,
            "avg_response_seconds": round(avg, 1),
            "fastest_response": round(min(response_times), 1),  # type: ignore[arg-type]
            "slowest_response": round(max(response_times), 1),  # type: ignore[arg-type]
        }
