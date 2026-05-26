#!/usr/bin/env python3
"""
Story of Pi Automation Scheduler
Master Codex Enterprise — Story + Code + Trends Agent

Operator: Cpl Tremain A. Wade Jr., USMC (Ret.)
Purpose: Every 8 hours produce a new Story of Pi chapter, attach visual code, gather fun information, monitor trends, and notify when alerts appear.
"""

import argparse
import json
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
HISTORY_PATH = ROOT / "story_of_pi_history.json"
TRENDS_PATH = ROOT / "story_of_pi_trends.json"
OUTPUT_PATH = ROOT / "story_of_pi_last_output.md"
LOG_PATH = ROOT / "story_of_pi_agent.log"
SCHEDULE_SECONDS = 8 * 60 * 60

CHAPTERS = [
    {
        "chapter": "Chapter I: The Pi Origin Code",
        "theme": "Origin, curiosity, math as myth.",
        "code_label": "Python Story Loop",
        "code_snippet": "def next_beat(beat):\n    return f'Pi reads the code, and the code reads back.'\n\nfor beat in ['origin', 'mirror', 'call']:\n    print(next_beat(beat))",
        "fun_fact": "Pi is not just a number here — it is a character who learns by writing code.",
        "practical_project": "Build a story card screen that reveals the next narrative beat when the player solves a simple Python puzzle.",
        "fun_score": 9,
        "practical_score": 8,
        "risk_score": 3,
        "mood_score": 8,
    },
    {
        "chapter": "Chapter II: The Echo Interface",
        "theme": "Dialogue, mentorship, accessible UI.",
        "code_label": "HTML/CSS Story Panel",
        "code_snippet": "<section class=\"story-card\">\n  <h2>Pi meets Echo</h2>\n  <p>Every answer becomes a new clue.</p>\n</section>\n<style>\n.story-card { padding: 18px; border: 2px solid #c92a2a; background: #fff4e6; }\n</style>",
        "fun_fact": "This chapter turns dialogue into a playful app onboarding experience.",
        "practical_project": "Prototype a responsive story card that changes color and text as the user picks choices.",
        "fun_score": 8,
        "practical_score": 9,
        "risk_score": 4,
        "mood_score": 7,
    },
    {
        "chapter": "Chapter III: The Bridge of Patterns",
        "theme": "Algorithms as bridges, patterns as portals.",
        "code_label": "Pseudo-code Pattern Map",
        "code_snippet": "patterns = ['loop', 'condition', 'recursion']\nfor pattern in patterns:\n    print(f'Pi crosses the bridge of {pattern}')",
        "fun_fact": "This chapter is designed to teach logic visually by mapping story scenes to code patterns.",
        "practical_project": "Create a pattern map page where each pattern unlocks a narrative clue and a practical coding exercise.",
        "fun_score": 8,
        "practical_score": 8,
        "risk_score": 5,
        "mood_score": 7,
    },
    {
        "chapter": "Chapter IV: The Gate of Ethics",
        "theme": "AI decisions, guardrails, moral code.",
        "code_label": "Decision Tree Example",
        "code_snippet": "def choose_path(trust):\n    if trust > 7:\n        return 'bridge'\n    return 'checkpoint'\n\nprint(choose_path(9))",
        "fun_fact": "This chapter makes AI ethics feel like a game checkpoint rather than a lecture.",
        "practical_project": "Build an interactive checkpoint screen that self-evaluates user decisions and shows consequences.",
        "fun_score": 7,
        "practical_score": 9,
        "risk_score": 6,
        "mood_score": 6,
    },
    {
        "chapter": "Chapter V: The Scarlet Gold Run",
        "theme": "Build sprint, design discipline, momentum.",
        "code_label": "Sprint Tracker Card",
        "code_snippet": "tasks = ['wireframe', 'prototype', 'user test']\ncompleted = tasks[:2]\nprint(f'Sprint progress: {len(completed)}/{len(tasks)}')",
        "fun_fact": "This chapter turns app building into a race story with real milestones.",
        "practical_project": "Design a visual sprint tracker that shows story progress as a running character.",
        "fun_score": 8,
        "practical_score": 10,
        "risk_score": 4,
        "mood_score": 8,
    },
    {
        "chapter": "Chapter VI: The Dreams Board Signal",
        "theme": "Goal-setting, trend sensing, future vision.",
        "code_label": "Trend Analyzer Snippet",
        "code_snippet": "signals = [7, 8, 6, 9]\naverage = sum(signals) / len(signals)\nprint(f'Fun signal average: {average}')",
        "fun_fact": "This chapter is the first to explicitly gather fun information and spot trends.",
        "practical_project": "Add a dashboard widget that flags high-risk or low-fun story sections automatically.",
        "fun_score": 9,
        "practical_score": 8,
        "risk_score": 5,
        "mood_score": 9,
    },
    {
        "chapter": "Chapter VII: The Bad-Weather Beacon",
        "theme": "Alert systems, resilience, emergency signal.",
        "code_label": "Watchdog Notification",
        "code_snippet": "if mood_score < 6 or risk_score > 7:\n    send_alert('Story health is weak')",
        "fun_fact": "This chapter makes the agent itself part of the story by learning when things are bad.",
        "practical_project": "Create a visual bad-weather beacon on the dashboard that turns red when the system needs attention.",
        "fun_score": 7,
        "practical_score": 7,
        "risk_score": 8,
        "mood_score": 5,
    },
    {
        "chapter": "Chapter VIII: The Council of 20",
        "theme": "Synthesis, review, next-phase strategy.",
        "code_label": "Review Engine",
        "code_snippet": "review = {'story': 8, 'trends': 7, 'alert': False}\nprint(review)",
        "fun_fact": "This chapter is the moment the system pauses and asks what to build next.",
        "practical_project": "Prototype a review screen that summarizes story progress, trending health, and next actions.",
        "fun_score": 8,
        "practical_score": 9,
        "risk_score": 4,
        "mood_score": 8,
    },
]


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def get_next_chapter_index(history):
    if not history:
        return 0
    return len(history) % len(CHAPTERS)


def format_code_block(code, label):
    return f"```python\n# {label}\n{code}\n````"


def send_macos_notification(title, body):
    try:
        subprocess.run([
            "osascript",
            "-e",
            f'display notification "{body}" with title "{title}"'
        ], check=True)
    except Exception:
        pass


def compute_trend_summary(history):
    if not history:
        return {
            "runs": 0,
            "fun_average": 0,
            "practical_average": 0,
            "mood_average": 0,
            "risk_average": 0,
            "alert_count": 0,
        }

    fun_values = [item['fun_score'] for item in history]
    practical_values = [item['practical_score'] for item in history]
    mood_values = [item['mood_score'] for item in history]
    risk_values = [item['risk_score'] for item in history]
    alert_count = sum(1 for item in history if item.get('alert'))

    return {
        "runs": len(history),
        "fun_average": round(sum(fun_values) / len(fun_values), 2),
        "practical_average": round(sum(practical_values) / len(practical_values), 2),
        "mood_average": round(sum(mood_values) / len(mood_values), 2),
        "risk_average": round(sum(risk_values) / len(risk_values), 2),
        "alert_count": alert_count,
    }


def evaluate_alert(chapter):
    alert = False
    reasons = []

    if chapter['mood_score'] < 6:
        alert = True
        reasons.append('low mood score')
    if chapter['risk_score'] > 7:
        alert = True
        reasons.append('high risk score')

    return alert, reasons


def build_output(chapter, history):
    timestamp = datetime.now().isoformat()
    alert, reasons = evaluate_alert(chapter)
    trend_summary = compute_trend_summary(history + [
        {
            'fun_score': chapter['fun_score'],
            'practical_score': chapter['practical_score'],
            'mood_score': chapter['mood_score'],
            'risk_score': chapter['risk_score'],
            'alert': alert,
        }
    ])

    text = [
        f"# Story of Pi Automation — {chapter['chapter']}",
        f"**Generated at:** {timestamp}",
        "",
        f"**Theme:** {chapter['theme']}",
        "",
        "## Narrative",
        f"{chapter['fun_fact']}",
        "",
        "## Visual Code Card",
        format_code_block(chapter['code_snippet'], chapter['code_label']),
        "",
        "## Practical Project",
        f"{chapter['practical_project']}",
        "",
        "## Trend Snapshot",
        f"- Fun score: {chapter['fun_score']}/10",
        f"- Practical score: {chapter['practical_score']}/10",
        f"- Mood score: {chapter['mood_score']}/10",
        f"- Risk score: {chapter['risk_score']}/10",
        "",
        "## Trend Averages (all runs)",
        f"- Fun average: {trend_summary['fun_average']}/10",
        f"- Practical average: {trend_summary['practical_average']}/10",
        f"- Mood average: {trend_summary['mood_average']}/10",
        f"- Risk average: {trend_summary['risk_average']}/10",
        f"- Alert count: {trend_summary['alert_count']}",
        "",
    ]

    if alert:
        text.append("## ALERT — HEALTH WARNING")
        text.append(f"- Reason: {', '.join(reasons)}")
        text.append("- Action: Review the dashboard, pause new story beats, and adjust the next project beat for higher fun and lower risk.")
        text.append("")

    text.append("## Operational Note")
    text.append("This agent cycles through Story of Pi beats every eight hours and writes the next chapter to `update/story_of_pi_last_output.md`.")
    text.append("It also updates trend data in `update/story_of_pi_trends.json` and keeps history in `update/story_of_pi_history.json`.")

    return "\n".join(text), alert


def log(message):
    entry = f"[{datetime.now().isoformat()}] {message}\n"
    ROOT.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, 'a') as handle:
        handle.write(entry)


def run_once():
    history = load_json(HISTORY_PATH, [])
    index = get_next_chapter_index(history)
    chapter = CHAPTERS[index]

    output_text, alert = build_output(chapter, history)
    OUTPUT_PATH.write_text(output_text)

    run_entry = {
        'timestamp': datetime.now().isoformat(),
        'chapter': chapter['chapter'],
        'theme': chapter['theme'],
        'fun_score': chapter['fun_score'],
        'practical_score': chapter['practical_score'],
        'mood_score': chapter['mood_score'],
        'risk_score': chapter['risk_score'],
        'alert': alert,
    }
    history.append(run_entry)
    save_json(HISTORY_PATH, history)
    save_json(TRENDS_PATH, compute_trend_summary(history))

    log(f"Generated {chapter['chapter']} (alert={alert})")

    if alert:
        send_macos_notification(
            "Story of Pi Alert",
            f"{chapter['chapter']} triggered an alert: {'; '.join([str(x) for x in [chapter['theme']]])}"
        )
    return chapter['chapter'], alert


def run_daemon():
    log('Starting Story of Pi scheduler daemon')
    while True:
        story, alert = run_once()
        if alert:
            log(f'Alert generated for {story}')
        else:
            log(f'Story generated: {story}')
        time.sleep(SCHEDULE_SECONDS)


def parse_args():
    parser = argparse.ArgumentParser(description='Story of Pi Automation Scheduler')
    parser.add_argument('--once', action='store_true', help='Generate one Story of Pi beat and exit')
    parser.add_argument('--daemon', action='store_true', help='Run the 8-hour scheduler loop continuously')
    parser.add_argument('--status', action='store_true', help='Show current schedule status and trend data')
    return parser.parse_args()


def show_status():
    history = load_json(HISTORY_PATH, [])
    trends = load_json(TRENDS_PATH, {})
    next_index = get_next_chapter_index(history)
    print('\nSTORY OF PI AUTOMATION STATUS')
    print('----------------------------------')
    print(f'Next chapter index: {next_index} ({CHAPTERS[next_index]['chapter']})')
    print(f'Run count: {len(history)}')
    print('Trend summary:')
    for key, value in trends.items():
        print(f'  - {key}: {value}')
    print('\nLast output file: update/story_of_pi_last_output.md')


def main():
    args = parse_args()
    if args.status:
        show_status()
        return
    if args.once:
        chapter, alert = run_once()
        print(f'Generated: {chapter} (alert={alert})')
        return
    if args.daemon:
        run_daemon()
        return
    print('No action selected. Use --once, --daemon, or --status.')


if __name__ == '__main__':
    main()
