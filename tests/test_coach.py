"""Tests for coaching modules."""

import pytest
from datetime import datetime

from vairagya.coach.advisor import WellnessAdvisor
from vairagya.coach.challenges import DetoxChallengeGenerator
from vairagya.coach.goals import DetoxGoalManager
from vairagya.models import AppCategory, ChallengeDifficulty, ScreenTime


class TestDetoxGoalManager:
    def test_set_goal(self) -> None:
        manager = DetoxGoalManager()
        goal = manager.set_goal(
            daily_limit_minutes=30,
            category=AppCategory.SOCIAL_MEDIA,
            current_average=120,
        )
        assert goal.goal_id == "GOAL001"
        assert goal.daily_limit_minutes == 30
        assert goal.category == AppCategory.SOCIAL_MEDIA

    def test_goal_reduction_target(self) -> None:
        manager = DetoxGoalManager()
        goal = manager.set_goal(daily_limit_minutes=30, current_average=120)
        assert goal.reduction_target_percent == 75.0

    def test_check_goal_met(self) -> None:
        manager = DetoxGoalManager()
        goal = manager.set_goal(
            daily_limit_minutes=30,
            category=AppCategory.SOCIAL_MEDIA,
        )
        summary = ScreenTime(
            by_category={"social_media": 25},
            total_minutes=100,
        )
        result = manager.check_goal(goal, summary)
        assert result["met"] is True
        assert result["actual_minutes"] == 25
        assert result["streak_days"] == 1

    def test_check_goal_not_met(self) -> None:
        manager = DetoxGoalManager()
        goal = manager.set_goal(
            daily_limit_minutes=30,
            category=AppCategory.SOCIAL_MEDIA,
        )
        summary = ScreenTime(
            by_category={"social_media": 60},
            total_minutes=200,
        )
        result = manager.check_goal(goal, summary)
        assert result["met"] is False
        assert result["over_by_minutes"] == 30

    def test_streak_resets_on_miss(self) -> None:
        manager = DetoxGoalManager()
        goal = manager.set_goal(
            daily_limit_minutes=30,
            category=AppCategory.SOCIAL_MEDIA,
        )
        good = ScreenTime(by_category={"social_media": 20}, total_minutes=50)
        bad = ScreenTime(by_category={"social_media": 60}, total_minutes=100)

        manager.check_goal(goal, good)
        assert goal.streak_days == 1
        manager.check_goal(goal, bad)
        assert goal.streak_days == 0

    def test_gradual_reduction_plan(self) -> None:
        manager = DetoxGoalManager()
        plan = manager.suggest_gradual_reduction(
            current_average=120, target_minutes=30, weeks=4
        )
        assert len(plan) == 4
        assert plan[0]["target_minutes"] > plan[-1]["target_minutes"]
        assert plan[-1]["target_minutes"] == 30

    def test_recommended_limits(self) -> None:
        manager = DetoxGoalManager()
        limit = manager.get_recommended_limit(AppCategory.SOCIAL_MEDIA)
        assert limit == 30

    def test_get_active_goals(self) -> None:
        manager = DetoxGoalManager()
        manager.set_goal(daily_limit_minutes=30, category=AppCategory.SOCIAL_MEDIA)
        manager.set_goal(daily_limit_minutes=60, category=AppCategory.ENTERTAINMENT)
        assert len(manager.get_active_goals()) == 2

    def test_deactivate_goal(self) -> None:
        manager = DetoxGoalManager()
        goal = manager.set_goal(daily_limit_minutes=30)
        assert manager.deactivate_goal(goal.goal_id)
        assert len(manager.get_active_goals()) == 0

    def test_goal_summary(self) -> None:
        manager = DetoxGoalManager()
        manager.set_goal(daily_limit_minutes=30, category=AppCategory.SOCIAL_MEDIA, current_average=90)
        summaries = manager.get_goal_summary()
        assert len(summaries) == 1
        assert summaries[0]["target"] == "social_media"


class TestDetoxChallengeGenerator:
    def test_get_random_challenge(self) -> None:
        gen = DetoxChallengeGenerator()
        ch = gen.get_random_challenge()
        assert ch.title
        assert ch.description
        assert ch.duration_days >= 1
        assert len(ch.rules) > 0

    def test_get_challenge_by_difficulty(self) -> None:
        gen = DetoxChallengeGenerator()
        ch = gen.get_random_challenge(difficulty=ChallengeDifficulty.EASY)
        assert ch.difficulty == ChallengeDifficulty.EASY

    def test_get_all_challenges(self) -> None:
        gen = DetoxChallengeGenerator()
        all_ch = gen.get_all_challenges()
        assert len(all_ch) >= 20  # Must have 20+ challenges

    def test_challenges_have_rules_and_tips(self) -> None:
        gen = DetoxChallengeGenerator()
        for ch in gen.get_all_challenges():
            assert len(ch.rules) > 0, f"Challenge '{ch.title}' has no rules"
            assert len(ch.tips) > 0, f"Challenge '{ch.title}' has no tips"

    def test_all_difficulties_represented(self) -> None:
        gen = DetoxChallengeGenerator()
        all_ch = gen.get_all_challenges()
        difficulties = {ch.difficulty for ch in all_ch}
        assert ChallengeDifficulty.EASY in difficulties
        assert ChallengeDifficulty.MEDIUM in difficulties
        assert ChallengeDifficulty.HARD in difficulties
        assert ChallengeDifficulty.EXTREME in difficulties

    def test_progressive_plan(self) -> None:
        gen = DetoxChallengeGenerator()
        plan = gen.get_progressive_plan(weeks=4)
        assert len(plan) == 4
        # Should progress from easy to harder
        assert plan[0].difficulty == ChallengeDifficulty.EASY
        assert plan[-1].difficulty == ChallengeDifficulty.EXTREME

    def test_filter_by_category(self) -> None:
        gen = DetoxChallengeGenerator()
        ch = gen.get_random_challenge(category=AppCategory.SOCIAL_MEDIA)
        # Should return a challenge (either category-specific or general)
        assert ch is not None


class TestWellnessAdvisor:
    def test_advice_for_heavy_usage(self) -> None:
        advisor = WellnessAdvisor()
        summary = ScreenTime(
            total_minutes=400,
            by_category={"social_media": 120, "entertainment": 150},
        )
        advice = advisor.get_advice_for_usage(summary)
        assert len(advice) > 0
        # Should mention total minutes
        assert any("400" in a or "screen" in a.lower() for a in advice)

    def test_advice_for_patterns(self) -> None:
        advisor = WellnessAdvisor()
        from vairagya.models import DetectedPattern, PatternType
        patterns = [
            DetectedPattern(
                pattern_type=PatternType.DOOM_SCROLLING,
                severity="high",
                description="Detected doom scrolling",
            ),
        ]
        advice = advisor.get_advice_for_patterns(patterns)
        assert len(advice) > 0

    def test_weekly_reflection_prompts(self) -> None:
        advisor = WellnessAdvisor()
        prompts = advisor.get_weekly_reflection_prompts()
        assert len(prompts) >= 5

    def test_motivation_messages(self) -> None:
        advisor = WellnessAdvisor()
        assert "journey" in advisor.get_motivation_message(0).lower() or "step" in advisor.get_motivation_message(0).lower()
        assert "streak" in advisor.get_motivation_message(5).lower() or "day" in advisor.get_motivation_message(5).lower()
        assert len(advisor.get_motivation_message(30)) > 0

    def test_general_advice_exists(self) -> None:
        advisor = WellnessAdvisor()
        assert len(advisor.GENERAL_ADVICE) >= 5

    def test_category_advice_coverage(self) -> None:
        advisor = WellnessAdvisor()
        assert AppCategory.SOCIAL_MEDIA.value in advisor.CATEGORY_ADVICE
        assert AppCategory.ENTERTAINMENT.value in advisor.CATEGORY_ADVICE
        assert AppCategory.NEWS.value in advisor.CATEGORY_ADVICE
