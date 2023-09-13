import os
import json

def parse_config():
    config_path = os.path.expanduser("~/.config/goc/config.json")
    if os.path.exists(config_path):
        config = json.loads(open(config_path).read())
    else:
        config = {
            "commit_template": "default",
            "diff_template": "default",
        }
    return config

def get_default_commit_template():
    return "<Fix|Add|Update|Refactor|Docs>: <commit message>"

def get_default_diff_template():
    return """# Git Commit Diff

## Description
- Briefly describe the changes made in this commit.

## Files Modified
- List the files that were modified in this commit:

  - `file1.ext`: Describe changes made in this file.
  - `file2.ext`: Explain modifications in this file.
  - ...

## Changes Made
- Specify the changes made to each file, including additions, deletions, and modifications.
    """

def get_commit_config():
    config = parse_config()
    if config.get("commit_template") == 'default':
        return get_default_commit_template()
    else:
        template = open(
            os.path.expanduser("~/.config/goc/") + config.get("commit_template")
        ).read()
        return template

def get_diff_config():
    config = parse_config()
    if config.get("diff_template") == 'default':
        return get_default_diff_template()
    else:
        template = open(
            os.path.expanduser("~/.config/goc/") + config.get("diff_template")
        ).read()
        return template

