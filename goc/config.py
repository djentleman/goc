import os
import yaml

from typing import Dict
from enum import Enum


class TemplateType(Enum):
    Diff = "diff_template"
    Commit = "commit_template"


class MultilineLiteralDumper(yaml.Dumper):
    """
    use '|' for dumping multiline string to yaml file
    """
    def represent_scalar(self, tag, value, style=None):
        if '\n' in value:
            style = '|'
        return super().represent_scalar(tag, value, style)


CONFIG_PATH = os.path.expanduser("~/.config/goc/config.yaml")
DEFAULT_GPT_VER = "3.5-turbo"
DEFAULT_DIFF_TEMPLATE = """# Git Commit Diff

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

DEFAULT_COMMIT_TEMPLATE = "<Fix|Add|Update|Refactor|Docs>: <commit message>"

def get_default_template_dict():
    return  {
        "diff_template": DEFAULT_DIFF_TEMPLATE,
        "commit_template": DEFAULT_COMMIT_TEMPLATE,
        "gpt_ver": DEFAULT_GPT_VER
    }

def write_config(config_dict):
    with open(CONFIG_PATH, "w") as file:
        yaml.dump(config_dict, file, Dumper=MultilineLiteralDumper, default_flow_style=False)
    print("goc generated a config file with default diff and commit templates under ~/.config/goc")


def generate_default_template() -> None:
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    default_template_dict = get_default_template_dict()
    write_config(default_template_dict)


def read_config() -> Dict[str,str]:
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)
    return config


def parse_config() -> Dict[str,str]:
    default_config = get_default_template_dict
    if os.path.exists(CONFIG_PATH):
        config = read_config()
        # check if any fields are missing
        if config.keys() != default_config.keys():
            upd_config = default_config | config
            write_config(upd_config)
            config = upd_config
    else:
        try:
            generate_default_template()
            config = read_config()
        except PermissionError:
            print("Failed to generate the default config file due to permission issues.")
            print("Please ensure you have write permissions to ~/.config directory.")
            raise
    return config


def get_template(template_type: TemplateType) -> str:
    config = parse_config()
    return config[template_type.value]

def get_gpt_ver():
    config = parse_config()
    return config['gpt_ver']
