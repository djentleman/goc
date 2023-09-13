from goc import goc
import unittest
from unittest.mock import patch


class ExecBashCmdTests(unittest.TestCase):
    @patch("os.popen")
    def test_exec_bash_cmd(self, mock_popen):
        mock_popen.return_value.read.return_value = "command_output\n"
        cmd = "some_command"

        result = goc.exec_bash_cmd(cmd)

        self.assertEqual(result, "command_output")
        mock_popen.assert_called_with(cmd)
        mock_popen.return_value.read.assert_called_once()

    @patch("os.popen")
    def test_exec_bash_cmd_multiple_lines_output(self, mock_popen):
        mock_popen.return_value.read.return_value = "line1\nline2\nline3\n"
        cmd = "some_command"

        result = goc.exec_bash_cmd(cmd)

        self.assertEqual(result, "line1\nline2\nline3")
        mock_popen.assert_called_with(cmd)
        mock_popen.return_value.read.assert_called_once()

class DocumentGitDiffWrapTests(unittest.TestCase):
    @patch("goc.goc.exec_bash_cmd")
    def test_document_git_diff_wrap_with_diff(self, mock_exec_bash_cmd):
        mock_exec_bash_cmd.return_value = "git_diff_output"
        args = ["--stat", "commit_hash"]

        expected_prompt_chain = [
        'When I send you a git diff, write documentation of the diff in markdown for a pull request',
        """Please use this format for the git diff

# Git Commit Diff

## Description
- Briefly describe the changes made in this commit.

## Files Modified
- List the files that were modified in this commit:

  - `file1.ext`: Describe changes made in this file.
  - `file2.ext`: Explain modifications in this file.
  - ...

## Changes Made
- Specify the changes made to each file, including additions, deletions, and modifications.
    """,
            "git_diff_output"
        ]

        result = goc.document_git_diff_wrap(args)

        self.assertEqual(result, expected_prompt_chain)
        mock_exec_bash_cmd.assert_called_with("git diff --stat commit_hash")

    @patch("goc.goc.exec_bash_cmd")
    def test_document_git_diff_wrap_no_diff(self, mock_exec_bash_cmd):
        mock_exec_bash_cmd.return_value = ""
        args = ["--stat", "commit_hash"]

        expected_prompt_chain = []

        result = goc.document_git_diff_wrap(args)

        self.assertEqual(result, expected_prompt_chain)
        mock_exec_bash_cmd.assert_called_with("git diff --stat commit_hash")

class GitCommitWrapTests(unittest.TestCase):
    @patch("goc.goc.exec_bash_cmd")
    def test_git_commit_wrap_with_diff(self, mock_exec_bash_cmd):
        mock_exec_bash_cmd.return_value = "git_diff_output"

        expected_prompt_chain = [
        'When I send you a git diff, write a commit message in 50 characters or less, do not include "git commit" or the character count',
        f'Please use this format for the git diff\n\n<Fix|Add|Update|Refactor|Docs>: <commit message>',
            "git_diff_output"
        ]

        result = goc.git_commit_wrap()

        self.assertEqual(result, expected_prompt_chain)
        mock_exec_bash_cmd.assert_called_with("git diff --staged")

    @patch("goc.goc.exec_bash_cmd")
    def test_git_commit_wrap_no_diff(self, mock_exec_bash_cmd):
        mock_exec_bash_cmd.return_value = ""

        expected_prompt_chain = []

        result = goc.git_commit_wrap()

        self.assertEqual(result, expected_prompt_chain)
        mock_exec_bash_cmd.assert_called_with("git diff --staged")

class ParseGptRespTests(unittest.TestCase):
    def test_parse_gpt_resp(self):
        resp = {
            'choices': [
                {
                    'message': {
                        'content': 'This is the GPT output.'
                    }
                }
            ]
        }

        expected_output = 'This is the GPT output.'

        result = goc.parse_gpt_resp(resp)

        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()

