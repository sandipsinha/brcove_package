import pendulum as dp
import pandas as pd
import numpy as np
import sys
import argparse
from brcov_ssinha import dataconfig as cfg
from brcov_ssinha import bcove_helper as hp
""" This is a small program which is designed to read a csv file, parse, curate and summarize 
    and then print it out (along with any exceptions)"""


parser = argparse.ArgumentParser(description="Ingesting a csv file",
                                 formatter_class=argparse.
                                 ArgumentDefaultsHelpFormatter)
parser.add_argument('fname', help='Name(with)absolute path  of the input file')
parser.add_argument('--sort_order', help='Please specify the sort order a list'
                    'as a string for ex "[col1, col2]" etc')


class create_a_file_object():

    def __init__(self, afilename: str):
        # accepts a input filename as a paramater and then creates a pandas
        # dataframe, else raises a file read error
        try:
            self.adf = pd.read_csv(afilename, index_col=None, header=None)
            self.adf.columns = cfg.header_cols
        except FileNotFoundError:
            print('The file {} was not found'.format(afilename))
            self.adf = pd.DataFrame([])
        except Exception as e:
            print('The error encountered is {}'.format(e.args))
            self.adf = pd.DataFrame([])

    def convert_ts_to_date_string(self):
        # Parses the timestamp column with a date string in the dataframe
        self.adf['date'] = self.adf['date'].apply(lambda x:
                                                  dp.parse(x, strict=False)
                                                  .to_date_string())

    def curate_invalid_account_ids(self):
        # calls a function repeatedly to ensure that the account ID has the right
        # data type
        for i in self.adf.index.tolist():
            # The second item in the dataframe is account id, index = 1
            value = self.adf.iloc[i, 1]
            try:
                hp.check_desired_format(value)
            except Exception as e:
                self.adf.drop(i, inplace=True)
                print('The row number {} is dropped due to invalid accountID {} , {}'.
                      format(i, value, e))
        self.adf['accountid'] = self.adf['accountid'].astype('int64')

    def clean_n_curate_data(self):
        # Replace null value with 'null_value' literal
        self.adf.replace(np.nan, 'null_values', regex=True, inplace=True)
        # Removes the row if there is a invalid datatype for accountid
        # Format the date time string to a date string
        self.curate_invalid_account_ids()
        self.convert_ts_to_date_string()


    def sort_n_summarize_data(self):
        # groups and sort the data as specified in the config file
        sorted_list = hp.read_and_get_sort_columns()
        print('the sorted list is {}'.format(sorted_list))
        d_list = eval(sorted_list)
        self.adf = self.adf.groupby(cfg.group_list).agg(cfg.agg_dict).sort_values(by=d_list)
        self.adf.columns = ['total_usage']
        self.adf = self.adf.reset_index()
        
    def display_data(self):
        # prints the dataframe without the row numbers
        print(self.adf.to_string(index=False))


def ingest_and_process_file(filename: str):
    # Accepts a filename where it expects to find the input data
    # ingests it as a dataframe, curates and summarizes the data, filters
    # out the invalid data and prints the sorted (as specified by the ) 
    print('The filename is {}'.format(filename))
    input_file = create_a_file_object(filename)
    if input_file.adf.empty:
        print('Input file was blank or could not be ingested')
    else:
        input_file.clean_n_curate_data()
        input_file.sort_n_summarize_data()
        input_file.display_data()


def main():
    # Main script of program, Formats the input params and initiates the main 
    # function
    script_name = sys.argv[0]
    print("Script name:", script_name)
    args = parser.parse_args()
    config = vars(args)
    ingest_and_process_file(config.get('fname'))


if __name__ == '__main__':
    main()
