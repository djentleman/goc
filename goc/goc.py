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

def document_comparison_vs_current_commit(args):
    fmt_args = " ".join(args)
    cmd = f"git diff {fmt_args}"
    git_diff = exec_bash_cmd(cmd)
    prompt_chain = [
        'I send you a git diff, and you write documentation of the commit in markdown',
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
    md_output = resp['choices'][-1]['message']['content']
    return md_output

def goc():
    n_args = len(sys.argv) - 1
    if n_args == 0:
        # compare the latest 2 commits
        prompt_chain = document_latest_commit()
    elif n_args > 0:
        # just pass the args directly into git diff
        prompt_chain = document_git_diff_wrap(sys.argv[1:])
    resp = execute_prompt_chain(prompt_chain)
    md_output = parse_gpt_resp(resp)
    print(md_output)


if __name__ == '__main__':
    goc()
