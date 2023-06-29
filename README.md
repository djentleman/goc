# GOC

This script, `goc.py`, is a utility tool that leverages the OpenAI GPT-3.5 Turbo model to generate Markdown documentation for Git diffs and commits. It provides three main functionalities:

1. **Document Latest Commit**: This function compares the latest two commits and generates documentation based on the differences between them.

2. **Document Comparison vs Current Commit**: This function compares the changes made in a specific commit to the current state of the repository and generates documentation accordingly.

3. **Document Comparison of Two Commits**: This function compares the differences between two specific commits and generates documentation based on the changes.

## Prerequisites

To use this tool, ensure that you have the following prerequisites installed:

- `openai` Python library
- Git (version control system)

## Usage

To execute the script, run the following command:

```bash
python goc.py [arguments]
```

Replace `[arguments]` with the appropriate options based on your requirement:

- **Document Latest Commit**:
  ```bash
  python goc.py
  ```

- **Document Comparison vs Current Commit**:
  ```bash
  python goc.py [commit_hash]
  ```

- **Document Comparison of Two Commits**:
  ```bash
  python goc.py [commit_a] [commit_b]
  ```

## Output

The script generates Markdown documentation by utilizing the OpenAI GPT-3.5 Turbo model. The resulting documentation will be displayed in the console output.

## Note

Make sure you have the necessary permissions and access to the Git repository you intend to analyze. Also, ensure that the repository is properly cloned on your local machine.

## Disclaimer

This tool relies on the OpenAI GPT-3.5 Turbo model for generating documentation. The accuracy and quality of the generated content depend on the model's training data and the provided input. Please review and validate the generated documentation before using it in your projects.
