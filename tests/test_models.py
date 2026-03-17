"""Tests for data models."""

import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from vairagya.models import (
    AppCategory,
    Challenge,
    ChallengeDifficulty,
    DetectedPattern,
    DetoxGoal,
    PatternType,
    ScreenTime,
    UsageSession,
)


class TestUsageSession:
    def test_create_session(self) -> None:
        now = datetime.now()
        session = UsageSession(
            app_name="Instagram",
            category=AppCategory.SOCIAL_MEDIA,
            start_time=now - timedelta(minutes=30),
            end_time=now,
            duration_minutes=30,
        )
        assert session.app_name == "Instagram"
        assert session.duration_minutes == 30

    def test_late_night_detection(self) -> None:
        late = datetime.now().replace(hour=23, minute=0)
        session = UsageSession(
            app_name="TikTok",
            category=AppCategory.SOCIAL_MEDIA,
            start_time=late,
            end_time=late + timedelta(minutes=30),
            duration_minutes=30,
        )
        assert session.is_late_night is True

    def test_not_late_night(self) -> None:
        afternoon = datetime.now().replace(hour=14, minute=0)
        session = UsageSession(
            app_name="TikTok",
            category=AppCategory.SOCIAL_MEDIA,
            start_time=afternoon,
            end_time=afternoon + timedelta(minutes=30),
            duration_minutes=30,
        )
        assert session.is_late_night is False

    def test_early_morning(self) -> None:
        early = datetime.now().replace(hour=6, minute=30)
        session = UsageSession(
            app_name="Instagram",
            category=AppCategory.SOCIAL_MEDIA,
            start_time=early,
            end_time=early + timedelta(minutes=10),
            duration_minutes=10,
        )
        assert session.is_early_morning is True

    def test_invalid_duration(self) -> None:
        now = datetime.now()
        with pytest.raises(ValidationError):
            UsageSession(
                app_name="Test",
                category=AppCategory.BROWSING,
                start_time=now,
                end_time=now,
                duration_minutes=-5,
            )


class TestScreenTime:
    def test_create_screen_time(self) -> None:
        st = ScreenTime(
            total_minutes=120,
            by_category={"social_media": 60, "entertainment": 60},
            total_pickups=30,
        )
        assert st.total_minutes == 120
        assert st.total_pickups == 30

    def test_defaults(self) -> None:
        st = ScreenTime()
        assert st.total_minutes == 0
        assert st.total_pickups == 0


class TestDetoxGoal:
    def test_compliance_rate(self) -> None:
        goal = DetoxGoal(
            goal_id="G1",
            daily_limit_minutes=30,
            total_days_met=7,
            total_days_tracked=10,
        )
        assert goal.compliance_rate == 70.0

    def test_compliance_rate_zero_days(self) -> None:
        goal = DetoxGoal(goal_id="G1", daily_limit_minutes=30)
        assert goal.compliance_rate == 0.0

    def test_reduction_target(self) -> None:
        goal = DetoxGoal(
            goal_id="G1",
            daily_limit_minutes=30,
            current_average_minutes=120,
        )
        assert goal.reduction_target_percent == 75.0


class TestChallenge:
    def test_create_challenge(self) -> None:
        ch = Challenge(
            challenge_id="CH1",
            title="Test Challenge",
            description="A test",
            difficulty=ChallengeDifficulty.EASY,
            duration_days=1,
            rules=["Rule 1"],
            tips=["Tip 1"],
        )
        assert ch.title == "Test Challenge"
        assert ch.is_completed is False


class TestDetectedPattern:
    def test_create_pattern(self) -> None:
        p = DetectedPattern(
            pattern_type=PatternType.DOOM_SCROLLING,
            severity="high",
            description="Doom scrolling detected",
            evidence=["Instagram: 45 min"],
            recommendation="Set a timer",
        )
        assert p.pattern_type == PatternType.DOOM_SCROLLING
        assert p.severity == "high"


class TestAppCategory:
    def test_all_categories(self) -> None:
        categories = list(AppCategory)
        assert len(categories) >= 8
        assert AppCategory.SOCIAL_MEDIA in categories
        assert AppCategory.ENTERTAINMENT in categories
