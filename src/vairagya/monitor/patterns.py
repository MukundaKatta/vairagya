"""Usage pattern detection for identifying addictive behaviors."""

from __future__ import annotations

from collections import Counter
from datetime import timedelta

from vairagya.models import (
    AppCategory,
    DetectedPattern,
    PatternType,
    ScreenTime,
    UsageSession,
)


class UsagePatternDetector:
    """Detect addictive usage patterns from screen time data.

    Identifies patterns such as doom scrolling, compulsive checking,
    late night use, binge watching, and more.
    """

    # Thresholds for pattern detection
    DOOM_SCROLL_THRESHOLD_MINUTES = 30  # Continuous social media > 30 min
    CHECKING_FREQUENCY_THRESHOLD = 20  # Pickups per day
    LATE_NIGHT_HOUR_START = 22  # 10 PM
    LATE_NIGHT_HOUR_END = 6  # 6 AM
    BINGE_WATCH_THRESHOLD_MINUTES = 120  # 2+ hours streaming
    MORNING_CHECK_THRESHOLD_MINUTES = 5  # Phone within 5 min of waking
    CONTEXT_SWITCH_THRESHOLD = 10  # App switches per hour

    def detect_all_patterns(
        self, sessions: list[UsageSession], daily_summary: ScreenTime | None = None
    ) -> list[DetectedPattern]:
        """Run all pattern detection algorithms."""
        patterns: list[DetectedPattern] = []

        doom_scroll = self.detect_doom_scrolling(sessions)
        if doom_scroll:
            patterns.append(doom_scroll)

        checking = self.detect_checking_frequency(sessions, daily_summary)
        if checking:
            patterns.append(checking)

        late_night = self.detect_late_night_use(sessions)
        if late_night:
            patterns.append(late_night)

        binge = self.detect_binge_watching(sessions)
        if binge:
            patterns.append(binge)

        morning = self.detect_first_thing_morning(sessions)
        if morning:
            patterns.append(morning)

        reactive = self.detect_notification_reactive(sessions)
        if reactive:
            patterns.append(reactive)

        switching = self.detect_context_switching(sessions)
        if switching:
            patterns.append(switching)

        return patterns

    def detect_doom_scrolling(
        self, sessions: list[UsageSession]
    ) -> DetectedPattern | None:
        """Detect doom scrolling - extended social media or news browsing sessions."""
        scrolling_categories = {AppCategory.SOCIAL_MEDIA, AppCategory.NEWS}

        long_sessions = [
            s for s in sessions
            if s.category in scrolling_categories
            and s.duration_minutes >= self.DOOM_SCROLL_THRESHOLD_MINUTES
        ]

        if not long_sessions:
            return None

        total_doom_minutes = sum(s.duration_minutes for s in long_sessions)
        apps = list({s.app_name for s in long_sessions})

        severity = "low"
        if total_doom_minutes > 120:
            severity = "high"
        elif total_doom_minutes > 60:
            severity = "moderate"

        return DetectedPattern(
            pattern_type=PatternType.DOOM_SCROLLING,
            severity=severity,
            description=(
                f"Detected {len(long_sessions)} doom scrolling session(s) "
                f"totaling {total_doom_minutes:.0f} minutes on {', '.join(apps)}."
            ),
            evidence=[
                f"{s.app_name}: {s.duration_minutes:.0f} min "
                f"({s.start_time.strftime('%H:%M')}-{s.end_time.strftime('%H:%M')})"
                for s in long_sessions
            ],
            recommendation=(
                "Try setting a timer before opening social media. "
                "Use app timers to limit sessions to 15-20 minutes. "
                "Consider removing infinite-scroll apps from your home screen."
            ),
        )

    def detect_checking_frequency(
        self,
        sessions: list[UsageSession],
        daily_summary: ScreenTime | None = None,
    ) -> DetectedPattern | None:
        """Detect compulsive checking - excessive phone pickups."""
        total_pickups = (
            daily_summary.total_pickups
            if daily_summary
            else sum(s.pickups for s in sessions)
        )

        if total_pickups < self.CHECKING_FREQUENCY_THRESHOLD:
            return None

        severity = "low"
        if total_pickups > 80:
            severity = "high"
        elif total_pickups > 50:
            severity = "moderate"

        # Find most-checked apps
        app_pickups: dict[str, int] = {}
        for s in sessions:
            app_pickups[s.app_name] = app_pickups.get(s.app_name, 0) + s.pickups
        top_apps = sorted(app_pickups.items(), key=lambda x: x[1], reverse=True)[:3]

        return DetectedPattern(
            pattern_type=PatternType.CHECKING_FREQUENCY,
            severity=severity,
            description=(
                f"Device was picked up {total_pickups} times today. "
                f"Average is recommended to be under {self.CHECKING_FREQUENCY_THRESHOLD}."
            ),
            evidence=[f"{app}: {count} pickups" for app, count in top_apps],
            recommendation=(
                "Try batching your phone checks to specific times. "
                "Place your phone face-down or in another room during focus time. "
                "Turn off non-essential notifications."
            ),
        )

    def detect_late_night_use(
        self, sessions: list[UsageSession]
    ) -> DetectedPattern | None:
        """Detect late night device use that may affect sleep."""
        late_sessions = [s for s in sessions if s.is_late_night]

        if not late_sessions:
            return None

        total_late_minutes = sum(s.duration_minutes for s in late_sessions)
        apps = list({s.app_name for s in late_sessions})

        severity = "low"
        if total_late_minutes > 60:
            severity = "high"
        elif total_late_minutes > 30:
            severity = "moderate"

        return DetectedPattern(
            pattern_type=PatternType.LATE_NIGHT_USE,
            severity=severity,
            description=(
                f"Detected {total_late_minutes:.0f} minutes of screen time "
                f"between {self.LATE_NIGHT_HOUR_START}:00 and "
                f"{self.LATE_NIGHT_HOUR_END}:00 on {', '.join(apps)}."
            ),
            evidence=[
                f"{s.app_name}: {s.duration_minutes:.0f} min at "
                f"{s.start_time.strftime('%H:%M')}"
                for s in late_sessions
            ],
            recommendation=(
                "Blue light from screens suppresses melatonin production. "
                "Set a digital curfew 1 hour before bedtime. "
                "Use Night Shift/blue light filter if you must use your device. "
                "Try reading a physical book instead."
            ),
        )

    def detect_binge_watching(
        self, sessions: list[UsageSession]
    ) -> DetectedPattern | None:
        """Detect binge watching - extended entertainment streaming."""
        entertainment_sessions = [
            s for s in sessions
            if s.category == AppCategory.ENTERTAINMENT
            and s.duration_minutes >= self.BINGE_WATCH_THRESHOLD_MINUTES
        ]

        if not entertainment_sessions:
            return None

        total = sum(s.duration_minutes for s in entertainment_sessions)
        apps = list({s.app_name for s in entertainment_sessions})

        severity = "moderate" if total < 240 else "high"

        return DetectedPattern(
            pattern_type=PatternType.BINGE_WATCHING,
            severity=severity,
            description=(
                f"Detected {total:.0f} minutes of continuous streaming on "
                f"{', '.join(apps)}."
            ),
            evidence=[
                f"{s.app_name}: {s.duration_minutes:.0f} min"
                for s in entertainment_sessions
            ],
            recommendation=(
                "Set episode limits before you start watching. "
                "Turn off auto-play to create natural stopping points. "
                "Take a 10-minute break between episodes to check in with yourself."
            ),
        )

    def detect_first_thing_morning(
        self, sessions: list[UsageSession]
    ) -> DetectedPattern | None:
        """Detect checking phone first thing in the morning."""
        morning_sessions = [
            s for s in sessions
            if s.is_early_morning
            and s.category in {AppCategory.SOCIAL_MEDIA, AppCategory.NEWS, AppCategory.COMMUNICATION}
        ]

        if not morning_sessions:
            return None

        apps = list({s.app_name for s in morning_sessions})

        return DetectedPattern(
            pattern_type=PatternType.FIRST_THING_MORNING,
            severity="moderate",
            description=(
                f"Phone was checked first thing in the morning on "
                f"{', '.join(apps)} before 7 AM."
            ),
            evidence=[
                f"{s.app_name} opened at {s.start_time.strftime('%H:%M')}"
                for s in morning_sessions[:3]
            ],
            recommendation=(
                "Your morning routine sets the tone for your day. "
                "Charge your phone outside the bedroom. "
                "Wait at least 30 minutes after waking before checking your phone. "
                "Start with intention-setting or journaling instead."
            ),
        )

    def detect_notification_reactive(
        self, sessions: list[UsageSession]
    ) -> DetectedPattern | None:
        """Detect notification-reactive behavior."""
        high_notification_sessions = [
            s for s in sessions
            if s.notifications_received > 5 and s.duration_minutes < 5
        ]

        if len(high_notification_sessions) < 3:
            return None

        return DetectedPattern(
            pattern_type=PatternType.NOTIFICATION_REACTIVE,
            severity="moderate",
            description=(
                f"Detected {len(high_notification_sessions)} instances of "
                f"opening apps briefly in response to notifications."
            ),
            evidence=[
                f"{s.app_name}: {s.notifications_received} notifications, "
                f"{s.duration_minutes:.0f} min session"
                for s in high_notification_sessions[:5]
            ],
            recommendation=(
                "You are reacting to notifications rather than using your phone intentionally. "
                "Turn off notifications for non-essential apps. "
                "Use notification summary/digest features. "
                "Batch-check messages at set intervals."
            ),
        )

    def detect_context_switching(
        self, sessions: list[UsageSession]
    ) -> DetectedPattern | None:
        """Detect rapid context switching between apps."""
        if len(sessions) < self.CONTEXT_SWITCH_THRESHOLD:
            return None

        sorted_sessions = sorted(sessions, key=lambda s: s.start_time)
        rapid_switches = 0
        switch_pairs: list[str] = []

        for i in range(1, len(sorted_sessions)):
            gap = (
                sorted_sessions[i].start_time - sorted_sessions[i - 1].end_time
            ).total_seconds()
            if gap < 60 and sorted_sessions[i].app_name != sorted_sessions[i - 1].app_name:
                rapid_switches += 1
                switch_pairs.append(
                    f"{sorted_sessions[i - 1].app_name} -> {sorted_sessions[i].app_name}"
                )

        if rapid_switches < 5:
            return None

        severity = "high" if rapid_switches > 20 else "moderate"

        return DetectedPattern(
            pattern_type=PatternType.CONTEXT_SWITCHING,
            severity=severity,
            description=(
                f"Detected {rapid_switches} rapid app switches, indicating "
                f"fragmented attention."
            ),
            evidence=switch_pairs[:5],
            recommendation=(
                "Rapid context-switching fragments your attention and reduces focus. "
                "Try single-tasking: use one app at a time for a set period. "
                "Close unused apps to reduce temptation to switch."
            ),
        )
