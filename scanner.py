#!/usr/bin/env python3
"""
LLM Security Scanner — CLI version
Analyzes Python files for security vulnerabilities using Claude.

Usage:
    python scanner.py <path_to_file>

Requirements:
    pip install anthropic
    export ANTHROPIC_API_KEY=your_key_here
"""

import sys
import json
import os
import anthropic

# ANSI color codes
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SEV_COLORS = {
    "HIGH":   RED,
    "MEDIUM": YELLOW,
    "LOW":    GREEN,
}

PROMPT_TEMPLATE = """You are a security analyst. Analyze this Python code for security vulnerabilities.

Return ONLY a raw JSON array. No markdown, no explanation, no backticks. Just the JSON array.

Each object must have exactly these fields:
- "type": short name (e.g. "Command Injection")
- "severity": one of "HIGH", "MEDIUM", "LOW"
- "line": line number as integer (best estimate)
- "problem": one sentence describing the specific risk
- "fix": one sentence describing the recommended fix

Code:
{code}"""


def print_banner():
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}  LLM Security Scanner — powered by Claude{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


def print_summary(issues):
    high   = sum(1 for i in issues if i["severity"] == "HIGH")
    medium = sum(1 for i in issues if i["severity"] == "MEDIUM")
    low    = sum(1 for i in issues if i["severity"] == "LOW")

    print(f"{BOLD}Summary:{RESET}  "
          f"{RED}{high} HIGH{RESET}  "
          f"{YELLOW}{medium} MEDIUM{RESET}  "
          f"{GREEN}{low} LOW{RESET}\n")


def print_issue(issue, index):
    sev   = issue.get("severity", "LOW")
    color = SEV_COLORS.get(sev, GRAY)

    print(f"{BOLD}Issue {index}{RESET}")
    print(f"  {BOLD}Type    {RESET} {issue.get('type', 'Unknown')}")
    print(f"  {BOLD}Severity{RESET} {color}{sev}{RESET}")
    print(f"  {BOLD}Line    {RESET} {GRAY}line {issue.get('line', '?')}{RESET}")
    print(f"  {BOLD}Problem {RESET} {issue.get('problem', '')}")
    print(f"  {BOLD}Fix     {RESET} {GREEN}{issue.get('fix', '')}{RESET}")
    print()


def analyze_file(filepath: str):
    if not os.path.exists(filepath):
        print(f"{RED}Error: File not found: {filepath}{RESET}")
        sys.exit(1)

    with open(filepath, "r") as f:
        code = f.read()

    print(f"{GRAY}Scanning: {filepath}{RESET}")
    print(f"{GRAY}Sending to Claude for analysis...{RESET}\n")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(f"{RED}Error: ANTHROPIC_API_KEY environment variable not set.{RESET}")
        print(f"Run: export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(code=code)
            }
        ]
    )

    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    issues = json.loads(raw)
    return issues


def main():
    print_banner()

    if len(sys.argv) < 2:
        print(f"Usage: python scanner.py <path_to_python_file>")
        print(f"Example: python scanner.py examples/command_injection.py")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        issues = analyze_file(filepath)
    except json.JSONDecodeError:
        print(f"{RED}Error: Could not parse Claude's response as JSON.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    if not issues:
        print(f"{GREEN}✓ No security issues detected.{RESET}\n")
        return

    print_summary(issues)

    # Sort by severity
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    issues.sort(key=lambda x: order.get(x.get("severity", "LOW"), 3))

    print(f"{BOLD}Issues found:{RESET}\n")
    for i, issue in enumerate(issues, 1):
        print_issue(issue, i)

    print(f"{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}Scan complete. {len(issues)} issue(s) found.{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


if __name__ == "__main__":
    main()
