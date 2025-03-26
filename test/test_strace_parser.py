import os
import csv
import unittest
from unittest.mock import patch, mock_open, MagicMock
from strace_parser import fileReader, create_headers, check_input_dir_exits, check_output_file, all_dicts

class TestStraceParser(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment for the test case.

        This method initializes the following:
        - A test directory (`test_dir`) and a test file (`test_file`) within it.
        - A CSV file name (`test_csv`) for output purposes.
        - Test data (`test_data`) simulating input lines, including syscall information.
        - An expected dictionary (`expected_dict`) containing parsed syscall data.
        - Expected headers (`expected_headers`) for CSV output.

        Additionally, it creates the mock directory and writes the test data to the test file.
        """
        """Set up test environment."""
        self.test_dir = "test_dir"
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        self.test_csv = "output.csv"
        self.test_data = [
            "line1\n",
            "line2\n",
            "syscall1 0 0 10 syscall_name1\n",
            "syscall2 0 0 20 syscall_name2\n",
            "line_last1\n",
            "line_last2\n"
        ]
        self.expected_dict = {
            "filename": self.test_file,
            "syscall_name1": "10",
            "syscall_name2": "20"
        }
        self.expected_headers = ["filename", "label", "syscall_name1", "syscall_name2"]

        # Create a mock directory and file
        os.makedirs(self.test_dir, exist_ok=True)
        with open(self.test_file, "w") as f:
            f.writelines(self.test_data)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
        all_dicts.clear()

    def test_fileReader(self):
        """Test the fileReader function."""
        fileReader(self.test_file)
        self.assertEqual(len(all_dicts), 1)
        self.assertEqual(all_dicts[0], self.expected_dict)

    def test_fileReader_with_directory(self):
        """Test fileReader with a directory instead of a file."""
        with patch("builtins.print") as mock_print:
            fileReader(self.test_dir)
            mock_print.assert_called_with("Error: File is a directory, skipping")
        self.assertEqual(len(all_dicts), 0)

    def test_create_headers(self):
        """Test the create_headers function."""
        all_dicts.append(self.expected_dict)
        create_headers(self.test_csv, label="test_label")
        self.assertTrue(os.path.exists(self.test_csv))

        with open(self.test_csv, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(headers, self.expected_headers)

            row = next(reader)
            self.assertEqual(row[0], self.expected_dict["filename"])
            self.assertEqual(row[1], "test_label")
            self.assertEqual(row[2], self.expected_dict["syscall_name1"])
            self.assertEqual(row[3], self.expected_dict["syscall_name2"])

    def test_check_input_dir_exits(self):
        """Test check_input_dir_exits with an existing directory."""
        result = check_input_dir_exits(self.test_dir)
        self.assertEqual(result, self.test_dir)

    def test_check_input_dir_exits_nonexistent(self):
        """Test check_input_dir_exits with a nonexistent directory."""
        with patch("builtins.print") as mock_print, self.assertRaises(SystemExit):
            check_input_dir_exits("nonexistent_dir")
            mock_print.assert_called_with("Directory does not exist")

    def test_check_output_file(self):
        """Test check_output_file with a non-existing file."""
        result = check_output_file(self.test_csv)
        self.assertEqual(result, self.test_csv)

    def test_check_output_file_existing(self):
        """Test check_output_file with an existing file."""
        with open(self.test_csv, "w") as f:
            f.write("test")
        with patch("builtins.print") as mock_print, self.assertRaises(SystemExit):
            check_output_file(self.test_csv)
            mock_print.assert_called_with("Error: CSV file already exists")


if __name__ == "__main__":
    unittest.main()