"""Command-line interface for Vairagya digital detox coach."""

from __future__ import annotations

from datetime import datetime, timedelta

import click
from rich.console import Console

from vairagya.coach.advisor import WellnessAdvisor
from vairagya.coach.challenges import DetoxChallengeGenerator
from vairagya.coach.goals import DetoxGoalManager
from vairagya.models import AppCategory, ChallengeDifficulty
from vairagya.monitor.notifications import NotificationAnalyzer
from vairagya.monitor.patterns import UsagePatternDetector
from vairagya.monitor.screen_time import ScreenTimeTracker
from vairagya.report import ReportGenerator
from vairagya.simulator import UsageSimulator

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """Vairagya - Digital Detox Coach.

    Monitor screen time, detect addictive patterns, and cultivate
    healthy digital habits.
    """
    pass


@cli.command()
@click.option("--app", "app_name", default="Instagram", help="App name")
@click.option(
    "--category", type=click.Choice([c.value for c in AppCategory], case_sensitive=False),
    default=None, help="App category",
)
@click.option("--duration", "-d", default=30, type=int, help="Duration in minutes")
@click.option("--simulate", is_flag=True, help="Use simulated data")
def track(app_name: str, category: str | None, duration: int, simulate: bool) -> None:
    """Track screen time usage."""
    report = ReportGenerator(console)

    if simulate:
        simulator = UsageSimulator()
        sessions = simulator.simulate_day(intensity="heavy")
        tracker = ScreenTimeTracker()
        tracker.sessions = sessions
        summary = tracker.get_daily_summary(sessions[0].start_time)
        report.display_daily_summary(summary)
    else:
        tracker = ScreenTimeTracker()
        cat = AppCategory(category) if category else None
        now = datetime.now()
        tracker.log_session(
            app_name=app_name,
            start_time=now - timedelta(minutes=duration),
            end_time=now,
            category=cat,
        )
        summary = tracker.get_daily_summary(now)
        report.display_daily_summary(summary)


@cli.command()
@click.option("--simulate", is_flag=True, help="Use simulated data")
def notifications(simulate: bool) -> None:
    """Analyze notification patterns."""
    report = ReportGenerator(console)

    if simulate:
        import random
        analyzer = NotificationAnalyzer()
        now = datetime.now()
        apps = ["Instagram", "WhatsApp", "Slack", "Gmail", "Twitter", "TikTok"]

        for _ in range(80):
            app = random.choice(apps)
            ts = now.replace(
                hour=random.randint(7, 23),
                minute=random.randint(0, 59),
            )
            analyzer.add_notification(
                app_name=app,
                timestamp=ts,
                was_opened=random.random() > 0.4,
                response_time_seconds=random.uniform(5, 300) if random.random() > 0.3 else None,
            )

        stats = analyzer.calculate_interruption_cost()
        report.display_notification_report(stats)

        response_patterns = analyzer.analyze_response_patterns()
        console.print(
            f"\n[bold]Response Pattern:[/bold] {response_patterns['pattern']}"
        )
        if "description" in response_patterns:
            console.print(f"  {response_patterns['description']}")
    else:
        console.print("[dim]Use --simulate to see a demo with generated data[/dim]")


@cli.command()
@click.option("--simulate", is_flag=True, help="Use simulated data")
def patterns(simulate: bool) -> None:
    """Detect addictive usage patterns."""
    report = ReportGenerator(console)

    if simulate:
        simulator = UsageSimulator()
        sessions = simulator.simulate_doom_scrolling_day()
        detector = UsagePatternDetector()

        tracker = ScreenTimeTracker()
        tracker.sessions = sessions
        summary = tracker.get_daily_summary(sessions[0].start_time)

        detected = detector.detect_all_patterns(sessions, summary)
        report.display_patterns(detected)
    else:
        console.print("[dim]Use --simulate to see a demo with generated data[/dim]")


@cli.group()
def goals() -> None:
    """Manage detox goals."""
    pass


@goals.command("set")
@click.option(
    "--category", type=click.Choice([c.value for c in AppCategory], case_sensitive=False),
    default="social_media", help="Category to limit",
)
@click.option("--daily-limit", default=30, type=int, help="Daily limit in minutes")
@click.option("--current-avg", default=120, type=float, help="Current daily average in minutes")
def set_goal(category: str, daily_limit: int, current_avg: float) -> None:
    """Set a new detox goal."""
    manager = DetoxGoalManager()
    cat = AppCategory(category)
    goal = manager.set_goal(
        daily_limit_minutes=daily_limit,
        category=cat,
        current_average=current_avg,
    )

    report = ReportGenerator(console)
    console.print(f"\n[bold green]Goal created![/bold green] ID: {goal.goal_id}")
    console.print(f"  Category: {category}")
    console.print(f"  Daily limit: {daily_limit} minutes")
    console.print(f"  Current average: {current_avg} minutes")
    console.print(f"  Target reduction: {goal.reduction_target_percent:.1f}%")

    plan = manager.suggest_gradual_reduction(current_avg, daily_limit)
    report.display_reduction_plan(plan)


@cli.command()
@click.option(
    "--difficulty",
    type=click.Choice(["easy", "medium", "hard", "extreme"], case_sensitive=False),
    default=None, help="Challenge difficulty",
)
def challenge(difficulty: str | None) -> None:
    """Get a digital detox challenge."""
    generator = DetoxChallengeGenerator()
    diff = ChallengeDifficulty(difficulty) if difficulty else None
    ch = generator.get_random_challenge(difficulty=diff)

    report = ReportGenerator(console)
    report.display_challenge(ch)


@cli.command()
@click.option("--simulate", is_flag=True, help="Use simulated data")
def advise(simulate: bool) -> None:
    """Get personalized wellness advice."""
    advisor = WellnessAdvisor()

    if simulate:
        simulator = UsageSimulator()
        sessions = simulator.simulate_day(intensity="heavy")
        tracker = ScreenTimeTracker()
        tracker.sessions = sessions
        summary = tracker.get_daily_summary(sessions[0].start_time)

        detector = UsagePatternDetector()
        detected = detector.detect_all_patterns(sessions, summary)

        advice = advisor.get_advice_for_usage(summary)
        advice += advisor.get_advice_for_patterns(detected)

        report = ReportGenerator(console)
        report.display_advice(advice)

        console.print("\n[bold]Weekly Reflection Prompts:[/bold]")
        for prompt in advisor.get_weekly_reflection_prompts()[:3]:
            console.print(f"  - {prompt}")
    else:
        advice = advisor.GENERAL_ADVICE[:5]
        report = ReportGenerator(console)
        report.display_advice(advice)


@cli.command()
@click.option("--simulate", is_flag=True, help="Use simulated data")
def report(simulate: bool) -> None:
    """Generate a comprehensive usage report."""
    rpt = ReportGenerator(console)

    if simulate:
        simulator = UsageSimulator()
        sessions = simulator.simulate_day(intensity="heavy")
        tracker = ScreenTimeTracker()
        tracker.sessions = sessions
        summary = tracker.get_daily_summary(sessions[0].start_time)

        rpt.display_daily_summary(summary)

        detector = UsagePatternDetector()
        detected = detector.detect_all_patterns(sessions, summary)
        rpt.display_patterns(detected)

        advisor = WellnessAdvisor()
        advice = advisor.get_advice_for_usage(summary)
        rpt.display_advice(advice)

        console.print(advisor.get_motivation_message(0))
    else:
        console.print("[dim]Use --simulate for a full demo report[/dim]")


if __name__ == "__main__":
    cli()
