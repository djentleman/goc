import openai
import os
import sys
import json

def exec_bash_cmd(cmd):
    return os.popen(cmd).read()[:-1]

def document_latest_commit():
    # compare latest 2 commits
    commit_hashes = exec_bash_cmd("git log | egrep '^commit ' | head -n 2 | awk '{print $NF}'")
    latest_commit, prev_commit = commit_hashes.split('\n')
    cmd = f"git diff {prev_commit} {latest_commit}"
    git_diff = exec_bash_cmd(cmd)
    prompt_chain = [
        'I send you a git diff, and you write documentation of the commit in markdown',
        git_diff
    ]
    return prompt_chain

def document_git_diff_wrap(args):
    fmt_args = " ".join(args)
    cmd = f"git diff {fmt_args}"
    git_diff = exec_bash_cmd(cmd)
    prompt_chain = [
        'I send you a git diff, and you write documentation of the commit in markdown',
        git_diff
    ]
    return prompt_chain

def git_commit_wrap():
    # compare latest 2 commits
    commit_hash = exec_bash_cmd("git log | egrep '^commit ' | head -n 1 | awk '{print $NF}'")
    cmd = f"git diff {commit_hash}"
    git_diff = exec_bash_cmd(cmd)
    prompt_chain = [
        'I send you a git diff, and you write a commit message in 50 characters or less, do not include "git commit"',
        git_diff
    ]
    return prompt_chain

def execute_prompt_chain(prompt_chain):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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
    n_args = len(sys.argv) - 1
    if n_args == 0:
        print('No Arguments, Please run "goc <mode> <args>"')
        mode = 'help'
    elif n_args > 0:
        mode = sys.argv[1]
    return mode

def goc():
    mode = get_args()
    if mode == 'help':
        print_help_text()
        return
    if mode == 'diff':
        # just pass the args directly into git diff
        prompt_chain = document_git_diff_wrap(sys.argv[2:])
    elif mode == 'commit':
        # get description of the current diff
        prompt_chain = git_commit_wrap()

    resp = execute_prompt_chain(prompt_chain)
    gpt_output = parse_gpt_resp(resp)
    if mode == 'diff':
        print(gpt_output)
    elif mode == 'commit':
        print('Committing with message: ' + gpt_output)
        do_git_commit(gpt_output)


if __name__ == '__main__':
    goc()
