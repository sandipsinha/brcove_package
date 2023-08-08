from os import path
# resources_dir = path.join(path.dirname(__file__), 'resources')
header_cols = ['date', 'accountid', 'metric', 'usage']
props_file = path.join(path.dirname(__file__), 'bcove_cfg_prop.py')
group_list = ['date', 'accountid', 'metric']
agg_dict = {'usage': ['sum']}