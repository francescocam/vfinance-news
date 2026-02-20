#!/usr/bin/env python3
"""
Briefing Generator - Main entry point for market briefings.
Generates market briefings for terminal/JSON output.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime

from vfinance_news.utils import ensure_venv

ensure_venv()


def generate_and_send(args):
    """Generate briefing output."""

    # Hard cutoff: morning before 12:00 local time, evening from 12:00 onward.
    hour = datetime.now().hour
    briefing_time = 'morning' if hour < 12 else 'evening'
    
    # Generate the briefing
    cmd = [
        sys.executable, '-m', 'vfinance_news.summarize',
        '--style', args.style,
    ]

    if args.deadline is not None:
        cmd.extend(['--deadline', str(args.deadline)])

    if args.fast:
        cmd.append('--fast')

    if args.llm:
        cmd.append('--llm')

    if args.debug:
        cmd.append('--debug')
    
    # Always use JSON for internal processing to handle splits
    cmd.append('--json')
    
    print(f"📊 Generating {briefing_time} briefing...", file=sys.stderr)
    
    timeout = args.deadline if args.deadline is not None else 300
    timeout = max(1, int(timeout))
    if args.deadline is not None:
        timeout = timeout + 5
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        timeout=timeout
    )
    
    if result.returncode != 0:
        print(f"❌ Briefing generation failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    try:
        data = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        # Fallback if not JSON (shouldn't happen with --json)
        print(f"⚠️ Failed to parse briefing JSON", file=sys.stderr)
        print(result.stdout)
        return result.stdout

    # Output handling
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        # Print for humans
        if data.get('macro_message'):
             print(data['macro_message'])
        if data.get('portfolio_message'):
             print("\n" + "="*20 + "\n")
             print(data['portfolio_message'])
    
    return data.get('macro_message', '')


def main():
    parser = argparse.ArgumentParser(description='Briefing Generator')
    parser.add_argument('--style', choices=['briefing', 'analysis', 'headlines'],
                        default='briefing', help='Summary style')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--deadline', type=int, default=None,
                        help='Overall deadline in seconds')
    parser.add_argument('--llm', action='store_true', help='Use LLM summary')
    parser.add_argument('--fast', action='store_true',
                        help='Use fast mode (shorter timeouts, fewer items)')
    parser.add_argument('--debug', action='store_true',
                        help='Write debug log with sources')
    
    args = parser.parse_args()
    generate_and_send(args)


if __name__ == '__main__':
    main()
