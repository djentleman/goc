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
            'I send you a git diff, and you write documentation of the commit in markdown',
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
            'I send you a git diff, and you write a commit message in 50 characters or less, do not include "git commit"',
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

if __name__ == "__main__":
    unittest.main()

