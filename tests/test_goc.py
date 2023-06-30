from goc import goc as target
import unittest
from unittest.mock import patch


class ExecBashCmdTests(unittest.TestCase):
    @patch("os.popen")
    def test_exec_bash_cmd(self, mock_popen):
        mock_popen.return_value.read.return_value = "command_output\n"
        cmd = "some_command"

        result = target.exec_bash_cmd(cmd)

        self.assertEqual(result, "command_output")
        mock_popen.assert_called_with(cmd)
        mock_popen.return_value.read.assert_called_once()

    @patch("os.popen")
    def test_exec_bash_cmd_multiple_lines_output(self, mock_popen):
        mock_popen.return_value.read.return_value = "line1\nline2\nline3\n"
        cmd = "some_command"

        result = target.exec_bash_cmd(cmd)

        self.assertEqual(result, "line1\nline2\nline3")
        mock_popen.assert_called_with(cmd)
        mock_popen.return_value.read.assert_called_once()

if __name__ == "__main__":
    unittest.main()

