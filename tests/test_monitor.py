"""Tests for usage monitoring modules."""

import pytest
from datetime import datetime, timedelta

from vairagya.models import AppCategory, PatternType
from vairagya.monitor.screen_time import ScreenTimeTracker
from vairagya.monitor.notifications import NotificationAnalyzer
from vairagya.monitor.patterns import UsagePatternDetector


class TestScreenTimeTracker:
    def test_log_session(self) -> None:
        tracker = ScreenTimeTracker()
        now = datetime.now()
        session = tracker.log_session(
            app_name="Instagram",
            start_time=now - timedelta(minutes=30),
            end_time=now,
            category=AppCategory.SOCIAL_MEDIA,
        )
        assert session.app_name == "Instagram"
        assert session.category == AppCategory.SOCIAL_MEDIA
        assert session.duration_minutes == 30.0

    def test_categorize_app(self) -> None:
        tracker = ScreenTimeTracker()
        assert tracker.categorize_app("Instagram") == AppCategory.SOCIAL_MEDIA
        assert tracker.categorize_app("YouTube") == AppCategory.ENTERTAINMENT
        assert tracker.categorize_app("Slack") == AppCategory.COMMUNICATION
        assert tracker.categorize_app("Chrome") == AppCategory.BROWSING

    def test_categorize_unknown_app(self) -> None:
        tracker = ScreenTimeTracker()
        assert tracker.categorize_app("UnknownApp") == AppCategory.BROWSING

    def test_daily_summary(self) -> None:
        tracker = ScreenTimeTracker()
        now = datetime.now()

        tracker.log_session("Instagram", now - timedelta(minutes=30), now,
                           AppCategory.SOCIAL_MEDIA)
        tracker.log_session("YouTube", now - timedelta(minutes=60), now - timedelta(minutes=30),
                           AppCategory.ENTERTAINMENT)

        summary = tracker.get_daily_summary(now)
        assert summary.total_minutes == 60.0
        assert "social_media" in summary.by_category
        assert "entertainment" in summary.by_category

    def test_category_breakdown(self) -> None:
        tracker = ScreenTimeTracker()
        now = datetime.now()
        tracker.log_session("Instagram", now - timedelta(minutes=30), now,
                           AppCategory.SOCIAL_MEDIA)
        tracker.log_session("TikTok", now - timedelta(minutes=20), now,
                           AppCategory.SOCIAL_MEDIA)

        breakdown = tracker.get_category_breakdown()
        assert breakdown["social_media"] == 50.0

    def test_top_apps(self) -> None:
        tracker = ScreenTimeTracker()
        now = datetime.now()
        tracker.log_session("Instagram", now - timedelta(minutes=60), now,
                           AppCategory.SOCIAL_MEDIA)
        tracker.log_session("TikTok", now - timedelta(minutes=30), now,
                           AppCategory.SOCIAL_MEDIA)

        top = tracker.get_top_apps(limit=2)
        assert top[0][0] == "Instagram"
        assert top[0][1] == 60.0

    def test_average_daily_usage(self) -> None:
        tracker = ScreenTimeTracker()
        now = datetime.now()
        tracker.log_session("Instagram", now - timedelta(minutes=60), now,
                           AppCategory.SOCIAL_MEDIA)
        avg = tracker.get_average_daily_usage()
        assert avg == 60.0

    def test_empty_tracker(self) -> None:
        tracker = ScreenTimeTracker()
        assert tracker.get_average_daily_usage() == 0.0
        summary = tracker.get_daily_summary()
        assert summary.total_minutes == 0


class TestNotificationAnalyzer:
    def test_add_notification(self) -> None:
        analyzer = NotificationAnalyzer()
        now = datetime.now()
        n = analyzer.add_notification("Instagram", now, AppCategory.SOCIAL_MEDIA)
        assert n.app_name == "Instagram"
        assert len(analyzer.notifications) == 1

    def test_daily_count(self) -> None:
        analyzer = NotificationAnalyzer()
        now = datetime.now()
        for _ in range(5):
            analyzer.add_notification("Instagram", now, AppCategory.SOCIAL_MEDIA)
        assert analyzer.get_daily_count(now) == 5

    def test_category_breakdown(self) -> None:
        analyzer = NotificationAnalyzer()
        now = datetime.now()
        analyzer.add_notification("Instagram", now, AppCategory.SOCIAL_MEDIA)
        analyzer.add_notification("Instagram", now, AppCategory.SOCIAL_MEDIA)
        analyzer.add_notification("Slack", now, AppCategory.COMMUNICATION)

        breakdown = analyzer.get_category_breakdown()
        assert breakdown["social_media"] == 2
        assert breakdown["communication"] == 1

    def test_interruption_cost(self) -> None:
        analyzer = NotificationAnalyzer()
        now = datetime.now()
        for i in range(10):
            analyzer.add_notification(
                "Instagram", now, AppCategory.SOCIAL_MEDIA,
                was_opened=(i % 2 == 0),
                response_time_seconds=30.0 if i % 2 == 0 else None,
            )
        cost = analyzer.calculate_interruption_cost()
        assert cost["total_notifications"] == 10
        assert cost["total_opened"] == 5
        assert cost["estimated_lost_minutes"] > 0

    def test_response_patterns_compulsive(self) -> None:
        analyzer = NotificationAnalyzer()
        now = datetime.now()
        for _ in range(10):
            analyzer.add_notification(
                "WhatsApp", now, AppCategory.COMMUNICATION,
                was_opened=True, response_time_seconds=10.0,
            )
        patterns = analyzer.analyze_response_patterns()
        assert patterns["pattern"] == "compulsive_checker"

    def test_hourly_distribution(self) -> None:
        analyzer = NotificationAnalyzer()
        base = datetime.now().replace(hour=14, minute=0)
        for _ in range(5):
            analyzer.add_notification("Slack", base, AppCategory.COMMUNICATION)
        dist = analyzer.get_hourly_distribution()
        assert dist[14] == 5

    def test_peak_interruption_hours(self) -> None:
        analyzer = NotificationAnalyzer()
        base = datetime.now().replace(minute=0)
        for _ in range(10):
            analyzer.add_notification("Slack", base.replace(hour=14), AppCategory.COMMUNICATION)
        for _ in range(5):
            analyzer.add_notification("Slack", base.replace(hour=10), AppCategory.COMMUNICATION)

        peaks = analyzer.get_peak_interruption_hours(top_n=1)
        assert peaks[0] == 14


class TestUsagePatternDetector:
    def test_detect_doom_scrolling(self) -> None:
        detector = UsagePatternDetector()
        now = datetime.now()
        from vairagya.models import UsageSession
        sessions = [
            UsageSession(
                app_name="Instagram",
                category=AppCategory.SOCIAL_MEDIA,
                start_time=now - timedelta(minutes=45),
                end_time=now,
                duration_minutes=45,
            ),
        ]
        pattern = detector.detect_doom_scrolling(sessions)
        assert pattern is not None
        assert pattern.pattern_type == PatternType.DOOM_SCROLLING

    def test_no_doom_scrolling_short_sessions(self) -> None:
        detector = UsagePatternDetector()
        now = datetime.now()
        from vairagya.models import UsageSession
        sessions = [
            UsageSession(
                app_name="Instagram",
                category=AppCategory.SOCIAL_MEDIA,
                start_time=now - timedelta(minutes=10),
                end_time=now,
                duration_minutes=10,
            ),
        ]
        pattern = detector.detect_doom_scrolling(sessions)
        assert pattern is None

    def test_detect_late_night_use(self) -> None:
        detector = UsagePatternDetector()
        from vairagya.models import UsageSession
        late = datetime.now().replace(hour=23, minute=0)
        sessions = [
            UsageSession(
                app_name="Reddit",
                category=AppCategory.SOCIAL_MEDIA,
                start_time=late,
                end_time=late + timedelta(minutes=30),
                duration_minutes=30,
            ),
        ]
        pattern = detector.detect_late_night_use(sessions)
        assert pattern is not None
        assert pattern.pattern_type == PatternType.LATE_NIGHT_USE

    def test_detect_checking_frequency(self) -> None:
        detector = UsagePatternDetector()
        from vairagya.models import UsageSession
        now = datetime.now()
        sessions = [
            UsageSession(
                app_name="WhatsApp",
                category=AppCategory.COMMUNICATION,
                start_time=now - timedelta(minutes=i * 5),
                end_time=now - timedelta(minutes=i * 5 - 1),
                duration_minutes=1,
                pickups=2,
            )
            for i in range(15)
        ]
        pattern = detector.detect_checking_frequency(sessions)
        assert pattern is not None
        assert pattern.pattern_type == PatternType.CHECKING_FREQUENCY

    def test_detect_binge_watching(self) -> None:
        detector = UsagePatternDetector()
        from vairagya.models import UsageSession
        now = datetime.now()
        sessions = [
            UsageSession(
                app_name="Netflix",
                category=AppCategory.ENTERTAINMENT,
                start_time=now - timedelta(minutes=180),
                end_time=now,
                duration_minutes=180,
            ),
        ]
        pattern = detector.detect_binge_watching(sessions)
        assert pattern is not None
        assert pattern.pattern_type == PatternType.BINGE_WATCHING

    def test_detect_all_patterns(self) -> None:
        detector = UsagePatternDetector()
        from vairagya.simulator import UsageSimulator
        simulator = UsageSimulator()
        sessions = simulator.simulate_doom_scrolling_day()
        patterns = detector.detect_all_patterns(sessions)
        # Should detect at least doom scrolling from the heavy simulation
        pattern_types = [p.pattern_type for p in patterns]
        assert PatternType.DOOM_SCROLLING in pattern_types
