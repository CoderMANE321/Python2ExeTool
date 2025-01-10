"""

Author: Deonta Williams

 

Purpose: Aggregrate CSV files

 

Date Created: 12/11/2024

"""

 

import os

import sys

import logging

import re

from typing import List, Optional

import pandas as pd

 

# logging

logging.basicConfig(

    level=logging.INFO,

    format='{} - {}: {}'.format('%(asctime)s', '%(levelname)s', '%(message)s')

)

 

class FileValidator:

    @staticmethod

    def validate_file_paths(file_paths: List[str]) -> List[str]:

        """

        Validate that all provided file paths exist and are readable CSV files.

       

        Args:

            file_paths (List[str]): List of file paths to validate

       

        Returns:

            List[str]: Filtered list of valid file paths

       

        Validates:

        - Path exists

        - Is a file

        - Is a CSV file

        """

        valid_paths = []

        for path in file_paths:

            try:

                # Check if path exists and is a file

                if not os.path.exists(path):

                    logging.warning('Path does not exist: {}'.format(path))

                    continue

               

                # Check if it's a file (not a directory)

                if not os.path.isfile(path):

                    logging.warning('Not a file: {}'.format(path))

                    continue

               

                # Check file extension

                if not path.lower().endswith('.csv'):

                    logging.warning('Not a CSV file: {}'.format(path))

                    continue

               

                valid_paths.append(path)

           

            except Exception as e:

                logging.error('Error validating path {}: {}'.format(path, e))

       

        return valid_paths

 

class FileParser:

    @staticmethod

    def parse_file_string(file_string: str, base_path: str) -> List[str]:

        """

        Parse a comma-separated string of file names into full file paths.

       

        Args:

            file_string (str): Comma-separated list of file names

            base_path (str): Base directory path

       

        Returns:

            List[str]: Full file paths

        """

        # Use regex to split file names, handling various delimiters

        file_parse_regex = r'[^,\s]+'

        matches = re.findall(file_parse_regex, file_string)

       

        # Convert file names to full paths

        file_paths = [os.path.join(base_path, match.strip()) for match in matches]

       

        return file_paths

 

class CSVProcessor:

    @staticmethod

    def read_and_concat_csvs(file_paths: List[str]) -> Optional[pd.DataFrame]:

        """

        Read multiple CSV files and concatenate them into a single DataFrame.

       

        Args:

            file_paths (List[str]): List of validated CSV file paths

       

        Returns:

            Optional[pd.DataFrame]: Concatenated DataFrame, or None if no files processed

        """

        if not file_paths:

            logging.warning('No valid files to process')

            return None

       

        dataframes = []

       

        for file in file_paths:

            try:

                # Read CSV file

                df = pd.read_csv(file)

               

                # Log successful file processing

                logging.info('Successfully processed: {}'.format(file))

               

                dataframes.append(df)

           

            except pd.errors.EmptyDataError:

                logging.warning('Empty file: {}'.format(file))

            except Exception as e:

                logging.error('Error processing {}: {}'.format(file, e))

       

        # Concatenate all processed DataFrames

        if dataframes:

            return pd.concat(dataframes, ignore_index=True)

       

        logging.warning('No DataFrames were processed')

        return None

 

class FileWriter:

    @staticmethod

    def save_dataframe(

        dataframe: pd.DataFrame,

        base_path: str,

        filename: str = 'aggregated_data.csv'

    ) -> str:

        """

        Save DataFrame to a CSV file.

       

        Args:

            dataframe (pd.DataFrame): DataFrame to save

            base_path (str): Base directory path

            filename (str, optional): Output filename. Defaults to 'aggregated_data.csv'

       

        Returns:

            str: Full path of the saved file

        """

        try:

            # Create full output file path

            out_file = os.path.join(base_path, filename)

           

            # Save DataFrame to CSV

            dataframe.to_csv(out_file, index=False)

           

            logging.info('Aggregated data saved to {}'.format(out_file))

            return out_file

       

        except Exception as e:

            logging.error('Error saving file: {}'.format(e))

            raise

 

class DataAggregator:

    def __init__(self, file_string: str):

        """

        Initialize DataAggregator with file string to process.

       

        Args:

            file_string (str): Comma-separated list of file names

        """

        self.file_string = file_string

        self.base_path = os.getcwd()

        self.dataframe = None

   

    def process(self) -> Optional[str]:

        """

        Execute the complete data aggregation workflow.

       

        Returns:

            Optional[str]: Path of the saved aggregated file, or None if processing failed

        """

        try:

            # Parse file string into potential file paths

            file_paths = FileParser.parse_file_string(self.file_string, self.base_path)

           

            # Validate file paths

            valid_paths = FileValidator.validate_file_paths(file_paths)

           

            # Process and concatenate CSVs

            self.dataframe = CSVProcessor.read_and_concat_csvs(valid_paths)

           

            # Validate DataFrame exists before saving

            if self.dataframe is not None:

                return FileWriter.save_dataframe(self.dataframe, self.base_path)

           

            logging.warning('No data to save')

            return None

       

        except Exception as e:

            logging.error('Data aggregation failed: {}'.format(e))

            return None

 

def main():

    try:

        # Validate command-line argument

        if len(sys.argv) < 2:

            logging.error('Please provide a comma-separated list of CSV files')

            sys.exit(1)

       

        # Get file string from command-line argument

        file_string = sys.argv[1]

       

        # Create and process DataAggregator

        aggregator = DataAggregator(file_string)

        result = aggregator.process()

       

        if result:

            print('Processing complete. Output file: {}'.format(result))

        else:

            print('Processing failed. Check logs for details.')

   

    except Exception as e:

        logging.error('Unexpected error in main execution: {}'.format(e))

        sys.exit(1)

 

# Ensure script is run directly

if __name__ == "__main__":

    main()