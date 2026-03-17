# Vairagya

Digital Detox Coach - monitor screen time, detect addictive usage patterns, and receive personalized digital wellness guidance.

*Vairagya (Sanskrit: dispassion/detachment) - the practice of cultivating non-attachment.*

## Features

- **Screen Time Tracking** - Log and categorize app usage by category
- **Notification Analysis** - Count and categorize notification interruptions
- **Pattern Detection** - Identify addictive patterns: doom scrolling, compulsive checking, late night use
- **Detox Goals** - Set and track screen time limits per category
- **Wellness Challenges** - 20+ digital wellness challenges for gradual improvement
- **Personalized Advice** - AI-generated reduction strategies based on your patterns
- **Usage Simulation** - Generate realistic usage data for testing
- **Rich Reports** - Beautiful terminal output with Rich

## Installation

```bash
pip install -e .
```

## Usage

### Track Screen Time

```bash
vairagya track --app Instagram --category social_media --duration 45
```

### Analyze Notifications

```bash
vairagya notifications --simulate
```

### Detect Usage Patterns

```bash
vairagya patterns --simulate
```

### Set a Detox Goal

```bash
vairagya goals set --category social_media --daily-limit 60
```

### Get a Challenge

```bash
vairagya challenge
```

### Get Wellness Advice

```bash
vairagya advise --simulate
```

### Generate Report

```bash
vairagya report --simulate
```

## Categories

- Social Media (Instagram, TikTok, Twitter/X, Facebook, Reddit)
- Entertainment (YouTube, Netflix, Twitch, Spotify)
- Communication (WhatsApp, Slack, Discord, Email)
- Productivity (VSCode, Notion, Google Docs)
- News (News apps, RSS readers)
- Gaming (Mobile games, Steam)
- Shopping (Amazon, eBay)
- Browsing (Chrome, Safari, Firefox)

## License

MIT
