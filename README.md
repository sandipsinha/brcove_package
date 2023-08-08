# brcove_package
A simple python assesment from BrightCove
# brightCove Package

This is a simple program to input a file. The name is specified as an input paramater(required). Once
it is able to read the file successfully, it formats it by parsing the date and time stamp field to a 
date string, summarizes it by grouping by date,accountid and metric. It also filters out the rows which does not have integer account Ids. 

## How to Install: ##
Unzip the contents in a folder. 
Create a virtual environment. 
Install build by running --> pip install build. (make sure that the file pyproject.toml is in the same folder at the same level)
Then run python -m build --wheel
It will create a file by the name brcov_ssinha-0.0.1-py3-none-any.whl under the dist folder.
run a pip install of that file brcov_ssinha-0.0.1-py3-none-any.whl from any virtual environment
Finally run it using this command 
start_ingestin <absolute path of the input file name>
It should create output in the format as below

start_ingesting /Users/sandipsinha/pythoncodes/atest/brcov_ssinha/data_input.csv   
### Output Display ###             
Script name: /Users/sandipsinha/litmus_test/avenv/bin/start_ingesting
The filename is /Users/sandipsinha/pythoncodes/atest/brcov_ssinha/data_input.csv
The row number 7 is dropped due to invalid accountID 1.32 , Conversion Error
the sorted list is ['date','accountid']
      date  accountid      metric  total_usage
2022-03-21          1       likes        70.00
2022-03-31          1 null_values        50.00
2022-12-24          4      amount         2.61
2023-04-02          5       bytes         0.25
2023-04-02         10       bytes         5.73
2023-04-02         10       likes         2.00

##Finally the tests folder contains various test cases which can be run by this command ##
python -m pytest brcov_ssinha/tests/test_bcove_ingest_file.py
