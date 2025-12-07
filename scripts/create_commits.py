#!/usr/bin/env python3
"""
Create git commits from commits.json file.
Sets custom timestamps and appends to data.csv.
"""

import json
import os
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git_command(cmd, check=True):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {cmd}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        if check:
            sys.exit(1)
        return None


def ensure_data_file():
    """Ensure data.csv exists with header."""
    data_file = Path("data.csv")
    if not data_file.exists():
        with open(data_file, "w") as f:
            f.write("value1,value2,value3,value4,value5\n")
        run_git_command("git add data.csv", check=False)


def append_to_data_file():
    """Append a random line to data.csv."""
    values = [str(random.randint(1, 1000)) for _ in range(5)]
    with open("data.csv", "a") as f:
        f.write(",".join(values) + "\n")


def create_commits(commits_file="commits.json", branch="generated-commits"):
    """Create git commits from commits.json."""
    # Read commits.json
    if not Path(commits_file).exists():
        print(f"Error: {commits_file} not found. Run 'make generate-commits' first.", file=sys.stderr)
        sys.exit(1)
    
    with open(commits_file, "r") as f:
        commits = json.load(f)
    
    # Ensure data.csv exists
    ensure_data_file()
    
    # Check if branch exists, create if not
    branch_exists = run_git_command(f"git rev-parse --verify {branch}", check=False) is not None
    
    if not branch_exists:
        # Create branch from current branch or HEAD
        current_branch = run_git_command("git branch --show-current", check=False)
        if not current_branch:
            # No branch exists, create initial commit if needed
            if run_git_command("git rev-parse --verify HEAD", check=False) is None:
                run_git_command("git add .", check=False)
                run_git_command('git commit -m "Initial commit"', check=False)
        run_git_command(f"git checkout -b {branch}", check=False)
    else:
        run_git_command(f"git checkout {branch}", check=False)
    
    # Create each commit
    for i, commit_data in enumerate(commits, 1):
        # Append to data.csv
        append_to_data_file()
        
        # Stage the file
        run_git_command("git add data.csv")
        
        # Create commit with custom date
        timestamp = commit_data["timestamp"]
        message = commit_data["message"]
        
        # Format timestamp for git (ISO 8601 format)
        # Git accepts: YYYY-MM-DD HH:MM:SS or ISO format
        dt = datetime.fromisoformat(timestamp)
        git_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Set both author and committer date
        env = {
            **os.environ,
            "GIT_AUTHOR_DATE": git_date,
            "GIT_COMMITTER_DATE": git_date,
        }
        
        subprocess.run(
            ["git", "commit", "-m", message],
            env=env,
            check=True
        )
        
        print(f"Created commit {i}/{len(commits)}: {commit_data['date']} - {message}")
    
    print(f"\nSuccessfully created {len(commits)} commits on branch '{branch}'")
    print(f"To view: git log --oneline --graph {branch}")


if __name__ == "__main__":
    create_commits()

