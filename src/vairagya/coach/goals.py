"""Detox goal management - set and track screen time limits."""

from __future__ import annotations

from datetime import datetime

from vairagya.models import AppCategory, DetoxGoal, ScreenTime


class DetoxGoalManager:
    """Manage digital detox goals and track compliance."""

    # Recommended daily limits by category (minutes)
    RECOMMENDED_LIMITS: dict[str, int] = {
        AppCategory.SOCIAL_MEDIA.value: 30,
        AppCategory.ENTERTAINMENT.value: 60,
        AppCategory.COMMUNICATION.value: 45,
        AppCategory.NEWS.value: 20,
        AppCategory.GAMING.value: 30,
        AppCategory.SHOPPING.value: 15,
        AppCategory.BROWSING.value: 30,
    }

    def __init__(self) -> None:
        self.goals: list[DetoxGoal] = []
        self._goal_counter = 0

    def set_goal(
        self,
        daily_limit_minutes: int,
        category: AppCategory | None = None,
        app_name: str | None = None,
        current_average: float = 0,
        target_date: datetime | None = None,
    ) -> DetoxGoal:
        """Create a new detox goal."""
        self._goal_counter += 1
        goal_id = f"GOAL{self._goal_counter:03d}"

        goal = DetoxGoal(
            goal_id=goal_id,
            category=category,
            app_name=app_name,
            daily_limit_minutes=daily_limit_minutes,
            current_average_minutes=current_average,
            target_date=target_date,
        )
        self.goals.append(goal)
        return goal

    def check_goal(self, goal: DetoxGoal, daily_usage: ScreenTime) -> dict:
        """Check if a goal was met for a given day."""
        if goal.category:
            actual = daily_usage.by_category.get(goal.category.value, 0)
        elif goal.app_name:
            actual = daily_usage.by_app.get(goal.app_name, 0)
        else:
            actual = daily_usage.total_minutes

        met = actual <= goal.daily_limit_minutes
        over_by = max(0, actual - goal.daily_limit_minutes)
        under_by = max(0, goal.daily_limit_minutes - actual)

        goal.total_days_tracked += 1
        if met:
            goal.total_days_met += 1
            goal.streak_days += 1
        else:
            goal.streak_days = 0

        return {
            "goal_id": goal.goal_id,
            "met": met,
            "actual_minutes": round(actual, 1),
            "limit_minutes": goal.daily_limit_minutes,
            "over_by_minutes": round(over_by, 1),
            "under_by_minutes": round(under_by, 1),
            "streak_days": goal.streak_days,
            "compliance_rate": goal.compliance_rate,
        }

    def get_recommended_limit(self, category: AppCategory) -> int:
        """Get the recommended daily limit for a category."""
        return self.RECOMMENDED_LIMITS.get(category.value, 30)

    def suggest_gradual_reduction(
        self,
        current_average: float,
        target_minutes: int,
        weeks: int = 4,
    ) -> list[dict]:
        """Suggest a gradual reduction plan over several weeks."""
        if current_average <= target_minutes:
            return [{"week": 1, "target_minutes": target_minutes, "reduction": 0}]

        total_reduction = current_average - target_minutes
        weekly_reduction = total_reduction / weeks

        plan: list[dict] = []
        for week in range(1, weeks + 1):
            week_target = max(
                target_minutes,
                round(current_average - weekly_reduction * week),
            )
            plan.append({
                "week": week,
                "target_minutes": week_target,
                "reduction_from_current": round(current_average - week_target),
                "reduction_percent": round(
                    (current_average - week_target) / current_average * 100, 1
                ),
            })

        return plan

    def get_active_goals(self) -> list[DetoxGoal]:
        """Get all active goals."""
        return [g for g in self.goals if g.is_active]

    def deactivate_goal(self, goal_id: str) -> bool:
        """Deactivate a goal."""
        for goal in self.goals:
            if goal.goal_id == goal_id:
                goal.is_active = False
                return True
        return False

    def get_goal_summary(self) -> list[dict]:
        """Get a summary of all goals and their status."""
        summaries: list[dict] = []
        for goal in self.goals:
            target = goal.category.value if goal.category else goal.app_name or "total"
            summaries.append({
                "goal_id": goal.goal_id,
                "target": target,
                "daily_limit": goal.daily_limit_minutes,
                "current_average": goal.current_average_minutes,
                "reduction_target": f"{goal.reduction_target_percent:.1f}%",
                "compliance_rate": f"{goal.compliance_rate:.1f}%",
                "streak_days": goal.streak_days,
                "is_active": goal.is_active,
            })
        return summaries
