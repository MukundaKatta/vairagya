"""Screen time tracking by app and category."""

from __future__ import annotations

from datetime import datetime

from vairagya.models import AppCategory, ScreenTime, UsageSession


class ScreenTimeTracker:
    """Track and aggregate screen time usage by app and category."""

    APP_CATEGORIES: dict[str, AppCategory] = {
        # Social Media
        "instagram": AppCategory.SOCIAL_MEDIA,
        "tiktok": AppCategory.SOCIAL_MEDIA,
        "twitter": AppCategory.SOCIAL_MEDIA,
        "x": AppCategory.SOCIAL_MEDIA,
        "facebook": AppCategory.SOCIAL_MEDIA,
        "reddit": AppCategory.SOCIAL_MEDIA,
        "snapchat": AppCategory.SOCIAL_MEDIA,
        "linkedin": AppCategory.SOCIAL_MEDIA,
        "threads": AppCategory.SOCIAL_MEDIA,
        # Entertainment
        "youtube": AppCategory.ENTERTAINMENT,
        "netflix": AppCategory.ENTERTAINMENT,
        "twitch": AppCategory.ENTERTAINMENT,
        "spotify": AppCategory.ENTERTAINMENT,
        "disney+": AppCategory.ENTERTAINMENT,
        "hulu": AppCategory.ENTERTAINMENT,
        "hbo max": AppCategory.ENTERTAINMENT,
        "apple tv": AppCategory.ENTERTAINMENT,
        # Communication
        "whatsapp": AppCategory.COMMUNICATION,
        "slack": AppCategory.COMMUNICATION,
        "discord": AppCategory.COMMUNICATION,
        "email": AppCategory.COMMUNICATION,
        "gmail": AppCategory.COMMUNICATION,
        "messages": AppCategory.COMMUNICATION,
        "telegram": AppCategory.COMMUNICATION,
        "teams": AppCategory.COMMUNICATION,
        "zoom": AppCategory.COMMUNICATION,
        # Productivity
        "vscode": AppCategory.PRODUCTIVITY,
        "notion": AppCategory.PRODUCTIVITY,
        "google docs": AppCategory.PRODUCTIVITY,
        "excel": AppCategory.PRODUCTIVITY,
        "figma": AppCategory.PRODUCTIVITY,
        "calendar": AppCategory.PRODUCTIVITY,
        # News
        "apple news": AppCategory.NEWS,
        "google news": AppCategory.NEWS,
        "bbc news": AppCategory.NEWS,
        "cnn": AppCategory.NEWS,
        "nyt": AppCategory.NEWS,
        # Gaming
        "candy crush": AppCategory.GAMING,
        "wordle": AppCategory.GAMING,
        "steam": AppCategory.GAMING,
        "roblox": AppCategory.GAMING,
        # Shopping
        "amazon": AppCategory.SHOPPING,
        "ebay": AppCategory.SHOPPING,
        "etsy": AppCategory.SHOPPING,
        # Browsing
        "chrome": AppCategory.BROWSING,
        "safari": AppCategory.BROWSING,
        "firefox": AppCategory.BROWSING,
    }

    def __init__(self) -> None:
        self.sessions: list[UsageSession] = []

    def log_session(
        self,
        app_name: str,
        start_time: datetime,
        end_time: datetime,
        category: AppCategory | None = None,
        notifications: int = 0,
        pickups: int = 1,
    ) -> UsageSession:
        """Log a usage session."""
        if category is None:
            category = self.categorize_app(app_name)

        duration = (end_time - start_time).total_seconds() / 60.0

        session = UsageSession(
            app_name=app_name,
            category=category,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=round(duration, 1),
            notifications_received=notifications,
            pickups=pickups,
        )
        self.sessions.append(session)
        return session

    def categorize_app(self, app_name: str) -> AppCategory:
        """Categorize an app by name."""
        normalized = app_name.lower().strip()
        return self.APP_CATEGORIES.get(normalized, AppCategory.BROWSING)

    def get_daily_summary(self, date: datetime | None = None) -> ScreenTime:
        """Get aggregated screen time for a specific day."""
        if date is None:
            date = datetime.now()

        day_sessions = [
            s for s in self.sessions
            if s.start_time.date() == date.date()
        ]

        by_category: dict[str, float] = {}
        by_app: dict[str, float] = {}
        total_minutes = 0.0
        total_pickups = 0
        total_notifications = 0

        for session in day_sessions:
            cat = session.category.value
            by_category[cat] = by_category.get(cat, 0) + session.duration_minutes
            by_app[session.app_name] = (
                by_app.get(session.app_name, 0) + session.duration_minutes
            )
            total_minutes += session.duration_minutes
            total_pickups += session.pickups
            total_notifications += session.notifications_received

        first_use = None
        last_use = None
        if day_sessions:
            sorted_sessions = sorted(day_sessions, key=lambda s: s.start_time)
            first_use = sorted_sessions[0].start_time.time()
            last_use = sorted_sessions[-1].end_time.time()

        return ScreenTime(
            date=date,
            total_minutes=round(total_minutes, 1),
            by_category=by_category,
            by_app=by_app,
            total_pickups=total_pickups,
            total_notifications=total_notifications,
            sessions=day_sessions,
            first_use_time=first_use,
            last_use_time=last_use,
        )

    def get_category_breakdown(self) -> dict[str, float]:
        """Get total time breakdown by category across all sessions."""
        breakdown: dict[str, float] = {}
        for session in self.sessions:
            cat = session.category.value
            breakdown[cat] = breakdown.get(cat, 0) + session.duration_minutes
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))

    def get_top_apps(self, limit: int = 5) -> list[tuple[str, float]]:
        """Get the top apps by usage time."""
        by_app: dict[str, float] = {}
        for session in self.sessions:
            by_app[session.app_name] = (
                by_app.get(session.app_name, 0) + session.duration_minutes
            )
        sorted_apps = sorted(by_app.items(), key=lambda x: x[1], reverse=True)
        return sorted_apps[:limit]

    def get_average_daily_usage(self) -> float:
        """Calculate average daily screen time in minutes."""
        if not self.sessions:
            return 0.0
        dates = {s.start_time.date() for s in self.sessions}
        total = sum(s.duration_minutes for s in self.sessions)
        return round(total / len(dates), 1)
