from jproperties import Properties
from brcov_ssinha import dataconfig as cfg


def read_and_get_sort_columns() -> list:
    configs = Properties()
    try:
        with open(cfg.props_file, 'rb') as config_file:
            configs.load(config_file)
            aj_list = eval(configs.get('sort_cols').data)
            return aj_list
    except Exception as e:
        print('The properties file as specified in the config file could '
              'not be opened {}'.format(e))

        
def check_desired_format(x):
    if int(x) == x:
        return True
    else:
        raise Exception("Conversion Error")
        