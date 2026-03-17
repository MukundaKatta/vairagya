"""Wellness advisor generating personalized reduction strategies."""

from __future__ import annotations

from vairagya.models import AppCategory, DetectedPattern, PatternType, ScreenTime


class WellnessAdvisor:
    """Generate personalized digital wellness advice based on usage patterns."""

    CATEGORY_ADVICE: dict[str, list[str]] = {
        AppCategory.SOCIAL_MEDIA.value: [
            "Curate your feed ruthlessly - unfollow accounts that trigger comparison or negativity.",
            "Set specific times for social media instead of checking impulsively.",
            "Replace one daily scroll session with calling a friend or meeting in person.",
            "Move social media apps off your home screen to add friction.",
            "Ask yourself before posting: Am I sharing, or seeking validation?",
            "Try a 'consume less, create more' approach to social media.",
        ],
        AppCategory.ENTERTAINMENT.value: [
            "Turn off auto-play on streaming services to create natural stopping points.",
            "Decide what to watch before opening the app - no browsing allowed.",
            "Set a 2-episode maximum per sitting.",
            "Replace one evening of streaming with a creative hobby.",
            "Try podcasts or audiobooks as lower-stimulation alternatives.",
        ],
        AppCategory.COMMUNICATION.value: [
            "Batch your email and message checking to 3 times per day.",
            "Use auto-responders to set expectations about response times.",
            "Distinguish between urgent and non-urgent communications.",
            "Turn off read receipts to reduce social pressure to respond immediately.",
            "Schedule 'office hours' for non-urgent conversations.",
        ],
        AppCategory.NEWS.value: [
            "Choose one trustworthy news source instead of many.",
            "Set a daily time limit for news consumption (15-20 minutes).",
            "Avoid news before bed - it activates your stress response.",
            "Subscribe to a daily news digest instead of checking constantly.",
            "Remember: being informed doesn't require being overwhelmed.",
        ],
        AppCategory.GAMING.value: [
            "Set a timer before you start gaming and respect it.",
            "Remove games with loot boxes or addictive reward mechanics.",
            "Play games that have natural stopping points (no infinite modes).",
            "Replace mobile gaming with physical puzzles or board games.",
            "Track your gaming time honestly - awareness is the first step.",
        ],
        AppCategory.SHOPPING.value: [
            "Remove saved payment methods to add friction to impulse buying.",
            "Implement a 24-hour rule: wait a day before purchasing anything.",
            "Unsubscribe from all promotional emails.",
            "Delete shopping apps and only shop from a computer with intention.",
            "Keep a wishlist instead of buying immediately.",
        ],
    }

    PATTERN_ADVICE: dict[PatternType, list[str]] = {
        PatternType.DOOM_SCROLLING: [
            "Set a physical timer for 10 minutes when you open social media.",
            "When you catch yourself scrolling mindlessly, do 10 deep breaths.",
            "Replace infinite feeds with finite content (newsletters, specific blogs).",
            "Use 'one and done' rule: open the app, check what you need, close it.",
        ],
        PatternType.CHECKING_FREQUENCY: [
            "Put your phone in a drawer or bag during work hours.",
            "Use a physical watch so you don't pick up your phone to check time.",
            "Set up a phone-free zone at your desk.",
            "Try the Pomodoro technique: 25 min focused work, 5 min break.",
        ],
        PatternType.LATE_NIGHT_USE: [
            "Set a digital curfew 1 hour before your target bedtime.",
            "Use Night Shift/blue light filter after sunset.",
            "Create a screen-free bedtime routine: reading, stretching, journaling.",
            "Charge your phone outside the bedroom.",
        ],
        PatternType.BINGE_WATCHING: [
            "Watch with intention: decide the number of episodes beforehand.",
            "Turn off auto-play features on all streaming services.",
            "After each episode, stand up and do a 5-minute activity.",
            "Try replacing TV with podcasts during chores.",
        ],
        PatternType.NOTIFICATION_REACTIVE: [
            "Turn off all non-essential notifications immediately.",
            "Use notification summary features (iOS 15+, Android 12+).",
            "Batch-check messages at predetermined times.",
            "Reclaim your attention: you choose when to engage, not your phone.",
        ],
        PatternType.FIRST_THING_MORNING: [
            "Charge your phone in another room overnight.",
            "Buy a physical alarm clock.",
            "Create a morning routine that doesn't involve screens for 30+ minutes.",
            "Start your day with intention: journal, meditate, exercise.",
        ],
        PatternType.CONTEXT_SWITCHING: [
            "Practice single-tasking: one app, one purpose, one session.",
            "Close all apps before opening a new one.",
            "Use Focus modes to limit available apps during certain activities.",
            "Recognize that multitasking is a myth - you're just switching poorly.",
        ],
    }

    GENERAL_ADVICE = [
        "Digital wellness is a practice, not a destination. Be patient with yourself.",
        "Small consistent changes beat dramatic unsustainable ones.",
        "Your phone is a tool. You should control it, not the other way around.",
        "The goal isn't zero screen time - it's intentional screen time.",
        "Every time you resist the urge to check your phone, you strengthen your willpower.",
        "Replace digital habits with physical ones: books, walks, conversations.",
        "Track your progress - seeing improvement is motivating.",
        "Tell someone about your digital wellness goals for accountability.",
        "Celebrate screen-free time instead of mourning missed content.",
        "Ask yourself: In 5 years, will I wish I had scrolled more or lived more?",
    ]

    def get_advice_for_usage(self, daily_summary: ScreenTime) -> list[str]:
        """Generate personalized advice based on daily usage data."""
        advice: list[str] = []

        # Advice based on total usage
        if daily_summary.total_minutes > 300:
            advice.append(
                f"You spent {daily_summary.total_minutes:.0f} minutes on screens today "
                f"({daily_summary.total_minutes / 60:.1f} hours). "
                f"Consider which activities truly added value to your day."
            )

        # Category-specific advice
        for category, minutes in sorted(
            daily_summary.by_category.items(), key=lambda x: x[1], reverse=True
        ):
            if category in self.CATEGORY_ADVICE and minutes > 30:
                import random
                cat_advice = random.choice(self.CATEGORY_ADVICE[category])
                advice.append(
                    f"{category.replace('_', ' ').title()} ({minutes:.0f} min): {cat_advice}"
                )

        # Pickup advice
        if daily_summary.total_pickups > 50:
            advice.append(
                f"You picked up your device {daily_summary.total_pickups} times today. "
                f"Each pickup is an attention interruption."
            )

        # General advice if no specific issues found
        if not advice:
            import random
            advice.append(random.choice(self.GENERAL_ADVICE))

        return advice

    def get_advice_for_patterns(
        self, patterns: list[DetectedPattern]
    ) -> list[str]:
        """Generate advice based on detected usage patterns."""
        advice: list[str] = []

        for pattern in patterns:
            pattern_advice = self.PATTERN_ADVICE.get(pattern.pattern_type, [])
            if pattern_advice:
                import random
                selected = random.sample(
                    pattern_advice, min(2, len(pattern_advice))
                )
                for a in selected:
                    advice.append(
                        f"[{pattern.pattern_type.value.replace('_', ' ').title()}] {a}"
                    )

        return advice

    def get_weekly_reflection_prompts(self) -> list[str]:
        """Get prompts for weekly digital wellness reflection."""
        return [
            "What was your most meaningful offline moment this week?",
            "Which app consumed the most time that you wish you'd spent differently?",
            "Did you notice any emotional triggers that led to screen use?",
            "What did you gain from your screen-free time?",
            "What boundaries worked well? What needs adjustment?",
            "How did your sleep quality compare on high vs. low screen time days?",
            "What offline activity would you like to try next week?",
        ]

    def get_motivation_message(self, streak_days: int) -> str:
        """Get a motivational message based on streak length."""
        if streak_days == 0:
            return "Every journey begins with a single step. Start your digital wellness journey today."
        elif streak_days < 3:
            return f"Day {streak_days}! The first few days are the hardest. You're building a new habit."
        elif streak_days < 7:
            return f"{streak_days}-day streak! You're rewiring your brain's reward pathways. Keep going!"
        elif streak_days < 14:
            return f"{streak_days} days strong! Research shows habits start forming around day 7. You're on track!"
        elif streak_days < 30:
            return f"Incredible - {streak_days} days! You've proven you don't need constant digital stimulation."
        else:
            return f"{streak_days} days of intentional living! You've transformed your relationship with technology."
