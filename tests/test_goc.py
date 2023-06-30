import goc as target
import unittest
from unittest.mock import patch

class DocumentLatestCommitTests(unittest.TestCase):
    @patch("your_module.exec_bash_cmd")
    def test_document_latest_commit(self, mock_exec_bash_cmd):
        # Mocking the output of exec_bash_cmd
        mock_exec_bash_cmd.return_value = "commit_hash_1\ncommit_hash_2\n"

        expected_prompt_chain = [
            'I send you a git diff, and you write documentation of the commit in markdown',
            "git_diff_output"
        ]

        with patch("target.exec_bash_cmd") as mock_exec_bash_cmd:
            mock_exec_bash_cmd.return_value = "git_diff_output"
            result = target.document_latest_commit()

        self.assertEqual(result, expected_prompt_chain)
        mock_exec_bash_cmd.assert_called_with("git log | egrep '^commit ' | head -n 2 | awk '{print $NF}'")
        mock_exec_bash_cmd.assert_called_with("git diff commit_hash_1 commit_hash_2")

if __name__ == "__main__":
    unittest.main()

