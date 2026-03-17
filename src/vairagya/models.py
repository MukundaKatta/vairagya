"""Data models for the digital detox coach."""

from __future__ import annotations

from datetime import datetime, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AppCategory(str, Enum):
    """Categories of applications."""

    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    COMMUNICATION = "communication"
    PRODUCTIVITY = "productivity"
    NEWS = "news"
    GAMING = "gaming"
    SHOPPING = "shopping"
    BROWSING = "browsing"
    HEALTH = "health"
    EDUCATION = "education"


class PatternType(str, Enum):
    """Types of addictive usage patterns."""

    DOOM_SCROLLING = "doom_scrolling"
    CHECKING_FREQUENCY = "checking_frequency"
    LATE_NIGHT_USE = "late_night_use"
    BINGE_WATCHING = "binge_watching"
    NOTIFICATION_REACTIVE = "notification_reactive"
    FIRST_THING_MORNING = "first_thing_morning"
    CONTEXT_SWITCHING = "context_switching"
    PHANTOM_CHECKING = "phantom_checking"


class ChallengeDifficulty(str, Enum):
    """Difficulty levels for detox challenges."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXTREME = "extreme"


class UsageSession(BaseModel):
    """A single usage session for an app."""

    app_name: str = Field(description="Name of the application")
    category: AppCategory
    start_time: datetime
    end_time: datetime
    duration_minutes: float = Field(ge=0, description="Duration in minutes")
    notifications_received: int = Field(default=0, ge=0)
    pickups: int = Field(default=1, ge=0, description="Number of times device was picked up")

    @property
    def is_late_night(self) -> bool:
        """Check if usage occurred during late night hours (10pm-6am)."""
        hour = self.start_time.hour
        return hour >= 22 or hour < 6

    @property
    def is_early_morning(self) -> bool:
        """Check if usage occurred first thing in the morning (before 7am)."""
        return self.start_time.hour < 7


class ScreenTime(BaseModel):
    """Aggregated screen time for a day."""

    date: datetime = Field(default_factory=datetime.now)
    total_minutes: float = Field(default=0, ge=0)
    by_category: dict[str, float] = Field(
        default_factory=dict, description="Minutes per category"
    )
    by_app: dict[str, float] = Field(
        default_factory=dict, description="Minutes per app"
    )
    total_pickups: int = Field(default=0, ge=0)
    total_notifications: int = Field(default=0, ge=0)
    sessions: list[UsageSession] = Field(default_factory=list)
    first_use_time: Optional[time] = None
    last_use_time: Optional[time] = None


class DetoxGoal(BaseModel):
    """A screen time reduction goal."""

    goal_id: str = Field(description="Unique goal identifier")
    category: Optional[AppCategory] = None
    app_name: Optional[str] = None
    daily_limit_minutes: int = Field(ge=0, description="Daily limit in minutes")
    current_average_minutes: float = Field(default=0, ge=0)
    start_date: datetime = Field(default_factory=datetime.now)
    target_date: Optional[datetime] = None
    is_active: bool = Field(default=True)
    streak_days: int = Field(default=0, ge=0)
    total_days_met: int = Field(default=0, ge=0)
    total_days_tracked: int = Field(default=0, ge=0)

    @property
    def compliance_rate(self) -> float:
        """Calculate goal compliance rate."""
        if self.total_days_tracked == 0:
            return 0.0
        return self.total_days_met / self.total_days_tracked * 100

    @property
    def reduction_target_percent(self) -> float:
        """Calculate the percent reduction targeted."""
        if self.current_average_minutes == 0:
            return 0.0
        return (
            (self.current_average_minutes - self.daily_limit_minutes)
            / self.current_average_minutes
            * 100
        )


class Challenge(BaseModel):
    """A digital detox challenge."""

    challenge_id: str
    title: str
    description: str
    difficulty: ChallengeDifficulty
    duration_days: int = Field(ge=1)
    category: Optional[AppCategory] = None
    rules: list[str] = Field(default_factory=list)
    tips: list[str] = Field(default_factory=list)
    is_completed: bool = Field(default=False)
    started_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None


class DetectedPattern(BaseModel):
    """An addictive usage pattern detected from data."""

    pattern_type: PatternType
    severity: str = Field(default="moderate", description="low, moderate, high")
    description: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str = Field(default="")
