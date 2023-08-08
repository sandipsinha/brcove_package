import pytest
from mock import patch
from brcov_ssinha import bcove_ingest_file as bcif
import pandas as pd

@pytest.fixture
def get_file_name():
    file_name = 'atest_file.csv'
    return file_name


@pytest.fixture
def get_fake_dframe(): 
    alist = [{'date': '2022-04-10T14:23:47Z', 'accountid': 20,
              'metric': 'likes', 'usage': 10},
             {'date': '2022-05-14T12:23:47Z', 'accountid': 10,
              'metric': 'bytes', 'usage': 20},
             {'date': '2022-05-14T10:23:47Z', 'accountid': 10,
              'metric': 'bytes', 'usage': 50}]
    return pd.DataFrame(alist)

@pytest.fixture
def get_dframe_wrong_dtype(): 
    alist = [{'date': '2022-04-10T14:23:47Z', 'accountid': 20,
              'metric': 'likes', 'usage': 10},
             {'date': '2022-05-14T12:23:47Z', 'accountid': 10.44,
              'metric': 'bytes', 'usage': 20}]
    return pd.DataFrame(alist)


@pytest.fixture
def get_dframe_null_accountid(): 
    alist = [{'date': '2022-04-10T14:23:47Z', 'accountid': 1,
              'metric': None, 'usage': 10},
             {'date': '2022-05-14T12:23:47Z', 'accountid': 10.44,
              'metric': 'bytes', 'usage': 20}]
    return pd.DataFrame(alist)


def test_summary_and_group_by(get_fake_dframe):
    # A test to make sure it is able to summarize rows with the same date
    # and accountid and usage being summarized 
    with patch.object(bcif.create_a_file_object, "__init__", lambda x,y : None):
        afile = bcif.create_a_file_object('afilename')
        afile.adf = get_fake_dframe
        # Before summarization
        assert len(afile.adf) == 3
        afile.convert_ts_to_date_string()
        afile.sort_n_summarize_data()
        # After summarization
        assert len(afile.adf) == 2


def test_filtering_bad_accounts(get_dframe_wrong_dtype):
    # A test to make sure it is able to detect wrong account ids and
    # filter it out
    with patch.object(bcif.create_a_file_object, "__init__", 
                      lambda x, y: None):
        afile = bcif.create_a_file_object('afilename')
        afile.adf = get_dframe_wrong_dtype
        # Before curation
        assert len(afile.adf) == 2
        afile.curate_invalid_account_ids()
        # After curation
        assert len(afile.adf) == 1


def test_reading_null_accountid(get_dframe_null_accountid):
    # To test if the process indeed takes note of the null usage column
    # and replaces them with a literal
    with patch.object(bcif.create_a_file_object, "__init__", 
                      lambda x, y: None):
        afile = bcif.create_a_file_object('afilename')
        afile.adf = get_dframe_null_accountid
        pre_curate_list = afile.adf['metric'].tolist()
        assert 'null_values' not in pre_curate_list
        afile.clean_n_curate_data()
        post_curate_list = afile.adf['metric'].tolist()
        assert 'null_values' in post_curate_list


def test_ingest_file_name(get_file_name):
    # to make sure that the process rejects a wrong file
    # at the start
    assert bcif.create_a_file_object(get_file_name).adf.empty
