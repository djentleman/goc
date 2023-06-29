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

def document_comparison_vs_current_commit(benchmark):
    cmd = f"git diff {benchmark}"
    git_diff = exec_bash_cmd(cmd)
    prompt_chain = [
        'I send you a git diff, and you write documentation of the commit in markdown',
        git_diff
    ]
    return prompt_chain

def document_comparison_of_2_commits(commit_a, commit_b):
    cmd = f"git diff {commit_a, commit_b}"
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
    md_output = resp['choices'][0]['message']['content']
    return md_output

def goc():
    n_args = len(sys.argv) - 1
    if n_args == 0:
        prompt_chain = document_latest_commit()
    elif n_args == 1:
        prompt_chain = document_comparison_vs_current_commit(sys.argv[1])
    elif n_args == 2:
        prompt_chain = document_comparison_of_2_commits(sys.argv[1], sys.argv[2])
    resp = execute_prompt_chain(prompt_chain)
    md_output = parse_gpt_resp(resp)
    print(md_output)


if __name__ == '__main__':
    goc()
