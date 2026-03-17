"""Rich-formatted reports for digital detox data."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from vairagya.models import (
    Challenge,
    DetectedPattern,
    DetoxGoal,
    ScreenTime,
)


class ReportGenerator:
    """Generate rich-formatted digital wellness reports."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def display_daily_summary(self, summary: ScreenTime) -> None:
        """Display a daily screen time summary."""
        hours = summary.total_minutes / 60

        self.console.print()
        self.console.print(
            Panel(
                f"[bold]Date:[/bold] {summary.date.strftime('%Y-%m-%d')}  |  "
                f"[bold]Total:[/bold] {summary.total_minutes:.0f} min ({hours:.1f} hrs)  |  "
                f"[bold]Pickups:[/bold] {summary.total_pickups}  |  "
                f"[bold]Notifications:[/bold] {summary.total_notifications}",
                title="[bold blue]Daily Screen Time Report[/bold blue]",
                border_style="blue",
            )
        )

        # Category breakdown table
        if summary.by_category:
            table = Table(title="Usage by Category", border_style="cyan")
            table.add_column("Category", style="bold")
            table.add_column("Minutes", justify="right")
            table.add_column("Hours", justify="right")
            table.add_column("% of Total", justify="right")
            table.add_column("Bar", min_width=20)

            sorted_cats = sorted(
                summary.by_category.items(), key=lambda x: x[1], reverse=True
            )
            max_minutes = max(summary.by_category.values()) if summary.by_category else 1

            for category, minutes in sorted_cats:
                pct = minutes / summary.total_minutes * 100 if summary.total_minutes > 0 else 0
                bar_len = int(minutes / max_minutes * 20)
                bar = "[green]" + "#" * bar_len + "[/green]"

                color = "red" if pct > 30 else "yellow" if pct > 15 else "green"

                table.add_row(
                    category.replace("_", " ").title(),
                    f"{minutes:.0f}",
                    f"{minutes / 60:.1f}",
                    f"[{color}]{pct:.1f}%[/{color}]",
                    bar,
                )

            self.console.print(table)

        # Top apps table
        if summary.by_app:
            table = Table(title="Top Apps", border_style="magenta")
            table.add_column("App", style="bold")
            table.add_column("Minutes", justify="right")

            sorted_apps = sorted(
                summary.by_app.items(), key=lambda x: x[1], reverse=True
            )[:10]
            for app, minutes in sorted_apps:
                table.add_row(app, f"{minutes:.0f}")

            self.console.print(table)

        # First/last use times
        if summary.first_use_time:
            self.console.print(
                f"  [dim]First use:[/dim] {summary.first_use_time.strftime('%H:%M')}  "
                f"[dim]Last use:[/dim] {summary.last_use_time.strftime('%H:%M') if summary.last_use_time else 'N/A'}"
            )
        self.console.print()

    def display_patterns(self, patterns: list[DetectedPattern]) -> None:
        """Display detected usage patterns."""
        if not patterns:
            self.console.print(
                Panel(
                    "[green]No addictive patterns detected. Keep it up![/green]",
                    title="[bold green]Pattern Analysis[/bold green]",
                    border_style="green",
                )
            )
            return

        self.console.print()
        self.console.print(
            Panel(
                f"[bold yellow]{len(patterns)} pattern(s) detected[/bold yellow]",
                title="[bold yellow]Pattern Analysis[/bold yellow]",
                border_style="yellow",
            )
        )

        severity_styles = {
            "high": "bold red",
            "moderate": "bold yellow",
            "low": "bold green",
        }

        for pattern in patterns:
            style = severity_styles.get(pattern.severity, "white")
            evidence_str = "\n".join(f"  - {e}" for e in pattern.evidence[:4])

            self.console.print(
                Panel(
                    f"[bold]Pattern:[/bold] {pattern.pattern_type.value.replace('_', ' ').title()}\n"
                    f"[bold]Severity:[/bold] [{style}]{pattern.severity.upper()}[/{style}]\n"
                    f"[bold]Description:[/bold] {pattern.description}\n\n"
                    f"[bold]Evidence:[/bold]\n{evidence_str}\n\n"
                    f"[bold]Recommendation:[/bold] {pattern.recommendation}",
                    border_style="red" if pattern.severity == "high" else "yellow",
                )
            )

        self.console.print()

    def display_goals(self, goals: list[dict]) -> None:
        """Display goal tracking summary."""
        table = Table(title="Detox Goals", border_style="blue")
        table.add_column("Goal ID", style="bold")
        table.add_column("Target")
        table.add_column("Daily Limit", justify="right")
        table.add_column("Current Avg", justify="right")
        table.add_column("Reduction", justify="right")
        table.add_column("Compliance", justify="right")
        table.add_column("Streak", justify="center")
        table.add_column("Active", justify="center")

        for goal in goals:
            active_str = "[green]Yes[/green]" if goal["is_active"] else "[dim]No[/dim]"
            table.add_row(
                goal["goal_id"],
                goal["target"],
                f"{goal['daily_limit']} min",
                f"{goal['current_average']:.0f} min",
                goal["reduction_target"],
                goal["compliance_rate"],
                str(goal["streak_days"]),
                active_str,
            )

        self.console.print()
        self.console.print(table)
        self.console.print()

    def display_challenge(self, challenge: Challenge) -> None:
        """Display a challenge."""
        diff_colors = {
            "easy": "green",
            "medium": "yellow",
            "hard": "red",
            "extreme": "bold red",
        }
        color = diff_colors.get(challenge.difficulty.value, "white")

        rules_str = "\n".join(f"  {i}. {r}" for i, r in enumerate(challenge.rules, 1))
        tips_str = "\n".join(f"  - {t}" for t in challenge.tips)

        self.console.print()
        self.console.print(
            Panel(
                f"[bold]{challenge.title}[/bold]\n\n"
                f"{challenge.description}\n\n"
                f"[bold]Difficulty:[/bold] [{color}]{challenge.difficulty.value.upper()}[/{color}]\n"
                f"[bold]Duration:[/bold] {challenge.duration_days} day(s)\n\n"
                f"[bold]Rules:[/bold]\n{rules_str}\n\n"
                f"[bold]Tips:[/bold]\n{tips_str}",
                title="[bold magenta]Digital Detox Challenge[/bold magenta]",
                border_style="magenta",
            )
        )
        self.console.print()

    def display_advice(self, advice_list: list[str]) -> None:
        """Display wellness advice."""
        self.console.print()
        self.console.print(
            Panel(
                "\n\n".join(f"  {a}" for a in advice_list),
                title="[bold cyan]Wellness Advice[/bold cyan]",
                border_style="cyan",
            )
        )
        self.console.print()

    def display_notification_report(self, stats: dict) -> None:
        """Display notification analysis."""
        self.console.print()
        self.console.print(
            Panel(
                f"[bold]Total Notifications:[/bold] {stats['total_notifications']}\n"
                f"[bold]Opened:[/bold] {stats['total_opened']} ({stats['open_rate_percent']}%)\n"
                f"[bold]Avg Response Time:[/bold] {stats['average_response_seconds']}s\n"
                f"[bold]Estimated Time Lost:[/bold] {stats['estimated_lost_minutes']} min "
                f"({stats['estimated_lost_hours']} hrs)\n"
                f"[bold]Top Interrupter:[/bold] {stats['top_interrupter']}",
                title="[bold yellow]Notification Analysis[/bold yellow]",
                border_style="yellow",
            )
        )
        self.console.print()

    def display_reduction_plan(self, plan: list[dict]) -> None:
        """Display a gradual reduction plan."""
        table = Table(title="Gradual Reduction Plan", border_style="green")
        table.add_column("Week", justify="center", style="bold")
        table.add_column("Target (min)", justify="right")
        table.add_column("Reduction", justify="right")
        table.add_column("% Reduced", justify="right")

        for week in plan:
            table.add_row(
                str(week["week"]),
                str(week["target_minutes"]),
                f"{week['reduction_from_current']} min",
                f"{week['reduction_percent']}%",
            )

        self.console.print()
        self.console.print(table)
        self.console.print()
