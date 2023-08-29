import openai
import os
import json
import argparse

def exec_bash_cmd(cmd):
    return os.popen(cmd).read()[:-1]

def document_git_diff_wrap(args):
    fmt_args = " ".join(args)
    cmd = f"git diff {fmt_args}"
    git_diff = exec_bash_cmd(cmd)
    if len(git_diff) == 0:
        print('No Git Diff Found')
        return []
    prompt_chain = [
        'I send you a git diff, and you write documentation of the commit in markdown',
        git_diff
    ]
    return prompt_chain

def git_commit_wrap():
    cmd = f"git diff --staged"
    git_diff = exec_bash_cmd(cmd)
    if len(git_diff) == 0:
        print('No Git Diff Found')
        return []
    prompt_chain = [
        'I send you a git diff, and you write a commit message in 50 characters or less, do not include "git commit"',
        git_diff
    ]
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

def print_help_text():
    helptext = """
Usage: goc <mode> <args>

Modes:
  diff <args>      Generate documentation for the git diff between commits or files.
  commit           Generate a commit message for the current git diff.

Options:
  help             Show this help text.

"""
    print(helptext)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['commit', 'diff', 'help'], default='help')
    parser.add_argument('--gpt_ver', default='3.5-turbo')

    args, gitargs = parser.parse_known_args()
    return args, gitargs

def goc():
    args, gitargs = get_args()
    prompt_chain = []
    if args.mode == 'help':
        print_help_text()
        return
    if args.mode == 'diff':
        # just pass the args directly into git diff
        prompt_chain = document_git_diff_wrap(gitargs)
    elif args.mode == 'commit':
        # get description of the current diff
        prompt_chain = git_commit_wrap()

    if len(prompt_chain) > 0:
        resp = execute_prompt_chain(prompt_chain, gpt_ver=args.gpt_ver)
        gpt_output = parse_gpt_resp(resp)
        if args.mode == 'diff':
            print(gpt_output)
        elif args.mode == 'commit':
            print('Committing with message: ' + gpt_output)
            do_git_commit(gpt_output)


if __name__ == '__main__':
    goc()
