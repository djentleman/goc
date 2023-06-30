# GOC

This script, `goc.py`, is a utility tool that leverages the OpenAI GPT-3.5 Turbo model to generate Markdown documentation for Git diffs and commits. It can be used to automatically generate a markdown document based on the output of git diff:


## Prerequisites

You will need an OpenAI API key, configure it to the environment variable like below:

```bash
export OPENAI_API_KEY=<your_key_here>
```

You will need a python version higher than 3.8

## Installation

You can either install from Pypi (https://pypi.org/project/goc/)
```bash
pip install goc
```

Or you can download this repository and run

```bash
poetry install
```

## Usage

To execute the script, run the following command:

```bash
goc [mode] [arguments]
```

Replace [mode] with one of the following options:

diff: Generate documentation for the git diff between commits or files.
commit: Generate a commit message for the current git diff.
Replace [arguments] based on the mode selected:

For the diff mode, provide the arguments to specify the commits or files to compare.
For the commit mode, no additional arguments are needed.

- **Generate documentation for the diff between two commits**:
  ```bash
  goc diff [commit_a] [commit_b]
  ```

- **Document Comparison vs Current Commit**:
  ```bash
  goc diff [commit_hash]
  ```

- **Document Comparison of a single commit**:
  ```bash
  goc diff [commit_hash]^!
  ```

- **Document Staged Changes**:
  ```bash
  goc diff --staged
  ```

- **Automatically generate commit message and commit**:
  ```bash
  goc commit
  ```

## Output

The script generates Markdown documentation by utilizing the OpenAI GPT-3.5 Turbo model. The resulting documentation will be displayed in the console output.


## Examples

```bash
$ goc diff a0f72101be85667a362425c2cdc30ef794e2a738
## Commit Details

- **Commit Type:** Code update
- **Commit Scope:** goc.py, pyproject.toml
- **Commit Description:**

### goc.py
1. Removed the `document_comparison_vs_current_commit` and `document_comparison_of_2_commits` functions as they were not being used.
2. Created a new function `document_git_diff_wrap` that takes command line arguments and runs the `git diff` command with those arguments. This allows for easy comparison of commits by passing the commit hashes or branches directly as arguments.
3. Modified the `goc` function to handle different scenarios based on the number of command line arguments passed. If no arguments are provided, it compares the latest two commits. If one or more arguments are provided, it passes them directly to `document_git_diff_wrap` for comparison.
4. updated the `parse_gpt_resp` function to return the content of the last choice/message in the response, as the final generated markdown content is usually the last choice.

### pyproject.toml
1. Updated the version to `"0.2.0"`.

Please review and merge these changes.
```

```bash
$ goc commit
Committing with message: "Update git diff handling, handle case when no diff is found"
```

## Note

Make sure you have the necessary permissions and access to the Git repository you intend to analyze. Also, ensure that the repository is properly cloned on your local machine.

## Disclaimer

This tool relies on the OpenAI GPT-3.5 Turbo model for generating documentation. The accuracy and quality of the generated content depend on the model's training data and the provided input. Please review and validate the generated documentation before using it in your projects.
