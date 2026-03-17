"""Digital detox challenge generator with 20+ wellness challenges."""

from __future__ import annotations

import random

from vairagya.models import AppCategory, Challenge, ChallengeDifficulty


class DetoxChallengeGenerator:
    """Generate digital wellness challenges for gradual detox.

    Contains 25+ curated challenges across difficulty levels.
    """

    CHALLENGES: list[dict] = [
        # EASY challenges
        {
            "title": "Notification Silence",
            "description": "Turn off all non-essential notifications for 24 hours.",
            "difficulty": ChallengeDifficulty.EASY,
            "duration_days": 1,
            "category": None,
            "rules": [
                "Disable notifications for social media, news, and entertainment apps",
                "Keep only phone calls and direct messages enabled",
                "Check apps manually at scheduled times only",
            ],
            "tips": [
                "You can use Do Not Disturb mode with exceptions for calls",
                "Set 3 specific times to check notifications",
            ],
        },
        {
            "title": "Grayscale Day",
            "description": "Set your phone to grayscale mode for an entire day.",
            "difficulty": ChallengeDifficulty.EASY,
            "duration_days": 1,
            "category": None,
            "rules": [
                "Enable grayscale/accessibility color filter on your device",
                "Keep it on for the full day",
                "Notice how it changes your desire to scroll",
            ],
            "tips": [
                "On iPhone: Settings > Accessibility > Display > Color Filters",
                "On Android: Settings > Digital Wellbeing > Bedtime Mode",
            ],
        },
        {
            "title": "No Phone First Hour",
            "description": "Don't touch your phone for the first hour after waking up.",
            "difficulty": ChallengeDifficulty.EASY,
            "duration_days": 3,
            "category": None,
            "rules": [
                "Use a physical alarm clock instead of your phone",
                "No checking messages, social media, or email for 60 minutes",
                "Spend the time on morning routine, exercise, or journaling",
            ],
            "tips": [
                "Charge your phone in another room overnight",
                "Prepare your morning routine the night before",
            ],
        },
        {
            "title": "App-Free Meals",
            "description": "Put your phone away during all meals for 3 days.",
            "difficulty": ChallengeDifficulty.EASY,
            "duration_days": 3,
            "category": None,
            "rules": [
                "Phone must be in another room or face-down during meals",
                "No watching videos or scrolling while eating",
                "Focus on the food and any company you have",
            ],
            "tips": [
                "Try describing the taste and texture of your food mindfully",
                "Use meal times to connect with family or roommates",
            ],
        },
        {
            "title": "Unsubscribe Marathon",
            "description": "Unsubscribe from 20 email lists and unfollow 50 accounts.",
            "difficulty": ChallengeDifficulty.EASY,
            "duration_days": 1,
            "category": None,
            "rules": [
                "Unsubscribe from at least 20 promotional emails",
                "Unfollow at least 50 social media accounts that don't add value",
                "Turn off email notifications from apps",
            ],
            "tips": [
                "Ask yourself: Does this account inspire or drain me?",
                "Use email unsubscribe tools like Unroll.me",
            ],
        },
        {
            "title": "Analog Evening",
            "description": "No screens after 8 PM for one evening.",
            "difficulty": ChallengeDifficulty.EASY,
            "duration_days": 1,
            "category": None,
            "rules": [
                "Power down all screens by 8 PM",
                "Spend the evening with books, board games, or conversation",
                "Use this time for self-care and relaxation",
            ],
            "tips": [
                "Prepare activities in advance: books, puzzles, art supplies",
                "Let close contacts know you'll be offline",
            ],
        },
        # MEDIUM challenges
        {
            "title": "Social Media Sunset",
            "description": "No social media after 6 PM for one week.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 7,
            "category": AppCategory.SOCIAL_MEDIA,
            "rules": [
                "Delete social media apps from home screen (don't uninstall)",
                "No social media usage between 6 PM and 8 AM",
                "Use the time for hobbies, exercise, or socializing in person",
            ],
            "tips": [
                "Move social apps to a folder on the last page of your phone",
                "Replace scrolling with a 10-minute walk",
            ],
        },
        {
            "title": "One App at a Time",
            "description": "Only use one app at a time. Close everything else.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 5,
            "category": None,
            "rules": [
                "Only have one app open at a time",
                "Close the current app before opening another",
                "No split-screen or picture-in-picture multitasking",
            ],
            "tips": [
                "This trains single-tasking and focused attention",
                "Notice your urge to switch - that's the addiction talking",
            ],
        },
        {
            "title": "News Detox",
            "description": "Limit news consumption to 15 minutes per day for one week.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 7,
            "category": AppCategory.NEWS,
            "rules": [
                "Set a 15-minute daily timer for news reading",
                "Choose one reliable news source instead of many",
                "No doomscrolling through news feeds",
                "No news after 7 PM",
            ],
            "tips": [
                "Try a daily news summary podcast or newsletter instead",
                "Remember: if it's important enough, you'll hear about it",
            ],
        },
        {
            "title": "Digital Sabbath",
            "description": "Take one full day off from non-essential screens.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 1,
            "category": None,
            "rules": [
                "Choose one day per week with no recreational screen time",
                "Only essential communications allowed (emergency calls)",
                "Fill the day with offline activities",
            ],
            "tips": [
                "Plan your offline day in advance with activities",
                "Tell friends and family so they know to call instead of text",
            ],
        },
        {
            "title": "Mindful Scrolling",
            "description": "Before opening any app, state your purpose out loud.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 7,
            "category": None,
            "rules": [
                "Before opening any app, say out loud why you're opening it",
                "Set a time limit for each session before you start",
                "If you can't state a clear purpose, don't open the app",
            ],
            "tips": [
                "Keep a tally of purposeful vs. aimless opens",
                "You'll be surprised how often you open apps for no reason",
            ],
        },
        {
            "title": "Batch Communication",
            "description": "Check messages only 3 times per day for 5 days.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 5,
            "category": AppCategory.COMMUNICATION,
            "rules": [
                "Check and respond to messages only at 9 AM, 1 PM, and 6 PM",
                "No peeking at messages outside these windows",
                "Set an auto-reply if needed",
            ],
            "tips": [
                "Most messages don't require immediate responses",
                "Use this time to practice deep work between check-ins",
            ],
        },
        {
            "title": "Walking Meetings",
            "description": "Replace one daily screen session with a walk.",
            "difficulty": ChallengeDifficulty.MEDIUM,
            "duration_days": 7,
            "category": None,
            "rules": [
                "Identify your longest daily scrolling session",
                "Replace it with a walk of the same duration",
                "Leave your phone at home or on airplane mode",
            ],
            "tips": [
                "Walking boosts creativity and reduces anxiety",
                "Try different routes to keep it interesting",
            ],
        },
        # HARD challenges
        {
            "title": "Social Media Fast",
            "description": "Complete social media abstinence for 7 days.",
            "difficulty": ChallengeDifficulty.HARD,
            "duration_days": 7,
            "category": AppCategory.SOCIAL_MEDIA,
            "rules": [
                "Delete all social media apps from your phone",
                "Log out of social media on your computer",
                "No checking social media at all for 7 days",
                "Journal about your experience daily",
            ],
            "tips": [
                "Tell friends how to reach you directly",
                "Notice withdrawal symptoms - they peak around day 2-3",
                "Replace the habit with something meaningful",
            ],
        },
        {
            "title": "Dumb Phone Week",
            "description": "Use your phone only for calls and texts for one week.",
            "difficulty": ChallengeDifficulty.HARD,
            "duration_days": 7,
            "category": None,
            "rules": [
                "Disable all apps except phone, messages, maps, and camera",
                "No web browsing on your phone",
                "Limit computer use to work hours only",
            ],
            "tips": [
                "Print directions before going out",
                "Carry a book or notebook for downtime",
                "This is how phones worked before 2008!",
            ],
        },
        {
            "title": "Entertainment Cleanse",
            "description": "No streaming, gaming, or video content for 7 days.",
            "difficulty": ChallengeDifficulty.HARD,
            "duration_days": 7,
            "category": AppCategory.ENTERTAINMENT,
            "rules": [
                "No Netflix, YouTube, Twitch, or any streaming service",
                "No mobile or video games",
                "Replace with books, podcasts, music, or creative hobbies",
            ],
            "tips": [
                "Make a list of books or hobbies to try",
                "You'll rediscover how much free time you actually have",
            ],
        },
        {
            "title": "Two-Hour Total",
            "description": "Limit total screen time to 2 hours per day for 5 days.",
            "difficulty": ChallengeDifficulty.HARD,
            "duration_days": 5,
            "category": None,
            "rules": [
                "Maximum 120 minutes of recreational screen time per day",
                "Work/school screen time doesn't count",
                "Track your usage honestly",
                "Plan your 2 hours intentionally each morning",
            ],
            "tips": [
                "Prioritize which apps matter most to you",
                "Use screen time tracking features on your device",
            ],
        },
        {
            "title": "Bedroom Sanctuary",
            "description": "No screens in the bedroom for 10 days.",
            "difficulty": ChallengeDifficulty.HARD,
            "duration_days": 10,
            "category": None,
            "rules": [
                "No phones, tablets, or laptops in the bedroom",
                "Get a physical alarm clock",
                "Read a physical book before bed instead",
                "Charge all devices in another room",
            ],
            "tips": [
                "Your bedroom should be for sleep and relaxation only",
                "You'll likely notice improved sleep quality within days",
            ],
        },
        {
            "title": "Connection Challenge",
            "description": "Replace all digital social interactions with in-person or phone calls.",
            "difficulty": ChallengeDifficulty.HARD,
            "duration_days": 7,
            "category": AppCategory.SOCIAL_MEDIA,
            "rules": [
                "No texting for social conversations - call or meet instead",
                "Have at least one in-person social activity per day",
                "No commenting or reacting on social media",
            ],
            "tips": [
                "Schedule coffee dates, walks, or dinners with friends",
                "Voice calls create deeper connection than text",
            ],
        },
        # EXTREME challenges
        {
            "title": "Digital Minimalism Month",
            "description": "30-day complete digital reset following Cal Newport's protocol.",
            "difficulty": ChallengeDifficulty.EXTREME,
            "duration_days": 30,
            "category": None,
            "rules": [
                "Remove all optional technologies for 30 days",
                "Only keep technology essential for work and safety",
                "Rediscover offline activities and hobbies",
                "After 30 days, reintroduce only what adds real value",
                "For each reintroduced app, define specific rules of use",
            ],
            "tips": [
                "Read 'Digital Minimalism' by Cal Newport",
                "Keep a journal of observations and feelings",
                "This is transformative - most people don't go back to old habits",
            ],
        },
        {
            "title": "Analog Week",
            "description": "One full week with absolutely no recreational screen time.",
            "difficulty": ChallengeDifficulty.EXTREME,
            "duration_days": 7,
            "category": None,
            "rules": [
                "Screens only for essential work (limited hours)",
                "No social media, news, entertainment, or casual browsing",
                "Use paper calendar, physical books, analog tools",
                "Write letters instead of emails where possible",
            ],
            "tips": [
                "Prepare extensively before starting",
                "Print out anything you might need",
                "This will reveal how dependent you are on screens",
            ],
        },
        {
            "title": "Sunrise to Sunset",
            "description": "No screens between sunrise and sunset for 3 days.",
            "difficulty": ChallengeDifficulty.EXTREME,
            "duration_days": 3,
            "category": None,
            "rules": [
                "From sunrise to sunset, no screen usage at all",
                "Spend the entire daylight hours offline",
                "Engage in outdoor activities, exercise, socializing",
                "Evening screen use limited to 1 hour",
            ],
            "tips": [
                "Best done on a weekend or during time off",
                "Plan outdoor activities in advance",
                "Bring a journal to capture thoughts and ideas",
            ],
        },
        {
            "title": "App Elimination Tournament",
            "description": "Delete one app from your phone each day for 14 days.",
            "difficulty": ChallengeDifficulty.EXTREME,
            "duration_days": 14,
            "category": None,
            "rules": [
                "Each morning, choose and delete one non-essential app",
                "Start with the least important, save the hardest for last",
                "Do not reinstall any deleted app during the challenge",
                "After 14 days, only reinstall apps you truly missed",
            ],
            "tips": [
                "Most people find they don't miss 80% of their apps",
                "This is a powerful exercise in digital intentionality",
            ],
        },
        {
            "title": "The Deep Work Sprint",
            "description": "4 hours of uninterrupted focus daily for 5 days, no digital distractions.",
            "difficulty": ChallengeDifficulty.EXTREME,
            "duration_days": 5,
            "category": None,
            "rules": [
                "Block 4 consecutive hours each day for deep work",
                "Phone on airplane mode during this period",
                "Close all non-essential browser tabs and apps",
                "No checking email, messages, or social media",
                "Track what you accomplish in these focused sessions",
            ],
            "tips": [
                "Start with 2 hours if 4 feels impossible - that's telling",
                "The quality of work produced will surprise you",
            ],
        },
    ]

    def __init__(self) -> None:
        self._challenge_counter = 0

    def get_random_challenge(
        self,
        difficulty: ChallengeDifficulty | None = None,
        category: AppCategory | None = None,
    ) -> Challenge:
        """Get a random challenge, optionally filtered by difficulty or category."""
        candidates = self.CHALLENGES.copy()

        if difficulty:
            candidates = [c for c in candidates if c["difficulty"] == difficulty]
        if category:
            candidates = [
                c for c in candidates
                if c.get("category") is None or c["category"] == category
            ]

        if not candidates:
            candidates = self.CHALLENGES.copy()

        chosen = random.choice(candidates)
        return self._to_challenge(chosen)

    def get_all_challenges(self) -> list[Challenge]:
        """Get all available challenges."""
        return [self._to_challenge(c) for c in self.CHALLENGES]

    def get_challenges_by_difficulty(
        self, difficulty: ChallengeDifficulty
    ) -> list[Challenge]:
        """Get all challenges of a specific difficulty."""
        return [
            self._to_challenge(c)
            for c in self.CHALLENGES
            if c["difficulty"] == difficulty
        ]

    def get_progressive_plan(self, weeks: int = 4) -> list[Challenge]:
        """Generate a progressive challenge plan over several weeks."""
        plan: list[Challenge] = []

        difficulty_progression = {
            1: ChallengeDifficulty.EASY,
            2: ChallengeDifficulty.MEDIUM,
            3: ChallengeDifficulty.HARD,
            4: ChallengeDifficulty.EXTREME,
        }

        for week in range(1, weeks + 1):
            diff = difficulty_progression.get(
                min(week, 4), ChallengeDifficulty.MEDIUM
            )
            candidates = [c for c in self.CHALLENGES if c["difficulty"] == diff]
            if candidates:
                chosen = random.choice(candidates)
                challenge = self._to_challenge(chosen)
                plan.append(challenge)

        return plan

    def _to_challenge(self, data: dict) -> Challenge:
        """Convert a challenge dict to a Challenge model."""
        self._challenge_counter += 1
        return Challenge(
            challenge_id=f"CH{self._challenge_counter:03d}",
            title=data["title"],
            description=data["description"],
            difficulty=data["difficulty"],
            duration_days=data["duration_days"],
            category=data.get("category"),
            rules=data.get("rules", []),
            tips=data.get("tips", []),
        )
