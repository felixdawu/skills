#!/usr/bin/env python3
"""
Analyze git changes and generate a Conventional Commits-style commit message.

Usage:
    python generate_commit_message.py [--staged-only] [--scope SCOPE] [--language en|zh]

Options:
    --staged-only   Only analyze staged changes (default: all changes)
    --scope SCOPE   Manually specify the scope (overrides auto-detection)
    --language      Output language: 'en' (default) or 'zh'
"""

import subprocess
import sys
import os
from collections import defaultdict


def run_git(args):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"git error: {e.stderr}", file=sys.stderr)
        return ""


def get_status():
    """Get git status output."""
    return run_git(["status", "--short"])


def get_diff(staged=False):
    """Get git diff output."""
    args = ["diff", "--stat"]
    if staged:
        args.insert(1, "--cached")
    return run_git(args)


def get_full_diff(staged=False):
    """Get full diff for analysis."""
    args = ["diff"]
    if staged:
        args.insert(1, "--cached")
    return run_git(args)


# File extension/type to Conventional Commit type mapping
FILE_TYPE_MAP = {
    # Test files
    ".test.": "test",
    "_test.": "test",
    ".spec.": "test",
    "/test/": "test",
    "/tests/": "test",
    "/__tests__/": "test",
    # Documentation
    ".md": "docs",
    ".rst": "docs",
    ".txt": "docs",
    # CI/CD
    ".github/": "ci",
    ".gitlab-ci.yml": "ci",
    ".circleci/": "ci",
    "Jenkinsfile": "ci",
    # Config/build
    "package.json": "build",
    "requirements.txt": "build",
    "Cargo.toml": "build",
    "go.mod": "build",
    "pyproject.toml": "build",
    ".eslintrc": "style",
    ".prettierrc": "style",
    ".editorconfig": "style",
}


def guess_type_from_files(files):
    """Guess commit type based on changed file patterns."""
    changes = defaultdict(list)

    for f in files:
        # Check test patterns first (higher priority)
        if any(p in f for p in [".test.", "_test.", ".spec.", "/test/", "/tests/", "/__tests__/"]):
            changes["test"].append(f)
        # Check CI patterns
        elif any(p in f for p in [".github/", ".gitlab-ci.yml", ".circleci/", "Jenkinsfile"]):
            changes["ci"].append(f)
        # Check docs patterns
        elif f.endswith((".md", ".rst", ".txt")):
            changes["docs"].append(f)
        # Check build/config patterns
        elif os.path.basename(f) in ["package.json", "requirements.txt", "Cargo.toml", "go.mod", "pyproject.toml"]:
            changes["build"].append(f)
        # Check style/lint config
        elif os.path.basename(f) in [".eslintrc", ".prettierrc", ".editorconfig", ".eslintrc.js", ".prettierrc.json"]:
            changes["style"].append(f)
        else:
            changes["unknown"].append(f)

    return changes


def guess_scope(files):
    """Guess scope from changed files."""
    if not files:
        return ""

    # If all files share a common directory, use that as scope
    dirs = set()
    for f in files:
        parts = f.split("/")
        if len(parts) > 1:
            dirs.add(parts[0])

    if len(dirs) == 1:
        return dirs.pop()

    # If files share a common prefix or are related to a known module
    known_modules = {"auth", "api", "ui", "db", "cache", "queue", "admin", "user", "payment", "search", "email", "config"}
    for f in files:
        basename = os.path.basename(f).split(".")[0]
        if basename in known_modules:
            return basename
        # Check directory name
        parts = f.split("/")
        if parts[0] in known_modules:
            return parts[0]

    return ""


def analyze_diff_for_description(diff_text):
    """Extract key changes from diff for commit body."""
    lines = []
    for line in diff_text.split("\n"):
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@") or line.startswith("diff "):
            continue
        if line.startswith("+") and not line.startswith("+++"):
            # Look for function/class definitions, imports, etc.
            stripped = line[1:].strip()
            if any(keyword in stripped for keyword in ["def ", "class ", "fn ", "func ", "const ", "let ", "import ", "export ", "type ", "interface "]):
                lines.append(stripped)
    return lines[:5]  # Limit to 5 key changes


def generate_message(files, diff_text="", is_new_feature=True, is_fix=False, manual_scope=None, language="en"):
    """Generate a commit message from changed files."""
    if not files:
        return {"error": "no changes detected"}

    file_type_changes = guess_type_from_files(files)

    # Determine primary type
    if is_fix:
        primary_type = "fix"
    elif len(file_type_changes.get("test", [])) == len(files):
        primary_type = "test"
    elif len(file_type_changes.get("docs", [])) == len(files):
        primary_type = "docs"
    elif len(file_type_changes.get("ci", [])) == len(files):
        primary_type = "ci"
    elif len(file_type_changes.get("build", [])) == len(files):
        primary_type = "build"
    elif len(file_type_changes.get("style", [])) == len(files):
        primary_type = "style"
    elif is_new_feature:
        primary_type = "feat"
    else:
        primary_type = "chore"

    # Determine scope
    scope = manual_scope if manual_scope else guess_scope(files)

    # Generate subject line
    if primary_type == "fix":
        subject = "fix known issue" if language == "en" else "修复已知问题"
    elif primary_type == "feat":
        subject = "add new functionality" if language == "en" else "添加新功能"
    elif primary_type == "docs":
        subject = "update documentation" if language == "en" else "更新文档"
    elif primary_type == "test":
        subject = "add tests" if language == "en" else "添加测试"
    elif primary_type == "ci":
        subject = "update CI configuration" if language == "en" else "更新 CI 配置"
    elif primary_type == "build":
        subject = "update dependencies" if language == "en" else "更新依赖"
    elif primary_type == "style":
        subject = "fix code style" if language == "en" else "修复代码格式"
    else:
        subject = "miscellaneous changes" if language == "en" else "杂项变更"

    # Build subject line
    if scope:
        subject_line = f"{primary_type}({scope}): {subject}"
    else:
        subject_line = f"{primary_type}: {subject}"

    # Truncate to 72 chars if needed
    if len(subject_line) > 72:
        subject_line = subject_line[:69] + "..."

    # Build message
    message_lines = [subject_line]

    # Add body if we have meaningful diff info
    if diff_text:
        key_changes = analyze_diff_for_description(diff_text)
        if key_changes:
            message_lines.append("")
            for change in key_changes:
                if language == "zh":
                    message_lines.append(f"- {change}")
                else:
                    message_lines.append(f"- {change}")

    return {
        "type": primary_type,
        "scope": scope,
        "subject": subject,
        "full_message": "\n".join(message_lines),
    }


def main():
    staged_only = "--staged-only" in sys.argv
    language = "en"
    manual_scope = None

    for i, arg in enumerate(sys.argv):
        if arg == "--scope" and i + 1 < len(sys.argv):
            manual_scope = sys.argv[i + 1]
        elif arg == "--language" and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]

    # Get status
    status = get_status()
    if not status:
        print("No changes to commit.", file=sys.stderr)
        sys.exit(1)

    # Parse changed files
    files = []
    for line in status.strip().split("\n"):
        if line:
            # Status format: XY filename
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                files.append(parts[1])
            else:
                files.append(parts[0])

    # Get diff for analysis
    diff = get_full_diff()

    result = generate_message(files, diff, language=language, manual_scope=manual_scope)

    if "error" in result:
        print(result["error"], file=sys.stderr)
        sys.exit(1)

    print(result["full_message"])


if __name__ == "__main__":
    main()
