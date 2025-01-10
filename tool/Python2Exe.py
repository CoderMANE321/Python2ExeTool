'''

Description: Test Python by running it and converting it to an executable

Author:      Deonta Williams

Date Created: 1/10/2024

'''

 

from pathlib import Path

import sys

import subprocess

import PyInstaller.__main__

import logging

 

# Set up logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

 
# check if file exists and is a python file
def validate_file(file: str):

    path = Path(file)

    if not path.exists():

        logging.error(f"Error: File '{file}' does not exist.")

        sys.exit(1)

    if not path.suffix == ".py":

        logging.error(f"Error: File '{file}' is not a Python file.")

        sys.exit(1)

    return path

 
# handle yes or no input
def get_yes_no(prompt: str) -> bool:

    while True:

        answer = input(prompt).strip().lower()

        if answer in ["y", "n"]:

            return answer == "y"

        logging.warning("Invalid input. Please enter 'y' or 'n'.")

 

class Executer:

    def __init__(self, file=None):

        self.file = Path(file)

 
    # grabs imports from user
    def get_imports(self) -> list:

        logging.info("Enter all your third-party imports. View an example below of how the string should be entered.")

        string = input("Example: string = 'chardet, pandas'\n\n")

        final_string = [imp.strip() for imp in string.split(",")]

        logging.info(f"Entered imports: {final_string}")

       

        if len(string) > 2:

            return None

       

        logging.info("\nYour entered imports:")

        return final_string

 
    # handle test file arguments
    def handle_test_file_arguments(self) -> list:

        argument_question = get_yes_no("\nDo you need to input arguments for your test file? (y/n): ")

        if argument_question:

            test_file_arguments = input("Separate each testing argument with a tilde (~): ")

            final_arguments = [arg.strip() for arg in test_file_arguments.split("~")]

            return final_arguments

        else:

            return []

 
    # test file execution
    def test_file(self) -> bool:

        arguments = self.handle_test_file_arguments()

        command = ["python", str(self.file)] + arguments

 

        if self.file.exists():

            logging.info(f"Testing file '{self.file}' with arguments: {arguments}")

            subprocess.Popen(command)

            logging.info("Python syntax is fine! Ready to turn into an executable.")

            return True

       

        logging.error(f"Error: File '{self.file}' does not exist or is invalid.")

        return False

 
    # compile python file to executable
    def compile_python(self):

        import_string = self.get_imports()

        logging.info("Compiling Python into an executable....")

 

        try:

            if isinstance(import_string, list):

                PyInstaller.__main__.run([

                    str(self.file),

                    '--onefile',

                    '--windowed',

                    '--hidden-import=' + ','.join(import_string),

                ])

            else:

                PyInstaller.__main__.run([

                    str(self.file),

                    '--onefile',

                    '--windowed',

                ])

        except Exception as e:

            logging.error(f"Error during compilation: {e}")

 
# entry point
def main():

    if len(sys.argv) < 2:

        logging.error("Usage: python script.py <filename>")

        sys.exit(1)

   

    file = validate_file(sys.argv[1])

    compile_file = True

 

    executer = Executer(file)

    while compile_file:

        test_question = input("\nDid your test pass or execute? (q to quit) \n").strip().lower()

        print("\n")

       

        if test_question == "q":

            compile_file = False

        elif executer.test_file() and test_question == "y":

            logging.info("Results of file are:\n")

            executer.compile_python()

            break

 

if __name__ == "__main__":

    main()