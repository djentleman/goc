import os
from typing import List

import click
import openai

from goc.config_reader import get_diff_config, get_commit_config


def exec_bash_cmd(cmd):
    return os.popen(cmd).read()[:-1]


def document_git_diff_wrap(args):
    diff_config = get_diff_config()
    fmt_args = " ".join(args)
    cmd = f"git diff {fmt_args}"
    git_diff = exec_bash_cmd(cmd)
    if len(git_diff) == 0:
        print('No Git Diff Found')
        return []
    prompt_chain = [
        'When I send you a git diff, write documentation of the diff in markdown for a pull request',
        f'Please use this format for the git diff\n\n{diff_config}',
        git_diff
    ]
    return prompt_chain


def git_commit_wrap(m: str = None):
    commit_config = get_commit_config()
    cmd = f"git diff --staged"
    git_diff = exec_bash_cmd(cmd)
    if len(git_diff) == 0:
        print('No Staged Git Diff Found')
        return []

    prompt_chain = [
        'When I send you a git diff, write a commit message in 50 characters or less, do not include "git commit" or the character count',
        f'Please use this format for the git diff\n\n{commit_config}',
    ]
    if m is not None:
        prompt_chain.append(
            f'Here is a hint from the user about the commit message: "{m}" - the following prompt will be a git diff'
        )
    prompt_chain.append(git_diff)
    return prompt_chain


def execute_prompt_chain(prompt_chain, gpt_ver='3.5-turbo'):
    resp = openai.ChatCompletion.create(
        model=f"gpt-{gpt_ver}",
        messages=[
            {"role": "assistant", "content": cmd}
            for cmd in prompt_chain
        ]
    )    
    return resp


def parse_gpt_resp(resp):
    gpt_output = resp['choices'][-1]['message']['content']
    return gpt_output


def do_git_commit(gpt_output):
    gpt_output = gpt_output.split('\n')[0]
    if gpt_output[0] != '"':
        gpt_output = f'"{gpt_output}"'
    cmd = f'git commit -m {gpt_output}'
    exec_bash_cmd(cmd)


@click.group()
def diff_cmd():
    pass


@click.group()
def commit_cmd():
    pass


@diff_cmd.command(help="Generate documentation for the git diff between commits or files")
@click.option("--gpt_ver", help="GPT model version to use", default="3.5-turbo")
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def diff(gpt_ver: str, args: List[str]):
    prompt_chain = []
    prompt_chain = document_git_diff_wrap(args)
    if len(prompt_chain) > 0:
        resp = execute_prompt_chain(prompt_chain, gpt_ver=gpt_ver)
        gpt_output = parse_gpt_resp(resp)
        print(gpt_output)


@commit_cmd.command(help="Generate a commit message for the current git diff")
@click.option("--gpt_ver", help="GPT model version to use", default="3.5-turbo")
@click.option("-m", help="Hint Message to send to chat GPT", default=None)
def commit(gpt_ver: str, m: str):
    prompt_chain = []
    prompt_chain = git_commit_wrap(m=m)
    if len(prompt_chain) > 0:
        resp = execute_prompt_chain(prompt_chain, gpt_ver=gpt_ver)
        gpt_output = parse_gpt_resp(resp)
        print('Committing with message: ' + gpt_output)
        do_git_commit(gpt_output)


def goc():
    cli = click.CommandCollection(sources=[diff_cmd, commit_cmd])
    cli()


if __name__ == '__main__':
    goc()
