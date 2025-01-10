import unittest

import subprocess

from pathlib import Path

import os

import tempfile

 

class TestExecuter(unittest.TestCase):

 

    def setUp(self):

        """

        Set up a temporary Python file and its corresponding executable for testing.

        """

        # Create a temporary Python file

        self.test_script = Path(tempfile.gettempdir()) / "test_script.py"

        with open(self.test_script, "w") as f:

            f.write(

                "import sys\n"

                "if __name__ == '__main__':\n"

                "    print('Arguments:', sys.argv[1:])\n"

            )

 

        self.test_executable = self.test_script.with_suffix('.exe')

 

    def tearDown(self):

        """

        Clean up the test files.

        """

        if self.test_script.exists():

            self.test_script.unlink()

        if self.test_executable.exists():

            self.test_executable.unlink()

 

    def run_script(self, file_path, args):

        """

        Helper method to run a Python or executable file and capture the output.

        """

        command = [str(file_path)] + args

        result = subprocess.run(command, capture_output=True, text=True, shell=False)

        return result.stdout.strip()

 

    def test_python_file_output(self):

        """

        Test that the Python file produces the expected output.

        """

        args = ["arg1", "arg2", "arg3"]

        expected_output = f"Arguments: {args}"

 

        # Run the Python file and compare the output

        output = self.run_script("python", [self.test_script] + args)

        self.assertEqual(output, expected_output, "Python file output did not match the expected output.")

 

    def test_executable_file_output(self):

        """

        Test that the executable file produces the same output as the Python file.

        """

        args = ["arg1", "arg2", "arg3"]

 

        # Run the Python file

        python_output = self.run_script("python", [self.test_script] + args)

 

        # Compile the Python file into an executable

        import PyInstaller.__main__

        PyInstaller.__main__.run([

            str(self.test_script),

            '--onefile',

            '--windowed',

            '--distpath', tempfile.gettempdir(),

            '--name', self.test_script.stem

        ])

 

        # Run the executable and compare outputs

        executable_path = Path(tempfile.gettempdir()) / self.test_script.stem

        executable_output = self.run_script(executable_path, args)

 

        self.assertEqual(executable_output, python_output, "Executable output did not match Python file output.")

 

if __name__ == '__main__':

    unittest.main()