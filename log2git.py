#!/usr/bin/env python3

import git
import os
import argparse
from datetime import datetime

def touch_target(repo_name, logs):
  target_name = os.path.join(repo_name, logs + ".txt")
  with open(target_name, 'w') as file:
    pass

  return target_name

def make_commits(repo, logs, target):
  target_inrepo = os.path.abspath(target)

  for f in os.listdir(logs):
    fpath = os.path.join(logs, f)
    if os.path.isfile(fpath):
      event_isotime = os.path.splitext(f)[0]
      event_time = datetime.fromisoformat(event_isotime)
      print(f"ready to write {fpath} to {target} with time {event_time}")

      with open(fpath, 'r') as file:
        event = file.readline().rstrip()
        file.seek(0)
        content = file.read()
      with open(target, 'w') as file:
        file.write(content)

      repo.index.add(target_inrepo)
      # repo.index.commit(message=event, author_date=event_time)
      repo.index.commit(message=event, commit_date=event_time)

def main(repo_name, branch_name, logs):
  print(f"Working on branch {branch_name} of repo {repo_name}")

  repo = git.Repo(repo_name)
  branch = repo.create_head(branch_name)
  branch.checkout()

  # touch target file
  target = touch_target(repo_name, logs)

  #make commits
  make_commits(repo, logs, target)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="log2git")
  # Add the repo and branch arguments
  parser.add_argument("repo", type=str, help="The repository name")
  parser.add_argument("branch", type=str, help="The branch name")
  parser.add_argument("logs", type=str, help="The logs directory")

  # Parse the command-line arguments
  args = parser.parse_args()

  # Call the main function with the provided arguments
  main(args.repo, args.branch, args.logs)
