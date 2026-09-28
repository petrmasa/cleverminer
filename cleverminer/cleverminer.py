import sys
import time
import copy
import inspect
from time import strftime
from time import gmtime
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
import progressbar
import re
from textwrap import wrap
import seaborn as sns
import matplotlib.pyplot as plt
import re
import pickle
import json
import hashlib
from datetime import datetime
import tempfile
import os
import urllib

class cleverminer:
    version_string = '1.2.8'
    temppath = tempfile.gettempdir()
    cache_dir = os.path.join(temppath, 'clm_cache')

    def __init__(O00O0OO00OO, **OOOOOO0OOOO):
        """
        Starts CleverMiner procedure. Either only prepares data to binary form or both prepare data and execute enhanced association rule mining task.

        CleverMiner encapsulates several procedures - 4ft-Miner, CF-Miner, SD4ft-Miner and UIC-Miner.

        See https://cleverminer.org for details

        :param kwargs: list of keyword arguments.

        Keyword arguments inlude:
            * **df** - pandas dataframe (mandatory)
            * **proc** - procedure name (mandatory if task to be performed); one of the strings '4ftMiner','CFMiner','SD4ftMiner','UICMiner'
            * **target** - target variable for histogram mining procedures (CF-Miner, UIC-Miner) - for them parameter is mandatory
            * **opts** - options
            * **cedents** - definition of cedents.

            Each cedent has attributes and their types, minimal and maximal length. Attribute can be subset, sequence (seq), left or right cut (lcut, rcut) or one category (one) and for each, minimal and maximal number of categories are specified.

            ========== ========== ============ ============ ========== =============
            Procedure  Antecedent Succedent    Condition    First set  Second set
                       *ante*     *succ*       *cond*       *frst*     *scnd*
            ========== ========== ============ ============ ========== =============
            4ftMiner   Mandatory  Mandatory    Optional
            SD4ftMiner Mandatory  Mandatory    Optional     Mandatory  Mandatory
            CFMiner                            Mandatory
            UICMiner   Mandatory               Optional
            ========== ========== ============ ============ ========== =============

        """
        O00O0OO00OO._print_disclaimer()
        O00O0OO00OO.use_cache = False
        O00O0OO00OO.hidearray = None
        O00O0OO00OO.cache_also_data = True
        O00O0OO00OO.stats = {'total_cnt': 0, 'total_ver': 0, 'total_valid': 0, 'control_number': 0, 'start_prep_time': time.time(), 'end_prep_time': time.time(), 'start_proc_time': time.time(), 'end_proc_time': time.time()}
        O00O0OO00OO.options = {'max_categories': 100, 'max_rules': None, 'optimizations': True, 'automatic_data_conversions': True, 'progressbar': True, 'keep_df': False}
        O00O0OO00OO.df = None
        O00O0OO00OO.kwargs = None
        if len(OOOOOO0OOOO) > 0:
            O00O0OO00OO.kwargs = OOOOOO0OOOO
        O00O0OO00OO.profiles = {}
        O00O0OO00OO.verbosity = {}
        O00O0OO00OO.verbosity['debug'] = False
        O00O0OO00OO.verbosity['print_rules'] = False
        O00O0OO00OO.verbosity['print_hashes'] = True
        O00O0OO00OO.verbosity['last_hash_time'] = 0
        O00O0OO00OO.verbosity['hint'] = False
        if 'opts' in OOOOOO0OOOO:
            O00O0OO00OO._set_opts(OOOOOO0OOOO.get('opts'))
        if 'opts' in OOOOOO0OOOO:
            OOO00000O00O = OOOOOO0OOOO['opts']
            if 'use_cache' in OOO00000O00O:
                O00O0OO00OO.use_cache = OOO00000O00O['use_cache']
            if 'cache_also_data' in OOO00000O00O:
                O00O0OO00OO.cache_also_data = OOO00000O00O['cache_also_data']
            if 'verbose' in OOOOOO0OOOO.get('opts'):
                O00000O0OO00 = OOOOOO0OOOO.get('opts').get('verbose')
                if O00000O0OO00.upper() == 'FULL':
                    O00O0OO00OO.verbosity['debug'] = True
                    O00O0OO00OO.verbosity['print_rules'] = True
                    O00O0OO00OO.verbosity['print_hashes'] = False
                    O00O0OO00OO.verbosity['hint'] = True
                    O00O0OO00OO.options['progressbar'] = False
                elif O00000O0OO00.upper() == 'RULES':
                    O00O0OO00OO.verbosity['debug'] = False
                    O00O0OO00OO.verbosity['print_rules'] = True
                    O00O0OO00OO.verbosity['print_hashes'] = True
                    O00O0OO00OO.verbosity['hint'] = True
                    O00O0OO00OO.options['progressbar'] = False
                elif O00000O0OO00.upper() == 'HINT':
                    O00O0OO00OO.verbosity['debug'] = False
                    O00O0OO00OO.verbosity['print_rules'] = False
                    O00O0OO00OO.verbosity['print_hashes'] = True
                    O00O0OO00OO.verbosity['last_hash_time'] = 0
                    O00O0OO00OO.verbosity['hint'] = True
                    O00O0OO00OO.options['progressbar'] = False
                elif O00000O0OO00.upper() == 'DEBUG':
                    O00O0OO00OO.verbosity['debug'] = True
                    O00O0OO00OO.verbosity['print_rules'] = True
                    O00O0OO00OO.verbosity['print_hashes'] = True
                    O00O0OO00OO.verbosity['last_hash_time'] = 0
                    O00O0OO00OO.verbosity['hint'] = True
                    O00O0OO00OO.options['progressbar'] = False
        if 'load' in OOOOOO0OOOO:
            if O00O0OO00OO.use_cache:
                O00O0OO00OO.use_cache = False
        OOO000O0000 = copy.deepcopy(OOOOOO0OOOO)
        if 'df' in OOO000O0000:
            OOO000O0000['df'] = OOO000O0000['df'].to_json()
        OO0OO0O0O000 = O00O0OO00OO._get_hash(OOO000O0000)
        O00O0OO00OO.guid = OO0OO0O0O000
        if O00O0OO00OO.use_cache:
            if not os.path.isdir(O00O0OO00OO.cache_dir):
                os.mkdir(O00O0OO00OO.cache_dir)
            O00O0OO00OO.cache_fname = os.path.join(O00O0OO00OO.cache_dir, OO0OO0O0O000 + '.clm')
            if os.path.isfile(O00O0OO00OO.cache_fname):
                print(f'Will use cached file {O00O0OO00OO.cache_fname}')
                O0O0O0OO0O0O = 'pickle'
                if 'fmt' in OOOOOO0OOOO:
                    O0O0O0OO0O0O = OOOOOO0OOOO.get('fmt')
                O00O0OO00OO.load(O00O0OO00OO.cache_fname, fmt=O0O0O0OO0O0O)
                return
            print(f'Task {OO0OO0O0O000} not in cache, will calculate it.')
        O00O0OO00OO.O0OOOOO0OO0OO = sys.version_info[0] >= 4 or (sys.version_info[0] >= 3 and sys.version_info[1] >= 10)
        if not O00O0OO00OO.O0OOOOO0OO0OO:
            print('Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance')
        elif O00O0OO00OO.verbosity['debug']:
            print('Python 3.10+ detected.')
        O00O0OO00OO.OOOOOOO0OOOO0 = False
        if 'load' in OOOOOO0OOOO:
            O0O0O0OO0O0O = 'pickle'
            if 'fmt' in OOOOOO0OOOO:
                O0O0O0OO0O0O = OOOOOO0OOOO.get('fmt')
            O00O0OO00OO.load(filename=OOOOOO0OOOO.get('load'), fmt=O0O0O0OO0O0O)
            return
        O00O0OO00OO._init_data()
        O00O0OO00OO._init_task()
        if len(OOOOOO0OOOO) > 0:
            if 'df' in OOOOOO0OOOO:
                O00O0OO00OO._prep_data(OOOOOO0OOOO.get('df'))
            else:
                print('Missing dataframe. Cannot initialize.')
                O00O0OO00OO.OOOOOOO0OOOO0 = False
                return
            O0O00O0O00OO = OOOOOO0OOOO.get('proc', None)
            if not O0O00O0O00OO == None:
                O00O0OO00OO._calculate(**OOOOOO0OOOO)
            else:
                if O00O0OO00OO.verbosity['debug']:
                    print('INFO: just initialized')
                O0000O00O000O = {}
                O0OO0OO0OOO0 = {}
                O0OO0OO0OOO0['varname'] = O00O0OO00OO.data['varname']
                O0OO0OO0OOO0['catnames'] = O00O0OO00OO.data['catnames']
                O0000O00O000O['datalabels'] = O0OO0OO0OOO0
                O00O0OO00OO.result = O0000O00O000O
        O00O0OO00OO.OOOOOOO0OOOO0 = True
        if O00O0OO00OO.use_cache:
            O00O0OO00OO.save(O00O0OO00OO.cache_fname, savedata=O00O0OO00OO.cache_also_data, embeddata=False)
            print(f'CACHE: results cache saved into {O00O0OO00OO.cache_fname}')

    def _get_hash(O0OO0OO00OO, OOO00O0O0O0):

        class NpEncoder(json.JSONEncoder):

            def default(O0OO0OO00OO, OOO000O000):
                if isinstance(OOO000O000, np.integer):
                    return int(OOO000O000)
                if isinstance(OOO000O000, np.floating):
                    return float(OOO000O000)
                if isinstance(OOO000O000, np.ndarray):
                    return OOO000O000.tolist()
                if callable(OOO000O000):
                    return time.time()
                return super(NpEncoder, O0OO0OO00OO).default(OOO000O000)
        O00OOO00OO0O = hashlib.sha256(json.dumps(OOO00O0O0O0, sort_keys=True, cls=NpEncoder).encode('utf-8')).hexdigest()
        return O00OOO00OO0O

    def _get_fast_hash(OOOOO0O000, O000O0O00OOO):
        O00O0OO000OO = pickle.dumps(O000O0O00OOO)
        print(f'...CALC THE HASH {datetime.now()}')
        OOO0OO000OO0O = hashlib.md5(O00O0OO000OO).hexdigest()
        return OOO0OO000OO0O

    def _set_opts(O00O0000000, OO0000O0OO0O):
        if 'no_optimizations' in OO0000O0OO0O:
            O00O0000000.options['optimizations'] = not OO0000O0OO0O['no_optimizations']
            print('No optimization will be made.')
        if 'disable_progressbar' in OO0000O0OO0O:
            O00O0000000.options['progressbar'] = False
            print('Progressbar will not be shown.')
        if 'max_rules' in OO0000O0OO0O:
            O00O0000000.options['max_rules'] = OO0000O0OO0O['max_rules']
        if 'max_categories' in OO0000O0OO0O:
            O00O0000000.options['max_categories'] = OO0000O0OO0O['max_categories']
            if O00O0000000.verbosity['debug'] == True:
                print(f"Maximum number of categories set to {O00O0000000.options['max_categories']}")
        if 'no_automatic_data_conversions' in OO0000O0OO0O:
            O00O0000000.options['automatic_data_conversions'] = not OO0000O0OO0O['no_automatic_data_conversions']
            print('No automatic data conversions will be made.')
        if 'keep_df' in OO0000O0OO0O:
            O00O0000000.options['keep_df'] = OO0000O0OO0O['keep_df']

    def _init_data(O0OO00OO0O):
        O0OO00OO0O.data = {}
        O0OO00OO0O.data['varname'] = []
        O0OO00OO0O.data['catnames'] = []
        O0OO00OO0O.data['vtypes'] = []
        O0OO00OO0O.data['dm'] = []
        O0OO00OO0O.data['rows_count'] = int(0)
        O0OO00OO0O.data['data_prepared'] = 0

    def _init_task(OO0OOO0000):
        if 'opts' in OO0OOO0000.kwargs:
            OO0OOO0000._set_opts(OO0OOO0000.kwargs.get('opts'))
        OO0OOO0000.cedent = {'cedent_type': 'none', 'defi': {}, 'num_cedent': 0, 'trace_cedent': [], 'trace_cedent_asindata': [], 'traces': [], 'generated_string': '', 'rule': {}, 'filter_value': int(0)}
        OO0OOO0000.task_actinfo = {'proc': '', 'cedents_to_do': [], 'cedents': []}
        OO0OOO0000.rulelist = []
        OO0OOO0000.stats['total_cnt'] = 0
        OO0OOO0000.stats['total_valid'] = 0
        OO0OOO0000.stats['control_number'] = 0
        OO0OOO0000.result = {}
        OO0OOO0000.O0O0000OO0 = None
        OO0OOO0000.OOO0O0O0O000 = None
        OO0OOO0000.OOO0O00OOO = None
        OO0OOO0000.O00O0O0000OO = None
        OO0OOO0000.OOOOOO0OO00O0 = None
        OO0OOO0000.O0OO000O0OO0O = None
        OO0OOOO0O00O0 = None
        if not OO0OOO0000.kwargs == None:
            OO0OOOO0O00O0 = OO0OOO0000.kwargs.get('quantifiers', None)
            if not OO0OOOO0O00O0 == None:
                for O00000O000 in OO0OOOO0O00O0.keys():
                    if O00000O000.upper() == 'BASE':
                        OO0OOO0000.O0O0000OO0 = OO0OOOO0O00O0.get(O00000O000)
                    if O00000O000.upper() == 'RELBASE':
                        OO0OOO0000.OOO0O0O0O000 = OO0OOOO0O00O0.get(O00000O000)
                    if (O00000O000.upper() == 'FRSTBASE') | (O00000O000.upper() == 'BASE1'):
                        OO0OOO0000.OOO0O00OOO = OO0OOOO0O00O0.get(O00000O000)
                    if (O00000O000.upper() == 'SCNDBASE') | (O00000O000.upper() == 'BASE2'):
                        OO0OOO0000.OOOOOO0OO00O0 = OO0OOOO0O00O0.get(O00000O000)
                    if (O00000O000.upper() == 'FRSTRELBASE') | (O00000O000.upper() == 'RELBASE1'):
                        OO0OOO0000.O00O0O0000OO = OO0OOOO0O00O0.get(O00000O000)
                    if (O00000O000.upper() == 'SCNDRELBASE') | (O00000O000.upper() == 'RELBASE2'):
                        OO0OOO0000.O0OO000O0OO0O = OO0OOOO0O00O0.get(O00000O000)
            else:
                print('Warning: no quantifiers found. Optimization will not take place (1)')
        else:
            print('Warning: no quantifiers found. Optimization will not take place (2)')

    def mine(O0OOO0O00O0, **O0O00O000OOO):
        """
        Runs a mining task on a prepared data set.
        :param kwargs: list of keyword arguments. List is the same as for mining task with default constructor.
        :return: a dictionary with task summary, task processing statistics, ruleset and variable information.
        """
        if not O0OOO0O00O0.OOOOOOO0OOOO0:
            print('Class NOT INITIALIZED. Please call constructor with dataframe first')
            return
        O0OOO0O00O0.kwargs = None
        O0OOO0O00O0.hidearray = None
        if len(O0O00O000OOO) > 0:
            O0OOO0O00O0.kwargs = O0O00O000OOO
        O0OOO0O00O0._init_task()
        if len(O0O00O000OOO) > 0:
            O000000000O0O = O0O00O000OOO.get('proc', None)
            if not O000000000O0O == None:
                O0OOO0O00O0._calc_all(**O0O00O000OOO)
            else:
                print('Rule mining procedure missing')

    def _get_ver(OOOO000O00):
        return OOOO000O00.version_string

    def _print_disclaimer(OO0OOOO00OO0O):
        print(f'Cleverminer version {OO0OOOO00OO0O._get_ver()}.')

    def _automatic_data_conversions(O00O00OOOO0O, OO0O0O0OOOO):
        print('Automatically reordering numeric categories ...')
        for OO00OO00O0OOO in range(len(OO0O0O0OOOO.columns)):
            if O00O00OOOO0O.verbosity['debug']:
                print(f'#{OO00OO00O0OOO}: {OO0O0O0OOOO.columns[OO00OO00O0OOO]} : {OO0O0O0OOOO.dtypes[OO00OO00O0OOO]}.')
            try:
                OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]] = OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]].astype(str).astype(float)
                if O00O00OOOO0O.verbosity['debug']:
                    print(f'CONVERTED TO FLOATS #{OO00OO00O0OOO}: {OO0O0O0OOOO.columns[OO00OO00O0OOO]} : {OO0O0O0OOOO.dtypes[OO00OO00O0OOO]}.')
                OOO00O0O000 = pd.unique(OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]])
                OO00O0OO0O = True
                for OO00000OOOO in OOO00O0O000:
                    if OO00000OOOO % 1 != 0:
                        OO00O0OO0O = False
                if OO00O0OO0O:
                    OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]] = OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]].astype(int)
                    if O00O00OOOO0O.verbosity['debug']:
                        print(f'CONVERTED TO INT #{OO00OO00O0OOO}: {OO0O0O0OOOO.columns[OO00OO00O0OOO]} : {OO0O0O0OOOO.dtypes[OO00OO00O0OOO]}.')
                OO00O00O0O = pd.unique(OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]])
                O0O00000OO0O0 = CategoricalDtype(categories=OO00O00O0O.sort(), ordered=True)
                OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]] = OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]].astype(O0O00000OO0O0)
                if O00O00OOOO0O.verbosity['debug']:
                    print(f'CONVERTED TO CATEGORY #{OO00OO00O0OOO}: {OO0O0O0OOOO.columns[OO00OO00O0OOO]} : {OO0O0O0OOOO.dtypes[OO00OO00O0OOO]}.')
            except:
                if O00O00OOOO0O.verbosity['debug']:
                    print('...cannot be converted to int')
                try:
                    O0OOO0OO00O00 = OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]].unique()
                    if O00O00OOOO0O.verbosity['debug']:
                        print(f'Values: {O0OOO0OO00O00}')
                    OO00O0O00O00 = True
                    O0O0OOOO00OO = []
                    for OO00000OOOO in O0OOO0OO00O00:
                        O0O0OOO0OO = re.findall('-?\\d+', OO00000OOOO)
                        if len(O0O0OOO0OO) > 0:
                            O0O0OOOO00OO.append(int(O0O0OOO0OO[0]))
                        else:
                            OO00O0O00O00 = False
                    if O00O00OOOO0O.verbosity['debug']:
                        print(f'Is ok: {OO00O0O00O00}, extracted {O0O0OOOO00OO}')
                    if OO00O0O00O00:
                        O0000O000OO0O = copy.deepcopy(O0O0OOOO00OO)
                        O0000O000OO0O.sort()
                        OOO000O00O = []
                        for OOO0O0OO000O in O0000O000OO0O:
                            OOOO0OO0O0O0 = O0O0OOOO00OO.index(OOO0O0OO000O)
                            OOO000O00O.append(O0OOO0OO00O00[OOOO0OO0O0O0])
                        if O00O00OOOO0O.verbosity['debug']:
                            print(f'Sorted list: {OOO000O00O}')
                        O0O00000OO0O0 = CategoricalDtype(categories=OOO000O00O, ordered=True)
                        OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]] = OO0O0O0OOOO[OO0O0O0OOOO.columns[OO00OO00O0OOO]].astype(O0O00000OO0O0)
                except:
                    if O00O00OOOO0O.verbosity['debug']:
                        print('...cannot extract numbers from all categories')
        print('Automatically reordering numeric categories ...done')

    def _prep_data(OOOO000OOO, OOO0O0O0OOO00):
        print('Starting data preparation ...')
        OOOO000OOO._init_data()
        OOOO000OOO.stats['start_prep_time'] = time.time()
        if OOOO000OOO.options['automatic_data_conversions']:
            OOOO000OOO._automatic_data_conversions(OOO0O0O0OOO00)
        OOOO000OOO.data['rows_count'] = OOO0O0O0OOO00.shape[0]
        for OOO0O00000 in OOO0O0O0OOO00.select_dtypes(exclude=['category']).columns:
            OOO0O0O0OOO00[OOO0O00000] = OOO0O0O0OOO00[OOO0O00000].apply(str)
        try:
            OO0O0O00OO00 = pd.DataFrame.from_records([(OOO0O00000, OOO0O0O0OOO00[OOO0O00000].nunique()) for OOO0O00000 in OOO0O0O0OOO00.columns], columns=['Column_Name', 'Num_Unique']).sort_values(by=['Num_Unique'])
        except:
            print('Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.')
            OOO00000O000O = ''
            try:
                for OOO0O00000 in OOO0O0O0OOO00.columns:
                    OOO00000O000O = OOO0O00000
                    print(f'...column {OOO0O00000} has {int(OOO0O0O0OOO00[OOO0O00000].nunique())} values')
            except:
                print(f'... detected : column {OOO00000O000O} has unsupported type: {type(OOO0O0O0OOO00[OOO0O00000])}.')
                exit(1)
            print(f'Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.')
            exit(1)
        if OOOO000OOO.verbosity['hint']:
            print('Quick profile of input data: unique value counts are:')
            print(OO0O0O00OO00)
            for OOO0O00000 in OOO0O0O0OOO00.columns:
                if OOO0O0O0OOO00[OOO0O00000].nunique() < OOOO000OOO.options['max_categories']:
                    OOO0O0O0OOO00[OOO0O00000] = OOO0O0O0OOO00[OOO0O00000].astype('category')
                else:
                    print(f"WARNING: attribute {OOO0O00000} has more than {OOOO000OOO.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")
                    del OOO0O0O0OOO00[OOO0O00000]
        for OOO0O00000 in OOO0O0O0OOO00.columns:
            if OOO0O0O0OOO00[OOO0O00000].nunique() > OOOO000OOO.options['max_categories']:
                print(f"WARNING: attribute {OOO0O00000} has more than {OOOO000OOO.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")
                del OOO0O0O0OOO00[OOO0O00000]
        if OOOO000OOO.options['keep_df']:
            if OOOO000OOO.verbosity['debug']:
                print('Keeping df.')
            OOOO000OOO.df = OOO0O0O0OOO00
        print('Encoding columns into bit-form...')
        O0000000OO0 = 0
        O0000O000OOO = 0
        for O0O00000OO0 in OOO0O0O0OOO00:
            if OOOO000OOO.verbosity['debug']:
                print('Column: ' + O0O00000OO0 + ' @ ' + str(time.time()))
            if OOOO000OOO.verbosity['debug']:
                print('Column: ' + O0O00000OO0)
            OOOO000OOO.data['varname'].append(O0O00000OO0)
            OO00OO00OOOO = pd.get_dummies(OOO0O0O0OOO00[O0O00000OO0])
            OO0OOOO0OO0 = 0
            if OOO0O0O0OOO00.dtypes[O0O00000OO0].name == 'category':
                OO0OOOO0OO0 = 1
            OOOO000OOO.data['vtypes'].append(OO0OOOO0OO0)
            if OOOO000OOO.verbosity['debug']:
                print(OO00OO00OOOO)
                print(OOO0O0O0OOO00[O0O00000OO0])
            OOO0000O0O00 = 0
            OO0OO0O000O0 = []
            OOOO00OOOO = []
            if OOOO000OOO.verbosity['debug']:
                print('...starting categories ' + str(time.time()))
            for O00O00O0O0000 in OO00OO00OOOO:
                if OOOO000OOO.verbosity['debug']:
                    print('....category : ' + str(O00O00O0O0000) + ' @ ' + str(time.time()))
                OO0OO0O000O0.append(O00O00O0O0000)
                O00OOO0O00 = int(0)
                O0000O00OOO0 = OO00OO00OOOO[O00O00O0O0000].values
                if OOOO000OOO.verbosity['debug']:
                    print(O0000O00OOO0.ndim)
                O0O000O0O0 = np.packbits(O0000O00OOO0, bitorder='little')
                O00OOO0O00 = int.from_bytes(O0O000O0O0, byteorder='little')
                OOOO00OOOO.append(O00OOO0O00)
                if OOOO000OOO.verbosity['debug']:
                    for OO000000OO in range(OOOO000OOO.data['rows_count']):
                        if O0000O00OOO0[OO000000OO] > 0:
                            O00OOO0O00 += 1 << OO000000OO
                            OOOO00OOOO.append(O00OOO0O00)
                    print('....category ATTEMPT 2: ' + str(O00O00O0O0000) + ' @ ' + str(time.time()))
                    O000000O0O0 = int(0)
                    OOO00O00OO = int(1)
                    for OO000000OO in range(OOOO000OOO.data['rows_count']):
                        if O0000O00OOO0[OO000000OO] > 0:
                            O000000O0O0 += OOO00O00OO
                            OOO00O00OO *= 2
                            OOO00O00OO = OOO00O00OO << 1
                            print(str(O00OOO0O00 == O000000O0O0) + ' @ ' + str(time.time()))
                OOO0000O0O00 += 1
                O0000O000OOO += 1
                if OOOO000OOO.verbosity['debug']:
                    print(OO0OO0O000O0)
            OOOO000OOO.data['catnames'].append(OO0OO0O000O0)
            OOOO000OOO.data['dm'].append(OOOO00OOOO)
        print('Encoding columns into bit-form...done')
        if OOOO000OOO.verbosity['hint']:
            print(f"List of attributes for analysis is: {OOOO000OOO.data['varname']}")
            print(f"List of category names for individual attributes is : {OOOO000OOO.data['catnames']}")
        if OOOO000OOO.verbosity['debug']:
            print(f"List of vtypes is (all should be 1) : {OOOO000OOO.data['vtypes']}")
        OOOO000OOO.data['data_prepared'] = 1
        print('Data preparation finished.')
        if OOOO000OOO.verbosity['debug']:
            print('Number of variables : ' + str(len(OOOO000OOO.data['dm'])))
            print('Total number of categories in all variables : ' + str(O0000O000OOO))
        OOOO000OOO.stats['end_prep_time'] = time.time()
        if OOOO000OOO.verbosity['debug']:
            print('Time needed for data preparation : ', str(OOOO000OOO.stats['end_prep_time'] - OOOO000OOO.stats['start_prep_time']))

    def _bitcount(O000O00000OO, OOOOO0OOOO0OO):
        O0O00OO000O00 = None
        if O000O00000OO.O0OOOOO0OO0OO:
            O0O00OO000O00 = OOOOO0OOOO0OO.bit_count()
        else:
            O0O00OO000O00 = bin(OOOOO0OOOO0OO).count('1')
        return O0O00OO000O00

    def _verifyCF(OO0O0O000O0, OO000000OO0):
        OO0O0OOOO00 = OO0O0O000O0._bitcount(OO000000OO0)
        OO0OO0000OOOO = []
        O0OOOOOOO00 = []
        O00O0O00000 = 0
        O00O0OOOO0 = 0
        OOO0O0OO0O0O0 = 0
        OOO00O0O0O00O = 0
        OO0OOOOO00OO0 = 0
        O0OO0O0000000 = 0
        OOO000OO0000 = 0
        O00OO00O00 = 0
        O000OOO00000O = 0
        OOOOOO0000 = None
        OO0O0OOOOO00O = None
        O00O00O00O = None
        if 'min_step_size' in OO0O0O000O0.quantifiers:
            OOOOOO0000 = OO0O0O000O0.quantifiers.get('min_step_size')
        if 'min_rel_step_size' in OO0O0O000O0.quantifiers:
            OO0O0OOOOO00O = OO0O0O000O0.quantifiers.get('min_rel_step_size')
            if OO0O0OOOOO00O >= 1 and OO0O0OOOOO00O < 100:
                OO0O0OOOOO00O = OO0O0OOOOO00O / 100
        O00OO00OOOO = 0
        OO0OO0000O0O = 0
        OOOO0O00O00OO = []
        if 'aad_weights' in OO0O0O000O0.quantifiers:
            O00OO00OOOO = 1
            O000O0O0000O = []
            OOOO0O00O00OO = OO0O0O000O0.quantifiers.get('aad_weights')
        OOO0000OOO0 = OO0O0O000O0.data['dm'][OO0O0O000O0.data['varname'].index(OO0O0O000O0.kwargs.get('target'))]

        def eval_step_size(O00O0O00000, O00O0OOOO0):
            O0O000O0OO0O = True
            if O00O0O00000 > O00O0OOOO0:
                if not (OOOOOO0000 is None or O00O0O00000 >= O00O0OOOO0 + OOOOOO0000):
                    O0O000O0OO0O = False
                if not (OO0O0OOOOO00O is None or O00O0O00000 >= O00O0OOOO0 * (1 + OO0O0OOOOO00O)):
                    O0O000O0OO0O = False
            if O00O0O00000 < O00O0OOOO0:
                if not (OOOOOO0000 is None or O00O0O00000 <= O00O0OOOO0 - OOOOOO0000):
                    O0O000O0OO0O = False
                if not (OO0O0OOOOO00O is None or O00O0O00000 <= O00O0OOOO0 * (1 - OO0O0OOOOO00O)):
                    O0O000O0OO0O = False
            return O0O000O0OO0O
        for O00OOO00000 in range(len(OOO0000OOO0)):
            O00O0OOOO0 = O00O0O00000
            O00O0O00000 = OO0O0O000O0._bitcount(OO000000OO0 & OOO0000OOO0[O00OOO00000])
            OO0OO0000OOOO.append(O00O0O00000)
            if O00OOO00000 > 0:
                if O00O0O00000 > O00O0OOOO0:
                    if OOO0O0OO0O0O0 == 1 and eval_step_size(O00O0O00000, O00O0OOOO0):
                        O00OO00O00 += 1
                    elif eval_step_size(O00O0O00000, O00O0OOOO0):
                        O00OO00O00 = 1
                    else:
                        O00OO00O00 = 0
                    if O00OO00O00 > OOO00O0O0O00O:
                        OOO00O0O0O00O = O00OO00O00
                    OOO0O0OO0O0O0 = 1
                    if eval_step_size(O00O0O00000, O00O0OOOO0):
                        O0OO0O0000000 += 1
                if O00O0O00000 < O00O0OOOO0:
                    if OOO0O0OO0O0O0 == -1 and eval_step_size(O00O0O00000, O00O0OOOO0):
                        O000OOO00000O += 1
                    elif eval_step_size(O00O0O00000, O00O0OOOO0):
                        O000OOO00000O = 1
                    else:
                        O000OOO00000O = 0
                    if O000OOO00000O > OO0OOOOO00OO0:
                        OO0OOOOO00OO0 = O000OOO00000O
                    OOO0O0OO0O0O0 = -1
                    if eval_step_size(O00O0O00000, O00O0OOOO0):
                        OOO000OO0000 += 1
                if O00O0O00000 == O00O0OOOO0:
                    OOO0O0OO0O0O0 = 0
                    O000OOO00000O = 0
                    O00OO00O00 = 0
            if O00OO00OOOO:
                O0OO0O0000 = OO0O0O000O0._bitcount(OOO0000OOO0[O00OOO00000])
                O000O0O0000O.append(O0OO0O0000)
        if O00OO00OOOO & sum(OO0OO0000OOOO) > 0:
            for O00OOO00000 in range(len(OOO0000OOO0)):
                if O000O0O0000O[O00OOO00000] > 0:
                    if OO0OO0000OOOO[O00OOO00000] / sum(OO0OO0000OOOO) > O000O0O0000O[O00OOO00000] / sum(O000O0O0000O):
                        OO0OO0000O0O += OOOO0O00O00OO[O00OOO00000] * (OO0OO0000OOOO[O00OOO00000] / sum(OO0OO0000OOOO) / (O000O0O0000O[O00OOO00000] / sum(O000O0O0000O)) - 1)
        O0O000O0OO0O = True
        for OOO00000O0 in OO0O0O000O0.quantifiers.keys():
            if OOO00000O0.upper() == 'BASE':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OO0O0OOOO00
            if OOO00000O0.upper() == 'RELBASE':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OO0O0OOOO00 * 1.0 / OO0O0O000O0.data['rows_count']
            if OOO00000O0.upper() == 'S_UP':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OOO00O0O0O00O
            if OOO00000O0.upper() == 'S_DOWN':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OO0OOOOO00OO0
            if OOO00000O0.upper() == 'S_ANY_UP':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OOO00O0O0O00O
            if OOO00000O0.upper() == 'S_ANY_DOWN':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OO0OOOOO00OO0
            if OOO00000O0.upper() == 'MAX':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= max(OO0OO0000OOOO)
            if OOO00000O0.upper() == 'MIN':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= min(OO0OO0000OOOO)
            if OOO00000O0.upper() == 'RELMAX':
                if sum(OO0OO0000OOOO) > 0:
                    O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= max(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                else:
                    O0O000O0OO0O = False
            if OOO00000O0.upper() == 'RELMAX_LEQ':
                if sum(OO0OO0000OOOO) > 0:
                    O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) >= max(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                else:
                    O0O000O0OO0O = False
            if OOO00000O0.upper() == 'RELMIN':
                if sum(OO0OO0000OOOO) > 0:
                    O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= min(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                else:
                    O0O000O0OO0O = False
            if OOO00000O0.upper() == 'RELMIN_LEQ':
                if sum(OO0OO0000OOOO) > 0:
                    O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) >= min(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                else:
                    O0O000O0OO0O = False
            if OOO00000O0.upper() == 'AAD':
                O0O000O0OO0O = O0O000O0OO0O and OO0O0O000O0.quantifiers.get(OOO00000O0) <= OO0OO0000O0O
            if OOO00000O0.upper() == 'RELRANGE_LEQ':
                O00O0O000OOO0 = OO0O0O000O0.quantifiers.get(OOO00000O0)
                if O00O0O000OOO0 >= 1 and O00O0O000OOO0 < 100:
                    O00O0O000OOO0 = O00O0O000OOO0 * 1.0 / 100
                O0000O000O0 = min(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                O0OO00O000OO = max(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                O0O000O0OO0O = O0O000O0OO0O and O00O0O000OOO0 >= O0OO00O000OO - O0000O000O0
        O0000OOOOO = {}
        if O0O000O0OO0O == True:
            if OO0O0O000O0.verbosity['debug']:
                print('Rule found: base: ' + str(OO0O0OOOO00) + ', hist: ' + str(OO0OO0000OOOO) + ', max: ' + str(max(OO0OO0000OOOO)) + ', min: ' + str(min(OO0OO0000OOOO)) + ', s_up: ' + str(OOO00O0O0O00O) + ', s_down: ' + str(OO0OOOOO00OO0))
            OO0O0O000O0.stats['total_valid'] += 1
            O0000OOOOO['base'] = OO0O0OOOO00
            O0000OOOOO['rel_base'] = OO0O0OOOO00 * 1.0 / OO0O0O000O0.data['rows_count']
            O0000OOOOO['s_up'] = OOO00O0O0O00O
            O0000OOOOO['s_down'] = OO0OOOOO00OO0
            O0000OOOOO['s_any_up'] = O0OO0O0000000
            O0000OOOOO['s_any_down'] = OOO000OO0000
            O0000OOOOO['max'] = max(OO0OO0000OOOO)
            O0000OOOOO['min'] = min(OO0OO0000OOOO)
            if OO0O0O000O0.verbosity['debug']:
                O0000OOOOO['rel_max'] = max(OO0OO0000OOOO) * 1.0 / OO0O0O000O0.data['rows_count']
                O0000OOOOO['rel_min'] = min(OO0OO0000OOOO) * 1.0 / OO0O0O000O0.data['rows_count']
            if sum(OO0OO0000OOOO) > 0:
                O0000OOOOO['rel_max'] = max(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
                O0000OOOOO['rel_min'] = min(OO0OO0000OOOO) * 1.0 / sum(OO0OO0000OOOO)
            else:
                O0000OOOOO['rel_max'] = 0
                O0000OOOOO['rel_min'] = 0
            O0000OOOOO['hist'] = OO0OO0000OOOO
            if O00OO00OOOO:
                O0000OOOOO['aad'] = OO0OO0000O0O
                O0000OOOOO['hist_full'] = O000O0O0000O
                O0000OOOOO['rel_hist'] = [O0OOOOOOO000 / sum(OO0OO0000OOOO) for O0OOOOOOO000 in OO0OO0000OOOO]
                O0000OOOOO['rel_hist_full'] = [O0OOOOOOO000 / sum(O000O0O0000O) for O0OOOOOOO000 in O000O0O0000O]
        if OO0O0O000O0.verbosity['debug']:
            print('Info: base: ' + str(OO0O0OOOO00) + ', hist: ' + str(OO0OO0000OOOO) + ', max: ' + str(max(OO0OO0000OOOO)) + ', min: ' + str(min(OO0OO0000OOOO)) + ', s_up: ' + str(OOO00O0O0O00O) + ', s_down: ' + str(OO0OOOOO00OO0))
        return (O0O000O0OO0O, O0000OOOOO)

    def _verifyUIC(OO0O0000OOO, OOOOO0000OO0):
        OOO0000000OO = {}
        O0000000OO = 0
        for O0OOO00OOOOO in OO0O0000OOO.task_actinfo['cedents']:
            OOO0000000OO[O0OOO00OOOOO['cedent_type']] = O0OOO00OOOOO['filter_value']
            O0000000OO = O0000000OO + 1
        if OO0O0000OOO.verbosity['debug']:
            print(O0OOO00OOOOO['cedent_type'] + ' : ' + str(O0OOO00OOOOO['filter_value']))
        OO00OO00OOOO0 = OO0O0000OOO._bitcount(OOOOO0000OO0)
        O00O00O0OOO0 = []
        OO00O0000OOO = 0
        O0OO0OO00000 = 0
        OOO0000O0O0 = 0
        O0000O00OO00 = []
        O00OO0O0O0O = []
        if 'aad_weights' in OO0O0000OOO.quantifiers:
            O0000O00OO00 = OO0O0000OOO.quantifiers.get('aad_weights')
            O0OO0OO00000 = 1
        O00OO000OO = OO0O0000OOO.data['dm'][OO0O0000OOO.data['varname'].index(OO0O0000OOO.kwargs.get('target'))]
        for OOOO000O0OOO in range(len(O00OO000OO)):
            OO000OOOOOO00 = OO00O0000OOO
            OO00O0000OOO = OO0O0000OOO._bitcount(OOOOO0000OO0 & O00OO000OO[OOOO000O0OOO])
            O00O00O0OOO0.append(OO00O0000OOO)
            OO0O00000O = OO0O0000OOO._bitcount(OOO0000000OO['cond'] & O00OO000OO[OOOO000O0OOO])
            O00OO0O0O0O.append(OO0O00000O)
        OO0O0O0O0OOO0 = 0
        OOOO00OO0OOO = 0
        if O0OO0OO00000 & sum(O00O00O0OOO0) > 0:
            for OOOO000O0OOO in range(len(O00OO000OO)):
                if O00OO0O0O0O[OOOO000O0OOO] > 0:
                    if O00O00O0OOO0[OOOO000O0OOO] / sum(O00O00O0OOO0) > O00OO0O0O0O[OOOO000O0OOO] / sum(O00OO0O0O0O):
                        OOO0000O0O0 += O0000O00OO00[OOOO000O0OOO] * (O00O00O0OOO0[OOOO000O0OOO] / sum(O00O00O0OOO0) / (O00OO0O0O0O[OOOO000O0OOO] / sum(O00OO0O0O0O)) - 1)
                if O0000O00OO00[OOOO000O0OOO] > 0:
                    OO0O0O0O0OOO0 += O00O00O0OOO0[OOOO000O0OOO]
                    OOOO00OO0OOO += O00OO0O0O0O[OOOO000O0OOO]
        O000OOOO000 = 0
        if sum(O00O00O0OOO0) > 0 and OOOO00OO0OOO > 0:
            O000OOOO000 = OO0O0O0O0OOO0 / sum(O00O00O0OOO0) / (OOOO00OO0OOO / sum(O00OO0O0O0O))
        OOOO00O0OO0OO = True
        for OOO00OOO00 in OO0O0000OOO.quantifiers.keys():
            if OOO00OOO00.upper() == 'BASE':
                OOOO00O0OO0OO = OOOO00O0OO0OO and OO0O0000OOO.quantifiers.get(OOO00OOO00) <= OO00OO00OOOO0
            if OOO00OOO00.upper() == 'RELBASE':
                OOOO00O0OO0OO = OOOO00O0OO0OO and OO0O0000OOO.quantifiers.get(OOO00OOO00) <= OO00OO00OOOO0 * 1.0 / OO0O0000OOO.data['rows_count']
            if OOO00OOO00.upper() == 'AAD_SCORE':
                OOOO00O0OO0OO = OOOO00O0OO0OO and OO0O0000OOO.quantifiers.get(OOO00OOO00) <= OOO0000O0O0
            if OOO00OOO00.upper() == 'RELEVANT_CAT_BASE':
                OOOO00O0OO0OO = OOOO00O0OO0OO and OO0O0000OOO.quantifiers.get(OOO00OOO00) <= OO0O0O0O0OOO0
            if OOO00OOO00.upper() == 'RELEVANT_BASE_LIFT':
                OOOO00O0OO0OO = OOOO00O0OO0OO and OO0O0000OOO.quantifiers.get(OOO00OOO00) <= O000OOOO000
        OO000OOO0000O = {}
        if OOOO00O0OO0OO == True:
            OO0O0000OOO.stats['total_valid'] += 1
            OO000OOO0000O['base'] = OO00OO00OOOO0
            OO000OOO0000O['rel_base'] = OO00OO00OOOO0 * 1.0 / OO0O0000OOO.data['rows_count']
            OO000OOO0000O['hist'] = O00O00O0OOO0
            OO000OOO0000O['aad_score'] = OOO0000O0O0
            OO000OOO0000O['hist_cond'] = O00OO0O0O0O
            OO000OOO0000O['rel_hist'] = [O0O0OOOO0O / sum(O00O00O0OOO0) for O0O0OOOO0O in O00O00O0OOO0]
            OO000OOO0000O['rel_hist_cond'] = [O0O0OOOO0O / sum(O00OO0O0O0O) for O0O0OOOO0O in O00OO0O0O0O]
            OO000OOO0000O['relevant_base_lift'] = O000OOOO000
            OO000OOO0000O['relevant_cat_base'] = OO0O0O0O0OOO0
            OO000OOO0000O['relevant_cat_base_full'] = OOOO00OO0OOO
        return (OOOO00O0OO0OO, OO000OOO0000O)

    def _verify4ft(O00OOOOOO00O, O00OO0O000OO, O0OO0O0OOO0O=None, O0O0O0O0OO00=None):
        OOO0O0OOOO0 = {}
        OO00OOOOOO0O0 = 0
        for OO000O00OO000 in O00OOOOOO00O.task_actinfo['cedents']:
            OOO0O0OOOO0[OO000O00OO000['cedent_type']] = OO000O00OO000['filter_value']
            OO00OOOOOO0O0 = OO00OOOOOO0O0 + 1
        OO0OO0OOOOO = O00OOOOOO00O._bitcount(OOO0O0OOOO0['ante'] & OOO0O0OOOO0['succ'] & OOO0O0OOOO0['cond'])
        OO0O00OOOO = None
        OO0O00OOOO = 0
        if OO0OO0OOOOO > 0:
            OO0O00OOOO = O00OOOOOO00O._bitcount(OOO0O0OOOO0['ante'] & OOO0O0OOOO0['succ'] & OOO0O0OOOO0['cond']) * 1.0 / O00OOOOOO00O._bitcount(OOO0O0OOOO0['ante'] & OOO0O0OOOO0['cond'])
        O0OO0O0OO0 = 1 << O00OOOOOO00O.data['rows_count']
        OOO00000OO0 = O00OOOOOO00O._bitcount(OOO0O0OOOO0['ante'] & OOO0O0OOOO0['succ'] & OOO0O0OOOO0['cond'])
        OO0O0OOOO0 = O00OOOOOO00O._bitcount(OOO0O0OOOO0['ante'] & ~(O0OO0O0OO0 | OOO0O0OOOO0['succ']) & OOO0O0OOOO0['cond'])
        OO000O00OO000 = O00OOOOOO00O._bitcount(~(O0OO0O0OO0 | OOO0O0OOOO0['ante']) & OOO0O0OOOO0['succ'] & OOO0O0OOOO0['cond'])
        OO00O0O00000 = O00OOOOOO00O._bitcount(~(O0OO0O0OO0 | OOO0O0OOOO0['ante']) & ~(O0OO0O0OO0 | OOO0O0OOOO0['succ']) & OOO0O0OOOO0['cond'])
        OO0OO0O000 = 0
        O0OO0O0O000 = 0
        if (OOO00000OO0 + OO0O0OOOO0) * (OOO00000OO0 + OO000O00OO000) > 0:
            OO0OO0O000 = OOO00000OO0 * (OOO00000OO0 + OO0O0OOOO0 + OO000O00OO000 + OO00O0O00000) / (OOO00000OO0 + OO0O0OOOO0) / (OOO00000OO0 + OO000O00OO000) - 1
            O0OO0O0O000 = OO0OO0O000 + 1
        else:
            OO0OO0O000 = None
            O0OO0O0O000 = None
        OO00OOO0O0 = 0
        if (OOO00000OO0 + OO0O0OOOO0) * (OOO00000OO0 + OO000O00OO000) > 0:
            OO00OOO0O0 = 1 - OOO00000OO0 * (OOO00000OO0 + OO0O0OOOO0 + OO000O00OO000 + OO00O0O00000) / (OOO00000OO0 + OO0O0OOOO0) / (OOO00000OO0 + OO000O00OO000)
        else:
            OO00OOO0O0 = None
        O00OOOOO00O = True
        for O0O0OO0OOO in O00OOOOOO00O.quantifiers.keys():
            if O0O0OO0OOO.upper() == 'BASE':
                O00OOOOO00O = O00OOOOO00O and O00OOOOOO00O.quantifiers.get(O0O0OO0OOO) <= OO0OO0OOOOO
            if O0O0OO0OOO.upper() == 'RELBASE':
                O00OOOOO00O = O00OOOOO00O and O00OOOOOO00O.quantifiers.get(O0O0OO0OOO) <= OO0OO0OOOOO * 1.0 / O00OOOOOO00O.data['rows_count']
            if O0O0OO0OOO.upper() == 'PIM' or O0O0OO0OOO.upper() == 'CONF':
                O00OOOOO00O = O00OOOOO00O and O00OOOOOO00O.quantifiers.get(O0O0OO0OOO) <= OO0O00OOOO
            if O0O0OO0OOO.upper() == 'AAD':
                if OO0OO0O000 != None:
                    O00OOOOO00O = O00OOOOO00O and O00OOOOOO00O.quantifiers.get(O0O0OO0OOO) <= OO0OO0O000
                else:
                    O00OOOOO00O = False
            if O0O0OO0OOO.upper() == 'BAD':
                if OO00OOO0O0 != None:
                    O00OOOOO00O = O00OOOOO00O and O00OOOOOO00O.quantifiers.get(O0O0OO0OOO) <= OO00OOO0O0
                else:
                    O00OOOOO00O = False
            if O0O0OO0OOO.upper() == 'DBLPIM':
                if OOO00000OO0 + OO0O0OOOO0 + OO000O00OO000 > 0:
                    OO0000O00OO = O00OOOOOO00O.quantifiers.get(O0O0OO0OOO)
                    O00OOOOO00O = O00OOOOO00O and OO0000O00OO <= OOO00000OO0 / (OOO00000OO0 + OO0O0OOOO0 + OO000O00OO000)
                else:
                    O00OOOOO00O = False
            if O0O0OO0OOO.upper() == 'EQUIV':
                if OOO00000OO0 + OO0O0OOOO0 + OO000O00OO000 + OO00O0O00000 > 0:
                    OO0000O00OO = O00OOOOOO00O.quantifiers.get(O0O0OO0OOO)
                    O00OOOOO00O = O00OOOOO00O and OO0000O00OO <= (OOO00000OO0 + OO00O0O00000) / (OOO00000OO0 + OO0O0OOOO0 + OO000O00OO000 + OO00O0O00000)
                else:
                    O00OOOOO00O = False
            if O0O0OO0OOO.upper() == 'LAMBDA' or O0O0OO0OOO.upper() == 'FN':
                O0O0OOO0O0O0O = O00OOOOOO00O.quantifiers.get(O0O0OO0OOO)
                O0OOO0OO0O0 = [OOO00000OO0, OO0O0OOOO0, OO000O00OO000, OO00O0O00000]
                OOO00O00OO0O = O0O0OOO0O0O0O.__code__.co_argcount
                if OOO00O00OO0O == 1:
                    O00OOOOO00O = O00OOOOO00O and O0O0OOO0O0O0O(O0OOO0OO0O0)
                elif OOO00O00OO0O == 2:
                    O0O0O0OOO00O0 = {}
                    OO0O0OO0000 = {}
                    OO0O0OO0000['varname'] = O00OOOOOO00O.data['varname']
                    OO0O0OO0000['catnames'] = O00OOOOOO00O.data['catnames']
                    O0O0O0OOO00O0['datalabels'] = OO0O0OO0000
                    O0O0O0OOO00O0['trace_cedent'] = O0OO0O0OOO0O
                    O0O0O0OOO00O0['traces'] = O0O0O0O0OO00
                    O00OOOOO00O = O00OOOOO00O and O0O0OOO0O0O0O(O0OOO0OO0O0, O0O0O0OOO00O0)
                else:
                    print(f'Unsupported number of arguments for lambda function ({OOO00O00OO0O} for procedure SD4ft-Miner')
            O00O00O0OO = {}
        if O00OOOOO00O == True:
            O00OOOOOO00O.stats['total_valid'] += 1
            O00O00O0OO['base'] = OO0OO0OOOOO
            O00O00O0OO['rel_base'] = OO0OO0OOOOO * 1.0 / O00OOOOOO00O.data['rows_count']
            O00O00O0OO['conf'] = OO0O00OOOO
            O00O00O0OO['aad'] = OO0OO0O000
            O00O00O0OO['bad'] = OO00OOO0O0
            O00O00O0OO['fourfold'] = [OOO00000OO0, OO0O0OOOO0, OO000O00OO000, OO00O0O00000]
        return (O00OOOOO00O, O00O00O0OO)

    def _verifysd4ft(OO0OOOOOOO00, O0OO000O00O0O):
        OO0OOOO000 = {}
        O00O0OOOO0O0O = 0
        for OOO000OO0OO in OO0OOOOOOO00.task_actinfo['cedents']:
            OO0OOOO000[OOO000OO0OO['cedent_type']] = OOO000OO0OO['filter_value']
            O00O0OOOO0O0O = O00O0OOOO0O0O + 1
        OOO00O0OOOOOO = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['frst'])
        O0000OOOO0 = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['scnd'])
        OO00O00OOOOO = None
        OO000O00000 = 0
        O00000O0000O = 0
        if OOO00O0OOOOOO > 0:
            OO000O00000 = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['frst']) * 1.0 / OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['cond'] & OO0OOOO000['frst'])
        if O0000OOOO0 > 0:
            O00000O0000O = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['scnd']) * 1.0 / OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['cond'] & OO0OOOO000['scnd'])
        O0000O0OO00 = 1 << OO0OOOOOOO00.data['rows_count']
        OO0000OO00000 = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['frst'])
        O00O00OO0O0OO = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & ~(O0000O0OO00 | OO0OOOO000['succ']) & OO0OOOO000['cond'] & OO0OOOO000['frst'])
        OO00O00OO00 = OO0OOOOOOO00._bitcount(~(O0000O0OO00 | OO0OOOO000['ante']) & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['frst'])
        OO0O00O00O0OO = OO0OOOOOOO00._bitcount(~(O0000O0OO00 | OO0OOOO000['ante']) & ~(O0000O0OO00 | OO0OOOO000['succ']) & OO0OOOO000['cond'] & OO0OOOO000['frst'])
        O00O0O00OO = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['scnd'])
        O0000OO0000 = OO0OOOOOOO00._bitcount(OO0OOOO000['ante'] & ~(O0000O0OO00 | OO0OOOO000['succ']) & OO0OOOO000['cond'] & OO0OOOO000['scnd'])
        OO000O0OOO0 = OO0OOOOOOO00._bitcount(~(O0000O0OO00 | OO0OOOO000['ante']) & OO0OOOO000['succ'] & OO0OOOO000['cond'] & OO0OOOO000['scnd'])
        OO0O0O0OO0O00 = OO0OOOOOOO00._bitcount(~(O0000O0OO00 | OO0OOOO000['ante']) & ~(O0000O0OO00 | OO0OOOO000['succ']) & OO0OOOO000['cond'] & OO0OOOO000['scnd'])
        O0OOOO0OOO000 = True
        for OO0OO0OO00000 in OO0OOOOOOO00.quantifiers.keys():
            if (OO0OO0OO00000.upper() == 'FRSTBASE') | (OO0OO0OO00000.upper() == 'BASE1'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= OOO00O0OOOOOO
            if (OO0OO0OO00000.upper() == 'SCNDBASE') | (OO0OO0OO00000.upper() == 'BASE2'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= O0000OOOO0
            if (OO0OO0OO00000.upper() == 'FRSTRELBASE') | (OO0OO0OO00000.upper() == 'RELBASE1'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= OOO00O0OOOOOO * 1.0 / OO0OOOOOOO00.data['rows_count']
            if (OO0OO0OO00000.upper() == 'SCNDRELBASE') | (OO0OO0OO00000.upper() == 'RELBASE2'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= O0000OOOO0 * 1.0 / OO0OOOOOOO00.data['rows_count']
            if (OO0OO0OO00000.upper() == 'FRSTPIM') | (OO0OO0OO00000.upper() == 'PIM1') | (OO0OO0OO00000.upper() == 'FRSTCONF') | (OO0OO0OO00000.upper() == 'CONF1'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= OO000O00000
            if (OO0OO0OO00000.upper() == 'SCNDPIM') | (OO0OO0OO00000.upper() == 'PIM2') | (OO0OO0OO00000.upper() == 'SCNDCONF') | (OO0OO0OO00000.upper() == 'CONF2'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= O00000O0000O
            if (OO0OO0OO00000.upper() == 'DELTAPIM') | (OO0OO0OO00000.upper() == 'DELTACONF'):
                O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= OO000O00000 - O00000O0000O
            if (OO0OO0OO00000.upper() == 'RATIOPIM') | (OO0OO0OO00000.upper() == 'RATIOCONF'):
                if O00000O0000O > 0:
                    O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) <= OO000O00000 * 1.0 / O00000O0000O
                else:
                    O0OOOO0OOO000 = False
            if (OO0OO0OO00000.upper() == 'RATIOPIM_LEQ') | (OO0OO0OO00000.upper() == 'RATIOCONF_LEQ'):
                if O00000O0000O > 0:
                    O0OOOO0OOO000 = O0OOOO0OOO000 and OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000) >= OO000O00000 * 1.0 / O00000O0000O
                else:
                    O0OOOO0OOO000 = False
            if OO0OO0OO00000.upper() == 'LAMBDA' or OO0OO0OO00000.upper() == 'FN':
                O0OO000000 = OO0OOOOOOO00.quantifiers.get(OO0OO0OO00000)
                OOOOO0O00O000 = O0OO000000.func_code.co_argcount
                OOOO0OO000O = [OO0000OO00000, O00O00OO0O0OO, OO00O00OO00, OO0O00O00O0OO]
                O000000O0O = [O00O0O00OO, O0000OO0000, OO000O0OOO0, OO0O0O0OO0O00]
                if OOOOO0O00O000 == 2:
                    O0OOOO0OOO000 = O0OOOO0OOO000 and O0OO000000(OOOO0OO000O, O000000O0O)
                elif OOOOO0O00O000 == 3:
                    O0OOOO0OOO000 = O0OOOO0OOO000 and O0OO000000(OOOO0OO000O, O000000O0O, None)
                else:
                    print(f'Unsupported number of arguments for lambda function ({OOOOO0O00O000} for procedure SD4ft-Miner')
        O00O0OO0O0OO0 = {}
        if O0OOOO0OOO000 == True:
            OO0OOOOOOO00.stats['total_valid'] += 1
            O00O0OO0O0OO0['base1'] = OOO00O0OOOOOO
            O00O0OO0O0OO0['base2'] = O0000OOOO0
            O00O0OO0O0OO0['rel_base1'] = OOO00O0OOOOOO * 1.0 / OO0OOOOOOO00.data['rows_count']
            O00O0OO0O0OO0['rel_base2'] = O0000OOOO0 * 1.0 / OO0OOOOOOO00.data['rows_count']
            O00O0OO0O0OO0['conf1'] = OO000O00000
            O00O0OO0O0OO0['conf2'] = O00000O0000O
            O00O0OO0O0OO0['deltaconf'] = OO000O00000 - O00000O0000O
            if O00000O0000O > 0:
                O00O0OO0O0OO0['ratioconf'] = OO000O00000 * 1.0 / O00000O0000O
            else:
                O00O0OO0O0OO0['ratioconf'] = None
            O00O0OO0O0OO0['fourfold1'] = [OO0000OO00000, O00O00OO0O0OO, OO00O00OO00, OO0O00O00O0OO]
            O00O0OO0O0OO0['fourfold2'] = [O00O0O00OO, O0000OO0000, OO000O0OOO0, OO0O0O0OO0O00]
        return (O0OOOO0OOO000, O00O0OO0O0OO0)

    def _verify_opt(O000O000O00, O0OOO0000O, O0OO000O0OO):
        O000O000O00.stats['total_ver'] += 1
        O0OO0O0O0000 = False
        if not O0OOO0000O['optim'].get('only_con'):
            return False
        if O000O000O00.verbosity['debug']:
            print(O000O000O00.options['optimizations'])
        if not O000O000O00.options['optimizations']:
            if O000O000O00.verbosity['debug']:
                print('NO OPTS')
            return False
        if O000O000O00.verbosity['debug']:
            print('OPTS')
        O0OO0OOO000 = {}
        for OO0OOO00OOO in O000O000O00.task_actinfo['cedents']:
            if O000O000O00.verbosity['debug']:
                print(OO0OOO00OOO['cedent_type'])
            O0OO0OOO000[OO0OOO00OOO['cedent_type']] = OO0OOO00OOO['filter_value']
            if O000O000O00.verbosity['debug']:
                print(OO0OOO00OOO['cedent_type'] + ' : ' + str(OO0OOO00OOO['filter_value']))
        OO0O0O00O00O0 = 1 << O000O000O00.data['rows_count']
        OOO0O00O00O0O = OO0O0O00O00O0 - 1
        OO0OOO00O000 = ''
        O0000O0OO0O0 = 0
        if O0OO0OOO000.get('ante') != None:
            OOO0O00O00O0O = OOO0O00O00O0O & O0OO0OOO000['ante']
        if O0OO0OOO000.get('succ') != None:
            OOO0O00O00O0O = OOO0O00O00O0O & O0OO0OOO000['succ']
        if O0OO0OOO000.get('cond') != None:
            OOO0O00O00O0O = OOO0O00O00O0O & O0OO0OOO000['cond']
        OO00O0O0OO0 = None
        if (O000O000O00.proc == 'CFMiner') | (O000O000O00.proc == '4ftMiner') | (O000O000O00.proc == 'UICMiner'):
            OO0000OOOOOO = O000O000O00._bitcount(OOO0O00O00O0O)
            if not O000O000O00.O0O0000OO0 == None:
                if not O000O000O00.O0O0000OO0 <= OO0000OOOOOO:
                    O0OO0O0O0000 = True
            if not O000O000O00.OOO0O0O0O000 == None:
                if not O000O000O00.OOO0O0O0O000 <= OO0000OOOOOO * 1.0 / O000O000O00.data['rows_count']:
                    O0OO0O0O0000 = True
        if O000O000O00.proc == 'SD4ftMiner':
            OO0000OOOOOO = O000O000O00._bitcount(OOO0O00O00O0O)
            if (not O000O000O00.OOO0O00OOO == None) & (not O000O000O00.OOOOOO0OO00O0 == None):
                if not max(O000O000O00.OOO0O00OOO, O000O000O00.OOOOOO0OO00O0) <= OO0000OOOOOO:
                    O0OO0O0O0000 = True
            if (not O000O000O00.O00O0O0000OO == None) & (not O000O000O00.O0OO000O0OO0O == None):
                if not max(O000O000O00.O00O0O0000OO, O000O000O00.O0OO000O0OO0O) <= OO0000OOOOOO * 1.0 / O000O000O00.data['rows_count']:
                    O0OO0O0O0000 = True
        return O0OO0O0O0000

    def _print(O0O0OOOOOO0O, O00OO00O00000, O0000O0OOO, O0O000OOO0O0):
        if len(O0000O0OOO) != len(O0O000OOO0O0):
            print('DIFF IN LEN for following cedent : ' + str(len(O0000O0OOO)) + ' vs ' + str(len(O0O000OOO0O0)))
            print('trace cedent : ' + str(O0000O0OOO) + ', traces ' + str(O0O000OOO0O0))
        O00O000O0O0OO = ''
        OOOO00OO0O = {}
        O0OOO000O0O0O = []
        for OOOO0O0OO0 in range(len(O0000O0OOO)):
            O0O000000O = O0O0OOOOOO0O.data['varname'].index(O00OO00O00000['defi'].get('attributes')[O0000O0OOO[OOOO0O0OO0]].get('name'))
            O00O000O0O0OO = O00O000O0O0OO + O0O0OOOOOO0O.data['varname'][O0O000000O] + '('
            O0OOO000O0O0O.append(O0O000000O)
            OOO0O0000O = []
            for O0OOOOO00OOO0 in O0O000OOO0O0[OOOO0O0OO0]:
                O00O000O0O0OO = O00O000O0O0OO + str(O0O0OOOOOO0O.data['catnames'][O0O000000O][O0OOOOO00OOO0]) + ' '
                OOO0O0000O.append(str(O0O0OOOOOO0O.data['catnames'][O0O000000O][O0OOOOO00OOO0]))
            O00O000O0O0OO = O00O000O0O0OO[:-1] + ')'
            OOOO00OO0O[O0O0OOOOOO0O.data['varname'][O0O000000O]] = OOO0O0000O
            if OOOO0O0OO0 + 1 < len(O0000O0OOO):
                O00O000O0O0OO = O00O000O0O0OO + ' & '
        return (O00O000O0O0OO, OOOO00OO0O, O0OOO000O0O0O)

    def _print_hypo(O00O000O0000O, OO0OOOOO0OO):
        O00O000O0000O.print_rule(OO0OOOOO0OO)

    def _print_rule(O00OO000O000, OO0O000O00O0):
        if O00OO000O000.verbosity['print_rules']:
            print('Rules info : ' + str(OO0O000O00O0['params']))
            for O0O0OO00O0O in O00OO000O000.task_actinfo['cedents']:
                print(O0O0OO00O0O['cedent_type'] + ' = ' + O0O0OO00O0O['generated_string'])

    def _genvar(O0O00O0OO0O, O0OOOO0O0O00, OOOOOO0OO0, OO0O0000000, O0O000O00OO0O, O00OOOOO0O, O00OOO0OO0, OO00OO0O0OOO0, OOO0OO0000, OOO00O00OO0):
        O0O0OOO000O = 0
        O0OO0O000O0O = []
        for OO000OOOO0 in range(OOOOOO0OO0['num_cedent']):
            if 'force' in OOOOOO0OO0['defi'].get('attributes')[OO000OOOO0] and OOOOOO0OO0['defi'].get('attributes')[OO000OOOO0].get('force'):
                O0OO0O000O0O.append(OO000OOOO0)
        if OOOOOO0OO0['num_cedent'] > 0:
            O0O0OOO000O = (OOO00O00OO0 - OOO0OO0000) / OOOOOO0OO0['num_cedent']
        if OOOOOO0OO0['num_cedent'] == 0:
            if len(O0OOOO0O0O00['cedents_to_do']) > len(O0OOOO0O0O00['cedents']):
                OO0O00OOO0OO, OOOO0O00OOO0O, OO00O00O0OO0O = O0O00O0OO0O._print(OOOOOO0OO0, OO0O0000000, O0O000O00OO0O)
                OOOOOO0OO0['generated_string'] = OO0O00OOO0OO
                OOOOOO0OO0['rule'] = OOOO0O00OOO0O
                OOOOOO0OO0['filter_value'] = (1 << O0O00O0OO0O.data['rows_count']) - 1
                OOOOOO0OO0['traces'] = []
                OOOOOO0OO0['trace_cedent'] = []
                OOOOOO0OO0['trace_cedent_asindata'] = []
                O0OOOO0O0O00['cedents'].append(OOOOOO0OO0)
                OO0O0000000.append(None)
                O0O00O0OO0O._start_cedent(O0OOOO0O0O00, OOO0OO0000, OOO00O00OO0)
                O0OOOO0O0O00['cedents'].pop()
        for OO000OOOO0 in range(OOOOOO0OO0['num_cedent']):
            O0OOOO00O0OO = True
            for OO0O00OOO000 in range(len(O0OO0O000O0O)):
                if OO0O00OOO000 < OO000OOOO0 and OO0O00OOO000 not in OO0O0000000 and (OO0O00OOO000 in O0OO0O000O0O):
                    O0OOOO00O0OO = False
            if (len(OO0O0000000) == 0 or OO000OOOO0 > OO0O0000000[-1]) and O0OOOO00O0OO:
                OO0O0000000.append(OO000OOOO0)
                O0OO00OO00O = O0O00O0OO0O.data['varname'].index(OOOOOO0OO0['defi'].get('attributes')[OO000OOOO0].get('name'))
                OO00OOOO0000 = OOOOOO0OO0['defi'].get('attributes')[OO000OOOO0].get('minlen')
                O0O00000O0OOO = OOOOOO0OO0['defi'].get('attributes')[OO000OOOO0].get('maxlen')
                O000000000 = OOOOOO0OO0['defi'].get('attributes')[OO000OOOO0].get('type')
                OO0O0O000O = len(O0O00O0OO0O.data['dm'][O0OO00OO00O])
                OO0O0OOO00OO = []
                O0O000O00OO0O.append(OO0O0OOO00OO)
                O0O000OOOOO = int(0)
                O0O00O0OO0O._gencomb(O0OOOO0O0O00, OOOOOO0OO0, OO0O0000000, O0O000O00OO0O, OO0O0OOO00OO, O00OOOOO0O, O0O000OOOOO, OO0O0O000O, O000000000, O00OOO0OO0, OO00OO0O0OOO0, OO00OOOO0000, O0O00000O0OOO, OOO0OO0000 + OO000OOOO0 * O0O0OOO000O, OOO0OO0000 + (OO000OOOO0 + 1) * O0O0OOO000O)
                O0O000O00OO0O.pop()
                OO0O0000000.pop()

    def _gencomb(OOO0O0O0OO, OO0OO0O00OO, OOO0O000OOO0O, OOO0000O00OOO, O0OOOOO0000OO, OO0OO0O00000, O000OO0OOOO, OOOO000OOO0, OOOO0OO0O0O00, OOOO0000O0, OOOOOOO0OOO, O0O0O00OOOO0, O00O0O0OOO0, OOOOOOO0OO000, OO0OO0O00O, O000OO00OO000, O0O0OOO0000=None):
        OOOOOO0O0OOO0 = []
        OOOOO00OOOO = O0O0OOO0000
        if OOOO0000O0 == 'subset':
            if len(OO0OO0O00000) == 0:
                OOOOOO0O0OOO0 = range(OOOO0OO0O0O00)
            else:
                OOOOOO0O0OOO0 = range(OO0OO0O00000[-1] + 1, OOOO0OO0O0O00)
        elif OOOO0000O0 == 'seq':
            if len(OO0OO0O00000) == 0:
                OOOOOO0O0OOO0 = range(OOOO0OO0O0O00 - O00O0O0OOO0 + 1)
            else:
                if OO0OO0O00000[-1] + 1 == OOOO0OO0O0O00:
                    return
                OO0O000O0O = OO0OO0O00000[-1] + 1
                OOOOOO0O0OOO0.append(OO0O000O0O)
        elif OOOO0000O0 == 'lcut':
            if len(OO0OO0O00000) == 0:
                OO0O000O0O = 0
            else:
                if OO0OO0O00000[-1] + 1 == OOOO0OO0O0O00:
                    return
                OO0O000O0O = OO0OO0O00000[-1] + 1
            OOOOOO0O0OOO0.append(OO0O000O0O)
        elif OOOO0000O0 == 'rcut':
            if len(OO0OO0O00000) == 0:
                OO0O000O0O = OOOO0OO0O0O00 - 1
            else:
                if OO0OO0O00000[-1] == 0:
                    return
                OO0O000O0O = OO0OO0O00000[-1] - 1
                if OOO0O0O0OO.verbosity['debug']:
                    print('Olditem: ' + str(OO0OO0O00000[-1]) + ', Newitem : ' + str(OO0O000O0O))
            OOOOOO0O0OOO0.append(OO0O000O0O)
        elif OOOO0000O0 == 'one':
            if len(OO0OO0O00000) == 0:
                OO0O0OOOO0O = OOO0O0O0OO.data['varname'].index(OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('name'))
                try:
                    OO0O000O0O = OOO0O0O0OO.data['catnames'][OO0O0OOOO0O].index(OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('value'))
                except:
                    print(f"ERROR: attribute '{OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('name')}' has not value '{OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('value')}'")
                    exit(1)
                OOOOOO0O0OOO0.append(OO0O000O0O)
                O00O0O0OOO0 = 1
                OOOOOOO0OO000 = 1
            else:
                print('DEBUG: one category should not have more categories')
                return
        elif OOOO0000O0 == 'list':
            if OOOOO00OOOO is None:
                OO0O0OOOO0O = OOO0O0O0OO.data['varname'].index(OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('name'))
                O00O0O00O0 = None
                OOO0O00OO0 = []
                try:
                    O00O0OOO0OO0O = OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('value')
                    for O000O00O000 in O00O0OOO0OO0O:
                        O00O0O00O0 = O000O00O000
                        OO0O000O0O = OOO0O0O0OO.data['catnames'][OO0O0OOOO0O].index(O000O00O000)
                        OOO0O00OO0.append(OO0O000O0O)
                except:
                    print(f"ERROR: attribute '{OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('name')}' has not value '{O000O00O000}'")
                    exit(1)
                OOOOO00OOOO = OOO0O00OO0
                O00O0O0OOO0 = len(OOOOO00OOOO)
                OOOOOOO0OO000 = len(OOOOO00OOOO)
            OOOOOO0O0OOO0.append(OOOOO00OOOO[len(OO0OO0O00000)])
        else:
            print('Attribute type ' + OOOO0000O0 + ' not supported.')
            return
        if len(OOOOOO0O0OOO0) > 0:
            OOOO00000O0OO = (O000OO00OO000 - OO0OO0O00O) / len(OOOOOO0O0OOO0)
        else:
            OOOO00000O0OO = 0
        O0O0O00000OOO = 0
        for OOO0OOO00O00 in OOOOOO0O0OOO0:
            OO0OO0O00000.append(OOO0OOO00O00)
            O0OOOOO0000OO.pop()
            O0OOOOO0000OO.append(OO0OO0O00000)
            OOOOO00O0OOOO = OOOO000OOO0 | OOO0O0O0OO.data['dm'][OOO0O0O0OO.data['varname'].index(OOO0O000OOO0O['defi'].get('attributes')[OOO0000O00OOO[-1]].get('name'))][OOO0OOO00O00]
            O00OO000OOO0O = 1
            if len(OOO0000O00OOO) < OOOOOOO0OOO:
                O00OO000OOO0O = -1
                if OOO0O0O0OO.verbosity['debug']:
                    print('DEBUG: will not verify, low cedent length')
            if len(O0OOOOO0000OO[-1]) < O00O0O0OOO0:
                O00OO000OOO0O = 0
                if OOO0O0O0OO.verbosity['debug']:
                    print('DEBUG: will not verify, low attribute length')
            O00OO00O0OO = 0
            if OOO0O000OOO0O['defi'].get('type') == 'con':
                O00OO00O0OO = O000OO0OOOO & OOOOO00O0OOOO
            else:
                O00OO00O0OO = O000OO0OOOO | OOOOO00O0OOOO
            OOO0O000OOO0O['trace_cedent'] = OOO0000O00OOO
            OOO0O000OOO0O['traces'] = O0OOOOO0000OO
            OO000OO0O0000, O0OOO0O00OO, OO0OO000O0O = OOO0O0O0OO._print(OOO0O000OOO0O, OOO0000O00OOO, O0OOOOO0000OO)
            OOO0O000OOO0O['generated_string'] = OO000OO0O0000
            OOO0O000OOO0O['rule'] = O0OOO0O00OO
            OOO0O000OOO0O['filter_value'] = O00OO00O0OO
            OOO0O000OOO0O['traces'] = copy.deepcopy(O0OOOOO0000OO)
            OOO0O000OOO0O['trace_cedent'] = copy.deepcopy(OOO0000O00OOO)
            OOO0O000OOO0O['trace_cedent_asindata'] = copy.deepcopy(OO0OO000O0O)
            if OOO0O0O0OO.verbosity['debug']:
                print(f"TC :{OOO0O000OOO0O['trace_cedent_asindata']}")
            OO0OO0O00OO['cedents'].append(OOO0O000OOO0O)
            OOOOOOO0OOO00 = OOO0O0O0OO._verify_opt(OO0OO0O00OO, OOO0O000OOO0O)
            if OOO0O0O0OO.verbosity['debug']:
                print(f"DEBUG: {OOO0O000OOO0O['generated_string']}.")
                print(f'DEBUG: {OOO0000O00OOO},{OOOOOOO0OOO}.')
                if OOOOOOO0OOO00:
                    print('DEBUG: Optimization: cutting')
            if not OOOOOOO0OOO00:
                if O00OO000OOO0O == 1:
                    if OOO0O0O0OO.verbosity['debug']:
                        print('DEBUG: verifying')
                    if len(OO0OO0O00OO['cedents_to_do']) == len(OO0OO0O00OO['cedents']):
                        if OOO0O0O0OO.proc == 'CFMiner':
                            OO00O00OO0, O0O0000OOOO = OOO0O0O0OO._verifyCF(O00OO00O0OO)
                        elif OOO0O0O0OO.proc == 'UICMiner':
                            OO00O00OO0, O0O0000OOOO = OOO0O0O0OO._verifyUIC(O00OO00O0OO)
                        elif OOO0O0O0OO.proc == '4ftMiner':
                            OO00O00OO0, O0O0000OOOO = OOO0O0O0OO._verify4ft(OOOOO00O0OOOO, OOO0000O00OOO, O0OOOOO0000OO)
                        elif OOO0O0O0OO.proc == 'SD4ftMiner':
                            OO00O00OO0, O0O0000OOOO = OOO0O0O0OO._verifysd4ft(OOOOO00O0OOOO)
                        else:
                            print('Unsupported procedure : ' + OOO0O0O0OO.proc)
                            exit(0)
                        if OO00O00OO0 == True:
                            OO0O0O00OOOOO = {}
                            OO0O0O00OOOOO['rule_id'] = OOO0O0O0OO.stats['total_valid']
                            OO0O0O00OOOOO['cedents_str'] = {}
                            OO0O0O00OOOOO['cedents_struct'] = {}
                            OO0O0O00OOOOO['traces'] = {}
                            OO0O0O00OOOOO['trace_cedent_taskorder'] = {}
                            OO0O0O00OOOOO['trace_cedent_dataorder'] = {}
                            for OOOOO00OOOOO in OO0OO0O00OO['cedents']:
                                if OOO0O0O0OO.verbosity['debug']:
                                    print(OOOOO00OOOOO)
                                OO0O0O00OOOOO['cedents_str'][OOOOO00OOOOO['cedent_type']] = OOOOO00OOOOO['generated_string']
                                OO0O0O00OOOOO['cedents_struct'][OOOOO00OOOOO['cedent_type']] = OOOOO00OOOOO['rule']
                                OO0O0O00OOOOO['traces'][OOOOO00OOOOO['cedent_type']] = OOOOO00OOOOO['traces']
                                OO0O0O00OOOOO['trace_cedent_taskorder'][OOOOO00OOOOO['cedent_type']] = OOOOO00OOOOO['trace_cedent']
                                OO0O0O00OOOOO['trace_cedent_dataorder'][OOOOO00OOOOO['cedent_type']] = OOOOO00OOOOO['trace_cedent_asindata']
                            OO0O0O00OOOOO['params'] = O0O0000OOOO
                            if OOO0O0O0OO.verbosity['debug']:
                                OO0O0O00OOOOO['trace_cedent'] = copy.deepcopy(OOO0000O00OOO)
                            OOO0O0O0OO._print_rule(OO0O0O00OOOOO)
                            OOO0O0O0OO.rulelist.append(OO0O0O00OOOOO)
                        OOO0O0O0OO.stats['total_cnt'] += 1
                        OOO0O0O0OO.stats['total_ver'] += 1
                if O00OO000OOO0O >= 1:
                    if len(OO0OO0O00OO['cedents_to_do']) > len(OO0OO0O00OO['cedents']):
                        OOO0O0O0OO._start_cedent(OO0OO0O00OO, OO0OO0O00O + O0O0O00000OOO * OOOO00000O0OO, OO0OO0O00O + (O0O0O00000OOO + 0.33) * OOOO00000O0OO)
                OO0OO0O00OO['cedents'].pop()
                if not O00OO000OOO0O == 0 and len(OOO0000O00OOO) < O0O0O00OOOO0:
                    OOO0O0O0OO._genvar(OO0OO0O00OO, OOO0O000OOO0O, OOO0000O00OOO, O0OOOOO0000OO, O00OO00O0OO, OOOOOOO0OOO, O0O0O00OOOO0, OO0OO0O00O + (O0O0O00000OOO + 0.33) * OOOO00000O0OO, OO0OO0O00O + (O0O0O00000OOO + 0.66) * OOOO00000O0OO)
            else:
                OO0OO0O00OO['cedents'].pop()
            if len(OO0OO0O00000) < OOOOOOO0OO000:
                OOO0O0O0OO._gencomb(OO0OO0O00OO, OOO0O000OOO0O, OOO0000O00OOO, O0OOOOO0000OO, OO0OO0O00000, O000OO0OOOO, OOOOO00O0OOOO, OOOO0OO0O0O00, OOOO0000O0, OOOOOOO0OOO, O0O0O00OOOO0, O00O0O0OOO0, OOOOOOO0OO000, OO0OO0O00O + OOOO00000O0OO * (O0O0O00000OOO + 0.66), OO0OO0O00O + OOOO00000O0OO * (O0O0O00000OOO + 1), OOOOO00OOOO)
            OO0OO0O00000.pop()
            O0O0O00000OOO += 1
            if OOO0O0O0OO.options['progressbar']:
                OOO0O0O0OO.bar.update(min(100, OO0OO0O00O + OOOO00000O0OO * O0O0O00000OOO))
            if OOO0O0O0OO.verbosity['debug']:
                print(f'Progress : lower: {OO0OO0O00O}, step: {OOOO00000O0OO}, step_no: {O0O0O00000OOO} overall: {OO0OO0O00O + OOOO00000O0OO * O0O0O00000OOO}')

    def _start_cedent(OOO00O000000, O0O00OO00OO0, OO00O0OO0O00, OO0OOO0O00):
        if len(O0O00OO00OO0['cedents_to_do']) > len(O0O00OO00OO0['cedents']):
            O00OOOO00OOO = []
            O0OOOO0O00 = []
            OO00000OOO = {}
            OO00000OOO['cedent_type'] = O0O00OO00OO0['cedents_to_do'][len(O0O00OO00OO0['cedents'])]
            OO000OO000000 = OO00000OOO['cedent_type']
            if (OO000OO000000[-1] == '-') | (OO000OO000000[-1] == '+'):
                OO000OO000000 = OO000OO000000[:-1]
            OO00000OOO['defi'] = OOO00O000000.kwargs.get(OO000OO000000)
            if OO00000OOO['defi'] == None:
                print('Error getting cedent ', OO00000OOO['cedent_type'])
            O0OOO0000OOO = int(0)
            OO00000OOO['num_cedent'] = len(OO00000OOO['defi'].get('attributes'))
            if OO00000OOO['defi'].get('type') == 'con':
                O0OOO0000OOO = (1 << OOO00O000000.data['rows_count']) - 1
            OOO00O000000._genvar(O0O00OO00OO0, OO00000OOO, O00OOOO00OOO, O0OOOO0O00, O0OOO0000OOO, OO00000OOO['defi'].get('minlen'), OO00000OOO['defi'].get('maxlen'), OO00O0OO0O00, OO0OOO0O00)

    def _calc_all(O00O0O0O0OOO, **O000O0000O):
        if 'df' in O000O0000O:
            O00O0O0O0OOO._prep_data(O00O0O0O0OOO.kwargs.get('df'))
        if not O00O0O0O0OOO.OOOOOOO0OOOO0:
            print('ERROR: dataframe is missing and not initialized with dataframe')
        else:
            O00O0O0O0OOO._calculate(**O000O0000O)

    def _check_cedents(OOO0000OOO, OOOOOO0O0O, **OOOO0O0OO00O):
        O000O00000 = True
        if OOOO0O0OO00O.get('quantifiers', None) == None:
            print(f'Error: missing quantifiers.')
            O000O00000 = False
            return O000O00000
        if type(OOOO0O0OO00O.get('quantifiers')) != dict:
            print(f'Error: quantifiers are not dictionary type.')
            O000O00000 = False
            return O000O00000
        for O00O00OOO000 in OOOOOO0O0O:
            if OOOO0O0OO00O.get(O00O00OOO000, None) == None:
                print(f'Error: cedent {O00O00OOO000} is missing in parameters.')
                O000O00000 = False
                return O000O00000
            O00OOO00OO0OO = OOOO0O0OO00O.get(O00O00OOO000)
            if (O00OOO00OO0OO.get('minlen'), None) == None:
                print(f'Error: cedent {O00O00OOO000} has no minimal length specified.')
                O000O00000 = False
                return O000O00000
            if not type(O00OOO00OO0OO.get('minlen')) is int:
                print(f"Error: cedent {O00O00OOO000} has invalid type of minimal length ({type(O00OOO00OO0OO.get('minlen'))}).")
                O000O00000 = False
                return O000O00000
            if (O00OOO00OO0OO.get('maxlen'), None) == None:
                print(f'Error: cedent {O00O00OOO000} has no maximal length specified.')
                O000O00000 = False
                return O000O00000
            if not type(O00OOO00OO0OO.get('maxlen')) is int:
                print(f'Error: cedent {O00O00OOO000} has invalid type of maximal length.')
                O000O00000 = False
                return O000O00000
            if (O00OOO00OO0OO.get('type'), None) == None:
                print(f'Error: cedent {O00O00OOO000} has no type specified.')
                O000O00000 = False
                return O000O00000
            if not O00OOO00OO0OO.get('type') in ['con', 'dis']:
                print(f"Error: cedent {O00O00OOO000} has invalid type. Allowed values are 'con' and 'dis'.")
                O000O00000 = False
                return O000O00000
            if (O00OOO00OO0OO.get('attributes'), None) == None:
                print(f'Error: cedent {O00O00OOO000} has no attributes specified.')
                O000O00000 = False
                return O000O00000
            for OOOOOOOO0OOO0 in O00OOO00OO0OO.get('attributes'):
                if (OOOOOOOO0OOO0.get('name'), None) == None:
                    print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0} has no 'name' attribute specified.")
                    O000O00000 = False
                    return O000O00000
                if not OOOOOOOO0OOO0.get('name') in OOO0000OOO.data['varname']:
                    print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} not in variable list. Please check spelling.")
                    O000O00000 = False
                    return O000O00000
                if (OOOOOOOO0OOO0.get('type'), None) == None:
                    print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} has no 'type' attribute specified.")
                    O000O00000 = False
                    return O000O00000
                if not OOOOOOOO0OOO0.get('type') in ['rcut', 'lcut', 'seq', 'subset', 'one', 'list']:
                    print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} has unsupported type {OOOOOOOO0OOO0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one','list'.")
                    O000O00000 = False
                    return O000O00000
                if (OOOOOOOO0OOO0.get('minlen'), None) == None:
                    print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} has no minimal length specified.")
                    O000O00000 = False
                    return O000O00000
                if not type(OOOOOOOO0OOO0.get('minlen')) is int:
                    if not (OOOOOOOO0OOO0.get('type') == 'one' or OOOOOOOO0OOO0.get('type') == 'list'):
                        print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} has invalid type of minimal length.")
                        O000O00000 = False
                        return O000O00000
                if (OOOOOOOO0OOO0.get('maxlen'), None) == None:
                    print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} has no maximal length specified.")
                    O000O00000 = False
                    return O000O00000
                if not type(OOOOOOOO0OOO0.get('maxlen')) is int:
                    if not (OOOOOOOO0OOO0.get('type') == 'one' or OOOOOOOO0OOO0.get('type') == 'list'):
                        print(f"Error: cedent {O00O00OOO000} / attribute {OOOOOOOO0OOO0.get('name')} has invalid type of maximal length.")
                        O000O00000 = False
                        return O000O00000
        return O000O00000

    def _calculate(OOO0O000O0, **O00OO0OO0O0O0):
        if OOO0O000O0.data['data_prepared'] == 0:
            print('Error: data not prepared')
            return
        OOO0O000O0.kwargs = O00OO0OO0O0O0
        OOO0O000O0.proc = O00OO0OO0O0O0.get('proc')
        OOO0O000O0.quantifiers = O00OO0OO0O0O0.get('quantifiers')
        OOO0O000O0._init_task()
        OOO0O000O0.stats['start_proc_time'] = time.time()
        OOO0O000O0.task_actinfo['cedents_to_do'] = []
        OOO0O000O0.task_actinfo['cedents'] = []
        if O00OO0OO0O0O0.get('proc') == 'UICMiner':
            if not OOO0O000O0._check_cedents(['ante'], **O00OO0OO0O0O0):
                return
            OO0OOO000O = O00OO0OO0O0O0.get('cond')
            if OO0OOO000O != None:
                OOO0O000O0.task_actinfo['cedents_to_do'].append('cond')
            else:
                OO0O0OOO0O = OOO0O000O0.cedent
                OO0O0OOO0O['cedent_type'] = 'cond'
                OO0O0OOO0O['filter_value'] = (1 << OOO0O000O0.data['rows_count']) - 1
                OO0O0OOO0O['generated_string'] = '---'
                if OOO0O000O0.verbosity['debug']:
                    print(OO0O0OOO0O['filter_value'])
                OOO0O000O0.task_actinfo['cedents_to_do'].append('cond')
                OOO0O000O0.task_actinfo['cedents'].append(OO0O0OOO0O)
            OOO0O000O0.task_actinfo['cedents_to_do'].append('ante')
            if O00OO0OO0O0O0.get('target', None) == None:
                print('ERROR: no succedent/target variable defined for UIC Miner')
                return
            if not O00OO0OO0O0O0.get('target') in OOO0O000O0.data['varname']:
                print("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")
                return
            if 'aad_score' in OOO0O000O0.quantifiers:
                if not 'aad_weights' in OOO0O000O0.quantifiers:
                    print('ERROR: for aad quantifier you need to specify aad weights.')
                    return
                if not len(OOO0O000O0.quantifiers.get('aad_weights')) == len(OOO0O000O0.data['dm'][OOO0O000O0.data['varname'].index(OOO0O000O0.kwargs.get('target'))]):
                    print('ERROR: aad weights has different number of weights than classes of target variable.')
                    return
        elif O00OO0OO0O0O0.get('proc') == 'CFMiner':
            OOO0O000O0.task_actinfo['cedents_to_do'] = ['cond']
            if O00OO0OO0O0O0.get('target', None) == None:
                print('ERROR: no target variable defined for CF Miner')
                return
            OO0000000O0 = O00OO0OO0O0O0.get('target', None)
            OOO0O000O0.profiles['hist_target_entire_dataset_labels'] = OOO0O000O0.data['catnames'][OOO0O000O0.data['varname'].index(OOO0O000O0.kwargs.get('target'))]
            OOOO00OOOO000 = OOO0O000O0.data['dm'][OOO0O000O0.data['varname'].index(OOO0O000O0.kwargs.get('target'))]
            OOO0000OO0 = []
            for O000O0O00O in range(len(OOOO00OOOO000)):
                OO000OO000O = OOO0O000O0._bitcount(OOOO00OOOO000[O000O0O00O])
                OOO0000OO0.append(OO000OO000O)
            OOO0O000O0.profiles['hist_target_entire_dataset_values'] = OOO0000OO0
            if not OOO0O000O0._check_cedents(['cond'], **O00OO0OO0O0O0):
                return
            if not O00OO0OO0O0O0.get('target') in OOO0O000O0.data['varname']:
                print("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")
                return
            if 'aad' in OOO0O000O0.quantifiers:
                if not 'aad_weights' in OOO0O000O0.quantifiers:
                    print('ERROR: for aad quantifier you need to specify aad weights.')
                    return
                if not len(OOO0O000O0.quantifiers.get('aad_weights')) == len(OOO0O000O0.data['dm'][OOO0O000O0.data['varname'].index(OOO0O000O0.kwargs.get('target'))]):
                    print('ERROR: aad weights has different number of weights than classes of target variable.')
                    return
        elif O00OO0OO0O0O0.get('proc') == '4ftMiner':
            if not OOO0O000O0._check_cedents(['ante', 'succ'], **O00OO0OO0O0O0):
                return
            OO0OOO000O = O00OO0OO0O0O0.get('cond')
            if OO0OOO000O != None:
                OOO0O000O0.task_actinfo['cedents_to_do'].append('cond')
            else:
                OO0O0OOO0O = OOO0O000O0.cedent
                OO0O0OOO0O['cedent_type'] = 'cond'
                OO0O0OOO0O['filter_value'] = (1 << OOO0O000O0.data['rows_count']) - 1
                OO0O0OOO0O['generated_string'] = '---'
                OOO0O000O0.task_actinfo['cedents_to_do'].append('cond')
                OOO0O000O0.task_actinfo['cedents'].append(OO0O0OOO0O)
            OOO0O000O0.task_actinfo['cedents_to_do'].append('ante')
            OOO0O000O0.task_actinfo['cedents_to_do'].append('succ')
        elif O00OO0OO0O0O0.get('proc') == 'SD4ftMiner':
            if not OOO0O000O0._check_cedents(['ante', 'succ', 'frst', 'scnd'], **O00OO0OO0O0O0):
                return
            OO0OOO000O = O00OO0OO0O0O0.get('cond')
            if OO0OOO000O != None:
                OOO0O000O0.task_actinfo['cedents_to_do'].append('cond')
            else:
                OO0O0OOO0O = OOO0O000O0.cedent
                OO0O0OOO0O['cedent_type'] = 'cond'
                OO0O0OOO0O['filter_value'] = (1 << OOO0O000O0.data['rows_count']) - 1
                OO0O0OOO0O['generated_string'] = '---'
                OOO0O000O0.task_actinfo['cedents_to_do'].append('cond')
                OOO0O000O0.task_actinfo['cedents'].append(OO0O0OOO0O)
            OOO0O000O0.task_actinfo['cedents_to_do'].append('frst')
            OOO0O000O0.task_actinfo['cedents_to_do'].append('scnd')
            OOO0O000O0.task_actinfo['cedents_to_do'].append('ante')
            OOO0O000O0.task_actinfo['cedents_to_do'].append('succ')
        else:
            print('Unsupported procedure')
            return
        print('Will go for ', O00OO0OO0O0O0.get('proc'))
        OOO0O000O0.task_actinfo['optim'] = {}
        O00000000OO0O = True
        for O0OO00O0O0O0 in OOO0O000O0.task_actinfo['cedents_to_do']:
            try:
                O0O0OOO0OO00 = OOO0O000O0.kwargs.get(O0OO00O0O0O0)
                if OOO0O000O0.verbosity['debug']:
                    print(O0O0OOO0OO00)
                    print(f"...cedent {O0OO00O0O0O0} is type {O0O0OOO0OO00.get('type')}")
                    print(f"Will check cedent type {O0OO00O0O0O0} : {O0O0OOO0OO00.get('type')}")
                if O0O0OOO0OO00.get('type') != 'con':
                    O00000000OO0O = False
                    if OOO0O000O0.verbosity['debug']:
                        print(f"Cannot optim due to cedent type {O0OO00O0O0O0} : {O0O0OOO0OO00.get('type')}")
            except:
                OO0OO00O0O = 1 < 2
        if OOO0O000O0.options['optimizations'] == False:
            O00000000OO0O = False
        OOO0OO0000OO0 = {}
        OOO0OO0000OO0['only_con'] = O00000000OO0O
        OOO0O000O0.task_actinfo['optim'] = OOO0OO0000OO0
        if OOO0O000O0.verbosity['debug']:
            print('Starting to prepare data.')
            OOO0O000O0._prep_data(OOO0O000O0.data.df)
            OOO0O000O0.stats['mid1_time'] = time.time()
            OOO0O000O0.quantifiers = O00OO0OO0O0O0.get('self.quantifiers')
        print('Starting to mine rules.')
        sys.stdout.flush()
        time.sleep(0.01)
        if OOO0O000O0.options['progressbar']:
            O0O00OO00O = [progressbar.Percentage(), progressbar.Bar(), progressbar.Timer()]
            OOO0O000O0.bar = progressbar.ProgressBar(widgets=O0O00OO00O, max_value=100, fd=sys.stdout).start()
            OOO0O000O0.bar.update(0)
        OOO0O000O0.progress_lower = 0
        OOO0O000O0.progress_upper = 100
        OOO0O000O0._start_cedent(OOO0O000O0.task_actinfo, OOO0O000O0.progress_lower, OOO0O000O0.progress_upper)
        if OOO0O000O0.options['progressbar']:
            OOO0O000O0.bar.update(100)
            OOO0O000O0.bar.finish()
        OOO0O000O0.stats['end_proc_time'] = time.time()
        print('Done. Total verifications : ' + str(OOO0O000O0.stats['total_cnt']) + ', rules ' + str(OOO0O000O0.stats['total_valid']) + ', times: prep ' + '{:.2f}'.format(OOO0O000O0.stats['end_prep_time'] - OOO0O000O0.stats['start_prep_time']) + 'sec, processing ' + '{:.2f}'.format(OOO0O000O0.stats['end_proc_time'] - OOO0O000O0.stats['start_proc_time']) + 'sec')
        OO0O0O0O0OO = {}
        O0O000OOO0O = {}
        O0O000OOO0O['guid'] = OOO0O000O0.guid
        O0O000OOO0O['task_type'] = O00OO0OO0O0O0.get('proc')
        O0O000OOO0O['target'] = O00OO0OO0O0O0.get('target')
        O0O000OOO0O['self.quantifiers'] = OOO0O000O0.quantifiers
        if O00OO0OO0O0O0.get('cond') != None:
            O0O000OOO0O['cond'] = O00OO0OO0O0O0.get('cond')
        if O00OO0OO0O0O0.get('ante') != None:
            O0O000OOO0O['ante'] = O00OO0OO0O0O0.get('ante')
        if O00OO0OO0O0O0.get('succ') != None:
            O0O000OOO0O['succ'] = O00OO0OO0O0O0.get('succ')
        if O00OO0OO0O0O0.get('opts') != None:
            O0O000OOO0O['opts'] = O00OO0OO0O0O0.get('opts')
        if OOO0O000O0.df is None:
            O0O000OOO0O['rowcount'] = OOO0O000O0.data['rows_count']
        else:
            O0O000OOO0O['rowcount'] = len(OOO0O000O0.df.index)
        OO0O0O0O0OO['taskinfo'] = O0O000OOO0O
        OO0000OOO0O = {}
        OO0000OOO0O['total_verifications'] = OOO0O000O0.stats['total_cnt']
        OO0000OOO0O['valid_rules'] = OOO0O000O0.stats['total_valid']
        OO0000OOO0O['total_verifications_with_opt'] = OOO0O000O0.stats['total_ver']
        OO0000OOO0O['time_prep'] = OOO0O000O0.stats['end_prep_time'] - OOO0O000O0.stats['start_prep_time']
        OO0000OOO0O['time_processing'] = OOO0O000O0.stats['end_proc_time'] - OOO0O000O0.stats['start_proc_time']
        OO0000OOO0O['time_total'] = OOO0O000O0.stats['end_prep_time'] - OOO0O000O0.stats['start_prep_time'] + OOO0O000O0.stats['end_proc_time'] - OOO0O000O0.stats['start_proc_time']
        OO0O0O0O0OO['summary_statistics'] = OO0000OOO0O
        OO0O0O0O0OO['rules'] = OOO0O000O0.rulelist
        O0OOO0OOOO = {}
        O0OOO0OOOO['varname'] = OOO0O000O0.data['varname']
        O0OOO0OOOO['catnames'] = OOO0O000O0.data['catnames']
        OO0O0O0O0OO['datalabels'] = O0OOO0OOOO
        OOO0O000O0.result = OO0O0O0O0OO

    def hide_rules(O00O0O0OO00, hidearray=None):
        """
        Hides rules in result rulelist
        :param array hidearray: list of booleans with length of the rulecount that indicates for each rule if to display or not
        Note that all rules are available to display, this method apply only to print_rulelist(). When iterating over rulelist, <cleverminer>.hidearray should be used
        """
        if hidearray == None:
            O00O0O0OO00.hidearray = None
        if len(hidearray) == O00O0O0OO00.get_rulecount():
            if all((isinstance(O00O0000O00, bool) for O00O0000O00 in hidearray)):
                O00O0O0OO00.hidearray = hidearray
            else:
                print('ERROR: parameter need to be list of booleans with the length of the rulelist.')
        else:
            print('ERROR: Provided list has invalid length. You should provide a list with length of the rulelist.')
        pass

    def hide_rule(OO00O0O0OO, rule_id):
        """
        Hides a single rule in result rulelist
        :param int rule_id: rule to hide
        Note that all rules are available to display, this method apply only to print_rulelist(). When iterating over rulelist, <cleverminer>.maskarray should be used
        """
        if OO00O0O0OO.hidearray == None:
            OO00O0O0OO.hidearray = [False] * OO00O0O0OO.get_rulecount()
        if rule_id >= 1 and rule_id <= OO00O0O0OO.get_rulecount():
            OO00O0O0OO.hidearray[rule_id - 1] = True
        else:
            print('WARNING: rule id not is defined range, procedure call will be ignored')

    def unhide_rule(OOOOO00OOO00, rule_id):
        """
        Unhide a single rule in result rulelist
        :param int rule_id: rule to unhide
        Note that all rules are available to display, this method apply only to print_rulelist(). When iterating over rulelist, <cleverminer>.maskarray should be used
        """
        if OOOOO00OOO00.hidearray == None:
            return
        if rule_id >= 1 and rule_id <= OOOOO00OOO00.get_rulecount():
            OOOOO00OOO00.hidearray[rule_id - 1] = False
        else:
            print('WARNING: rule id not is defined range, procedure call will be ignored')

    def reset_hiding(O0OOO000O0O):
        """
        Cancels any rule hiding
        """
        O0OOO000O0O.hidearray = None

    def is_not_hidden(O00000O0OOO, rule_id):
        """
        Returns True if rule is not hidden
        :param int rule_id: id of the rule to decide if it is hidden or not
        """
        return not O00000O0OOO.is_hidden(rule_id)

    def is_hidden(OOO00OO000O0, rule_id):
        """
        Returns True if rule is hidden
        :param int rule_id: id of the rule to decide if it is hidden or not
        """
        if rule_id >= 1 and rule_id <= OOO00OO000O0.get_rulecount():
            if OOO00OO000O0.hidearray is None:
                return False
            else:
                return OOO00OO000O0.hidearray[rule_id - 1]
        else:
            print('WARNING: rule id not is defined range, will return None')
            return None

    def print_summary(O000OOOOOO0O):
        """
        Prints the task processing summary.
        """
        if not O000OOOOOO0O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        print('')
        print('CleverMiner task processing summary:')
        print('')
        print(f"Task type : {O000OOOOOO0O.result['taskinfo']['task_type']}")
        print(f"Number of verifications : {O000OOOOOO0O.result['summary_statistics']['total_verifications']}")
        print(f"Number of rules : {O000OOOOOO0O.result['summary_statistics']['valid_rules']}")
        print(f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O000OOOOOO0O.result['summary_statistics']['time_total']))}")
        if O000OOOOOO0O.verbosity['debug']:
            print(f"Total time needed : {O000OOOOOO0O.result['summary_statistics']['time_total']}")
        print(f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O000OOOOOO0O.result['summary_statistics']['time_prep']))}")
        print(f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O000OOOOOO0O.result['summary_statistics']['time_processing']))}")
        print('')

    def print_hypolist(O0000O00O000):
        """
        Prints the list of rules.
        """
        O0000O00O000.print_rulelist()

    def print_rulelist(O00OO00O00O, sortby=None, storesorted=False):
        """
        Prints the list of rules.
        :param str sortby: name of the quantifier by which output will be sorted
        :param bool storesorted: whether to keep sorted dataframe or not
        """
        if not O00OO00O00O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return

        def get_sortby_parameter(OOO0OO0OOO):
            OO0000O000 = OOO0OO0OOO['params']
            return OO0000O000.get(sortby, 0)
        print('')
        print('List of rules:')
        if O00OO00O00O.result['taskinfo']['task_type'] == '4ftMiner':
            print('RULEID BASE  CONF  AAD    Rule')
        elif O00OO00O00O.result['taskinfo']['task_type'] == 'UICMiner':
            print('RULEID BASE  AAD_SCORE  Rule')
        elif O00OO00O00O.result['taskinfo']['task_type'] == 'CFMiner':
            print('RULEID BASE  S_UP  S_DOWN Condition')
        elif O00OO00O00O.result['taskinfo']['task_type'] == 'SD4ftMiner':
            print('RULEID BASE1 BASE2 RatioConf DeltaConf Rule')
        else:
            print('Unsupported task type for rulelist')
            return
        O000000OO0OO = O00OO00O00O.result['rules']
        if sortby is not None:
            O000000OO0OO = sorted(O000000OO0OO, key=get_sortby_parameter, reverse=True)
            if storesorted:
                O00OO00O00O.result['rules'] = O000000OO0OO
        for O0OO00O0000OO in range(len(O000000OO0OO)):
            O000O00OOOOO0 = O000000OO0OO[O0OO00O0000OO]
            if O00OO00O00O.is_not_hidden(O0OO00O0000OO + 1):
                OO00O0OOO0O = '{:6d}'.format(O000O00OOOOO0['rule_id'])
                if O00OO00O00O.result['taskinfo']['task_type'] == '4ftMiner':
                    if O00OO00O00O.verbosity['debug']:
                        print(f"{O000O00OOOOO0['params']}")
                    OO00O0OOO0O = OO00O0OOO0O + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['base']) + ' ' + '{:.3f}'.format(O000O00OOOOO0['params']['conf']) + ' ' + '{:+.3f}'.format(O000O00OOOOO0['params']['aad'])
                    OO00O0OOO0O = OO00O0OOO0O + ' ' + O000O00OOOOO0['cedents_str']['ante'] + ' => ' + O000O00OOOOO0['cedents_str']['succ'] + ' | ' + O000O00OOOOO0['cedents_str']['cond']
                elif O00OO00O00O.result['taskinfo']['task_type'] == 'UICMiner':
                    OO00O0OOO0O = OO00O0OOO0O + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['base']) + ' ' + '{:.3f}'.format(O000O00OOOOO0['params']['aad_score'])
                    OO00O0OOO0O = OO00O0OOO0O + '     ' + O000O00OOOOO0['cedents_str']['ante'] + ' => ' + O00OO00O00O.result['taskinfo']['target'] + '(*) | ' + O000O00OOOOO0['cedents_str']['cond']
                elif O00OO00O00O.result['taskinfo']['task_type'] == 'CFMiner':
                    OO00O0OOO0O = OO00O0OOO0O + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['base']) + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['s_up']) + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['s_down'])
                    OO00O0OOO0O = OO00O0OOO0O + ' ' + O000O00OOOOO0['cedents_str']['cond']
                elif O00OO00O00O.result['taskinfo']['task_type'] == 'SD4ftMiner':
                    OO00O0OOO0O = OO00O0OOO0O + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['base1']) + ' ' + '{:5d}'.format(O000O00OOOOO0['params']['base2']) + '    ' + '{:.3f}'.format(O000O00OOOOO0['params']['ratioconf']) + '    ' + '{:+.3f}'.format(O000O00OOOOO0['params']['deltaconf'])
                    OO00O0OOO0O = OO00O0OOO0O + '  ' + O000O00OOOOO0['cedents_str']['ante'] + ' => ' + O000O00OOOOO0['cedents_str']['succ'] + ' | ' + O000O00OOOOO0['cedents_str']['cond'] + ' : ' + O000O00OOOOO0['cedents_str']['frst'] + ' x ' + O000O00OOOOO0['cedents_str']['scnd']
                print(OO00O0OOO0O)
        print('')

    def print_hypo(O0O0OO0O000O, rule_id):
        """
        Prints the specified rule to the text output
        :param rule_id: identification of the rule (rule number) to be printed
        """
        O0O0OO0O000O.print_rule(rule_id)

    def print_rule(OO0O0000OOO0, rule_id):
        """
        Prints the specified rule to the text output
        :param rule_id: identification of the rule (rule number) to be printed
        """
        if not OO0O0000OOO0._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        print('')
        if rule_id <= len(OO0O0000OOO0.result['rules']):
            if OO0O0000OOO0.result['taskinfo']['task_type'] == '4ftMiner':
                print('')
                OO000OO00OOO = OO0O0000OOO0.result['rules'][rule_id - 1]
                print(f"Rule id : {OO000OO00OOO['rule_id']}")
                print('')
                print(f"Base : {'{:5d}'.format(OO000OO00OOO['params']['base'])}  Relative base : {'{:.3f}'.format(OO000OO00OOO['params']['rel_base'])}  CONF : {'{:.3f}'.format(OO000OO00OOO['params']['conf'])}  AAD : {'{:+.3f}'.format(OO000OO00OOO['params']['aad'])}  BAD : {'{:+.3f}'.format(OO000OO00OOO['params']['bad'])}")
                print('')
                print('Cedents:')
                print(f"  antecedent : {OO000OO00OOO['cedents_str']['ante']}")
                print(f"  succcedent : {OO000OO00OOO['cedents_str']['succ']}")
                print(f"  condition  : {OO000OO00OOO['cedents_str']['cond']}")
                print('')
                print('Fourfold table')
                print(f'    |  S  |  ¬S |')
                print(f'----|-----|-----|')
                print(f" A  |{'{:5d}'.format(OO000OO00OOO['params']['fourfold'][0])}|{'{:5d}'.format(OO000OO00OOO['params']['fourfold'][1])}|")
                print(f'----|-----|-----|')
                print(f"¬A  |{'{:5d}'.format(OO000OO00OOO['params']['fourfold'][2])}|{'{:5d}'.format(OO000OO00OOO['params']['fourfold'][3])}|")
                print(f'----|-----|-----|')
            elif OO0O0000OOO0.result['taskinfo']['task_type'] == 'CFMiner':
                print('')
                OO000OO00OOO = OO0O0000OOO0.result['rules'][rule_id - 1]
                print(f"Rule id : {OO000OO00OOO['rule_id']}")
                print('')
                O0O00OOOO00 = ''
                if 'aad' in OO000OO00OOO['params']:
                    O0O00OOOO00 = 'aad : ' + str(OO000OO00OOO['params']['aad'])
                print(f"Base : {'{:5d}'.format(OO000OO00OOO['params']['base'])}  Relative base : {'{:.3f}'.format(OO000OO00OOO['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(OO000OO00OOO['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(OO000OO00OOO['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(OO000OO00OOO['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(OO000OO00OOO['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(OO000OO00OOO['params']['max'])}  Histogram minimum : {'{:5d}'.format(OO000OO00OOO['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(OO000OO00OOO['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(OO000OO00OOO['params']['rel_min'])} {O0O00OOOO00}")
                print('')
                print(f"Condition  : {OO000OO00OOO['cedents_str']['cond']}")
                print('')
                OO0OO000O00O = OO0O0000OOO0.get_category_names(OO0O0000OOO0.result['taskinfo']['target'])
                print(f'Categories in target variable  {OO0OO000O00O}')
                print(f"Histogram                      {OO000OO00OOO['params']['hist']}")
                if 'aad' in OO000OO00OOO['params']:
                    print(f"Histogram on full set          {OO000OO00OOO['params']['hist_full']}")
                    print(f"Relative histogram             {OO000OO00OOO['params']['rel_hist']}")
                    print(f"Relative histogram on full set {OO000OO00OOO['params']['rel_hist_full']}")
            elif OO0O0000OOO0.result['taskinfo']['task_type'] == 'UICMiner':
                print('')
                OO000OO00OOO = OO0O0000OOO0.result['rules'][rule_id - 1]
                print(f"Rule id : {OO000OO00OOO['rule_id']}")
                print('')
                O0O00OOOO00 = ''
                if 'aad_score' in OO000OO00OOO['params']:
                    O0O00OOOO00 = 'aad score : ' + str(OO000OO00OOO['params']['aad_score'])
                print(f"Base : {'{:5d}'.format(OO000OO00OOO['params']['base'])}  Relative base : {'{:.3f}'.format(OO000OO00OOO['params']['rel_base'])}   {O0O00OOOO00}")
                print('')
                print(f"Condition  : {OO000OO00OOO['cedents_str']['cond']}")
                print(f"Antecedent : {OO000OO00OOO['cedents_str']['ante']}")
                print('')
                print(f"Histogram                                        {OO000OO00OOO['params']['hist']}")
                if 'aad_score' in OO000OO00OOO['params']:
                    print(f"Histogram on full set with condition             {OO000OO00OOO['params']['hist_cond']}")
                    print(f"Relative histogram                               {OO000OO00OOO['params']['rel_hist']}")
                    print(f"Relative histogram on full set with condition    {OO000OO00OOO['params']['rel_hist_cond']}")
                OOO000OO00OOO = OO0O0000OOO0.result['datalabels']['catnames'][OO0O0000OOO0.result['datalabels']['varname'].index(OO0O0000OOO0.result['taskinfo']['target'])]
                print(' ')
                print('Interpretation:')
                for OOOOOOOOO00O in range(len(OOO000OO00OOO)):
                    O0OO0O000OO0 = 0
                    if OO000OO00OOO['params']['rel_hist'][OOOOOOOOO00O] > 0:
                        O0OO0O000OO0 = OO000OO00OOO['params']['rel_hist'][OOOOOOOOO00O] / OO000OO00OOO['params']['rel_hist_cond'][OOOOOOOOO00O]
                    OOO0O00O0OO0O = ''
                    if not OO000OO00OOO['cedents_str']['cond'] == '---':
                        OOO0O00O0OO0O = 'For ' + OO000OO00OOO['cedents_str']['cond'] + ': '
                    print(f"    {OOO0O00O0OO0O}{OO0O0000OOO0.result['taskinfo']['target']}({OOO000OO00OOO[OOOOOOOOO00O]}) has occurence {'{:.1%}'.format(OO000OO00OOO['params']['rel_hist_cond'][OOOOOOOOO00O])}, with antecedent it has occurence {'{:.1%}'.format(OO000OO00OOO['params']['rel_hist'][OOOOOOOOO00O])}, that is {'{:.3f}'.format(O0OO0O000OO0)} times more.")
            elif OO0O0000OOO0.result['taskinfo']['task_type'] == 'SD4ftMiner':
                print('')
                OO000OO00OOO = OO0O0000OOO0.result['rules'][rule_id - 1]
                print(f"Rule id : {OO000OO00OOO['rule_id']}")
                print('')
                print(f"Base1 : {'{:5d}'.format(OO000OO00OOO['params']['base1'])} Base2 : {'{:5d}'.format(OO000OO00OOO['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(OO000OO00OOO['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(OO000OO00OOO['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(OO000OO00OOO['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(OO000OO00OOO['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(OO000OO00OOO['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(OO000OO00OOO['params']['ratioconf'])}")
                print('')
                print('Cedents:')
                print(f"  antecedent : {OO000OO00OOO['cedents_str']['ante']}")
                print(f"  succcedent : {OO000OO00OOO['cedents_str']['succ']}")
                print(f"  condition  : {OO000OO00OOO['cedents_str']['cond']}")
                print(f"  first set  : {OO000OO00OOO['cedents_str']['frst']}")
                print(f"  second set : {OO000OO00OOO['cedents_str']['scnd']}")
                print('')
                print('Fourfold tables:')
                print(f'FRST|  S  |  ¬S |  SCND|  S  |  ¬S |')
                print(f'----|-----|-----|  ----|-----|-----| ')
                print(f" A  |{'{:5d}'.format(OO000OO00OOO['params']['fourfold1'][0])}|{'{:5d}'.format(OO000OO00OOO['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(OO000OO00OOO['params']['fourfold2'][0])}|{'{:5d}'.format(OO000OO00OOO['params']['fourfold2'][1])}|")
                print(f'----|-----|-----|  ----|-----|-----|')
                print(f"¬A  |{'{:5d}'.format(OO000OO00OOO['params']['fourfold1'][2])}|{'{:5d}'.format(OO000OO00OOO['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(OO000OO00OOO['params']['fourfold2'][2])}|{'{:5d}'.format(OO000OO00OOO['params']['fourfold2'][3])}|")
                print(f'----|-----|-----|  ----|-----|-----|')
            else:
                print('Unsupported task type for rule details')
            print('')
        else:
            print('No such rule.')

    def get_ruletext(OOOOO00O000, rule_id):
        """
        Gets text for the rule. Can be used in further processing.
        :param int rule_id: identification of the rule (rule number)
        :return: text for the specified rule
        :rtype: str
        """
        if not OOOOO00O000._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= 0 or rule_id > OOOOO00O000.get_rulecount():
            if OOOOO00O000.get_rulecount() == 0:
                print('No such rule. There are no rules in result.')
            else:
                print(f'No such rule ({rule_id}). Available rules are 1 to {OOOOO00O000.get_rulecount()}')
            return None
        OOO00000OO00O = ''
        O0000O00O0 = OOOOO00O000.result['rules'][rule_id - 1]
        if OOOOO00O000.result['taskinfo']['task_type'] == '4ftMiner':
            OOO00000OO00O = OOO00000OO00O + ' ' + O0000O00O0['cedents_str']['ante'] + ' => ' + O0000O00O0['cedents_str']['succ'] + ' | ' + O0000O00O0['cedents_str']['cond']
        elif OOOOO00O000.result['taskinfo']['task_type'] == 'UICMiner':
            OOO00000OO00O = OOO00000OO00O + '     ' + O0000O00O0['cedents_str']['ante'] + ' => ' + OOOOO00O000.result['taskinfo']['target'] + '(*) | ' + O0000O00O0['cedents_str']['cond']
        elif OOOOO00O000.result['taskinfo']['task_type'] == 'CFMiner':
            OOO00000OO00O = OOO00000OO00O + ' ' + O0000O00O0['cedents_str']['cond']
        elif OOOOO00O000.result['taskinfo']['task_type'] == 'SD4ftMiner':
            OOO00000OO00O = OOO00000OO00O + '  ' + O0000O00O0['cedents_str']['ante'] + ' => ' + O0000O00O0['cedents_str']['succ'] + ' | ' + O0000O00O0['cedents_str']['cond'] + ' : ' + O0000O00O0['cedents_str']['frst'] + ' x ' + O0000O00O0['cedents_str']['scnd']
        return OOO00000OO00O

    def _annotate_chart(OOOOOO0O00, O0O0OOOOO000O, O00000OOOO00, O0OOO0O0OO0O=2):
        O000000O0O00O = O0O0OOOOO000O.axes.get_ylim()
        for OO0O00O00O in O0O0OOOOO000O.patches:
            OOO00O0O0O = '{:.1f}%'.format(100 * OO0O00O00O.get_height() / O00000OOOO00)
            OOO0000OOOO0O = OO0O00O00O.get_x() + OO0O00O00O.get_width() / 4
            OO0000OO0OO0 = OO0O00O00O.get_y() + OO0O00O00O.get_height() - O000000O0O00O[1] / 8
            if OO0O00O00O.get_height() < O000000O0O00O[1] / 8:
                OO0000OO0OO0 = OO0O00O00O.get_y() + OO0O00O00O.get_height() + O000000O0O00O[1] * 0.02
            O0O0OOOOO000O.annotate(OOO00O0O0O, (OOO0000OOOO0O, OO0000OO0OO0), size=23 / O0OOO0O0OO0O)

    def draw_rule(OOO0O00OOOO, rule_id, show=True, filename=None):
        """
        Show illustration chart for the specified rule.
        :param int rule_id: identification of the rule (rule number) to be shown
        :param bool show: whether to show chart to graphical output or not
        :param str filename: if specified, chart will be saved into this filename
        """
        if not OOO0O00OOOO._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        print('')
        if rule_id <= len(OOO0O00OOOO.result['rules']):
            if OOO0O00OOOO.result['taskinfo']['task_type'] == '4ftMiner':
                O00O0O0O000, OO0OO000O00OO = plt.subplots(2, 2)
                OO0000O0O0 = ['S', 'not S']
                OOOOOOO0O0 = ['A', 'not A']
                O0O0OOOOO0 = OOO0O00OOOO.get_fourfold(rule_id)
                O0OO00OOO0O00 = [O0O0OOOOO0[0], O0O0OOOOO0[1]]
                O00000OO0OO0 = [O0O0OOOOO0[2], O0O0OOOOO0[3]]
                OOO00000O0O = [O0O0OOOOO0[0] + O0O0OOOOO0[2], O0O0OOOOO0[1] + O0O0OOOOO0[3]]
                OO0OO000O00OO[0, 0] = sns.barplot(ax=OO0OO000O00OO[0, 0], x=OO0000O0O0, y=O0OO00OOO0O00, color='lightsteelblue')
                OOO0O00OOOO._annotate_chart(OO0OO000O00OO[0, 0], O0O0OOOOO0[0] + O0O0OOOOO0[1])
                OO0OO000O00OO[0, 1] = sns.barplot(ax=OO0OO000O00OO[0, 1], x=OO0000O0O0, y=OOO00000O0O, color='gray', edgecolor='black')
                OOO0O00OOOO._annotate_chart(OO0OO000O00OO[0, 1], sum(O0O0OOOOO0))
                OO0OO000O00OO[0, 0].set(xlabel=None, ylabel='Count')
                OO0OO000O00OO[0, 1].set(xlabel=None, ylabel='Count')
                O0OO0OOO0O = sns.color_palette('Blues', as_cmap=True)
                OO0OOOO0000 = sns.color_palette('Greys', as_cmap=True)
                OO0OO000O00OO[1, 0] = sns.heatmap(ax=OO0OO000O00OO[1, 0], data=[O0OO00OOO0O00, O00000OO0OO0], xticklabels=OO0000O0O0, yticklabels=OOOOOOO0O0, annot=True, cbar=False, fmt='.0f', cmap=O0OO0OOO0O)
                OO0OO000O00OO[1, 0].set(xlabel=None, ylabel='Count')
                OO0OO000O00OO[1, 1] = sns.heatmap(ax=OO0OO000O00OO[1, 1], data=np.asarray([OOO00000O0O]), xticklabels=OO0000O0O0, yticklabels=False, annot=True, cbar=False, fmt='.0f', cmap=OO0OOOO0000)
                OO0OO000O00OO[1, 1].set(xlabel=None, ylabel='Count')
                O00OOO00OO0 = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']['ante']
                OO0OO000O00OO[0, 0].set(title='\n'.join(wrap(O00OOO00OO0, 30)))
                OO0OO000O00OO[0, 1].set(title='Entire dataset')
                O00000O000O = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']
                O00O0O0O000.suptitle('Antecedent : ' + O00000O000O['ante'] + '\nSuccedent : ' + O00000O000O['succ'] + '\nCondition : ' + O00000O000O['cond'], x=0, ha='left', size='small')
                O00O0O0O000.tight_layout()
            elif OOO0O00OOOO.result['taskinfo']['task_type'] == 'SD4ftMiner':
                O00O0O0O000, OO0OO000O00OO = plt.subplots(2, 2)
                OO0000O0O0 = ['S', 'not S']
                OOOOOOO0O0 = ['A', 'not A']
                O0O00O0OOO0OO = OOO0O00OOOO.get_fourfold(rule_id, order=1)
                OO0OO0OO0O00 = OOO0O00OOOO.get_fourfold(rule_id, order=2)
                O000O00O0O = [O0O00O0OOO0OO[0], O0O00O0OOO0OO[1]]
                OOO0000O0OO0 = [O0O00O0OOO0OO[2], O0O00O0OOO0OO[3]]
                OO000O00O00O = [O0O00O0OOO0OO[0] + O0O00O0OOO0OO[2], O0O00O0OOO0OO[1] + O0O00O0OOO0OO[3]]
                OOOOOO0O00OO0 = [OO0OO0OO0O00[0], OO0OO0OO0O00[1]]
                O0O0OO0O00O = [OO0OO0OO0O00[2], OO0OO0OO0O00[3]]
                O0O0O00O0O0O = [OO0OO0OO0O00[0] + OO0OO0OO0O00[2], OO0OO0OO0O00[1] + OO0OO0OO0O00[3]]
                OO0OO000O00OO[0, 0] = sns.barplot(ax=OO0OO000O00OO[0, 0], x=OO0000O0O0, y=O000O00O0O, color='orange')
                OOO0O00OOOO._annotate_chart(OO0OO000O00OO[0, 0], O0O00O0OOO0OO[0] + O0O00O0OOO0OO[1])
                OO0OO000O00OO[0, 1] = sns.barplot(ax=OO0OO000O00OO[0, 1], x=OO0000O0O0, y=OOOOOO0O00OO0, color='green')
                OOO0O00OOOO._annotate_chart(OO0OO000O00OO[0, 1], OO0OO0OO0O00[0] + OO0OO0OO0O00[1])
                OO0OO000O00OO[0, 0].set(xlabel=None, ylabel='Count')
                OO0OO000O00OO[0, 1].set(xlabel=None, ylabel='Count')
                O0OO0OOO0O = sns.color_palette('Oranges', as_cmap=True)
                OO0OOOO0000 = sns.color_palette('Greens', as_cmap=True)
                OO0OO000O00OO[1, 0] = sns.heatmap(ax=OO0OO000O00OO[1, 0], data=[O000O00O0O, OOO0000O0OO0], xticklabels=OO0000O0O0, yticklabels=OOOOOOO0O0, annot=True, cbar=False, fmt='.0f', cmap=O0OO0OOO0O)
                OO0OO000O00OO[1, 0].set(xlabel=None, ylabel='Count')
                OO0OO000O00OO[1, 1] = sns.heatmap(ax=OO0OO000O00OO[1, 1], data=[OOOOOO0O00OO0, O0O0OO0O00O], xticklabels=OO0000O0O0, yticklabels=False, annot=True, cbar=False, fmt='.0f', cmap=OO0OOOO0000)
                OO0OO000O00OO[1, 1].set(xlabel=None, ylabel='Count')
                O00OOO00OO0 = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']['frst']
                OO0OO000O00OO[0, 0].set(title='\n'.join(wrap(O00OOO00OO0, 30)))
                O0OOOOOOO0 = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']['scnd']
                OO0OO000O00OO[0, 1].set(title='\n'.join(wrap(O0OOOOOOO0, 30)))
                O00000O000O = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']
                O00O0O0O000.suptitle('Antecedent : ' + O00000O000O['ante'] + '\nSuccedent : ' + O00000O000O['succ'] + '\nCondition : ' + O00000O000O['cond'] + '\nFirst : ' + O00000O000O['frst'] + '\nSecond : ' + O00000O000O['scnd'], x=0, ha='left', size='small')
                O00O0O0O000.tight_layout()
            elif OOO0O00OOOO.result['taskinfo']['task_type'] == 'CFMiner' or OOO0O00OOOO.result['taskinfo']['task_type'] == 'UICMiner':
                O000OO0OO0O = OOO0O00OOOO.result['taskinfo']['task_type'] == 'UICMiner'
                O00O0O0O000, OO0OO000O00OO = plt.subplots(2, 2, gridspec_kw={'height_ratios': [3, 1]})
                O0OO0OO00O00O = OOO0O00OOOO.result['taskinfo']['target']
                OO0000O0O0 = OOO0O00OOOO.result['datalabels']['catnames'][OOO0O00OOOO.result['datalabels']['varname'].index(OOO0O00OOOO.result['taskinfo']['target'])]
                O0O00O0OOOO00 = OOO0O00OOOO.result['rules'][rule_id - 1]
                OO00O00O0OO = OOO0O00OOOO.get_hist(rule_id)
                if O000OO0OO0O:
                    OO00O00O0OO = O0O00O0OOOO00['params']['hist']
                else:
                    OO00O00O0OO = OOO0O00OOOO.get_hist(rule_id)
                OO0OO000O00OO[0, 0] = sns.barplot(ax=OO0OO000O00OO[0, 0], x=OO0000O0O0, y=OO00O00O0OO, color='lightsteelblue')
                O000O0O000OOO = []
                O0O0OO0OO0OO = []
                if O000OO0OO0O:
                    O000O0O000OOO = OO0000O0O0
                    O0O0OO0OO0OO = OOO0O00OOOO.get_hist(rule_id, fullCond=True)
                else:
                    O000O0O000OOO = OOO0O00OOOO.profiles['hist_target_entire_dataset_labels']
                    O0O0OO0OO0OO = OOO0O00OOOO.profiles['hist_target_entire_dataset_values']
                OO0OO000O00OO[0, 1] = sns.barplot(ax=OO0OO000O00OO[0, 1], x=O000O0O000OOO, y=O0O0OO0OO0OO, color='gray', edgecolor='black')
                OOO0O00OOOO._annotate_chart(OO0OO000O00OO[0, 0], sum(OO00O00O0OO), len(OO00O00O0OO))
                OOO0O00OOOO._annotate_chart(OO0OO000O00OO[0, 1], sum(O0O0OO0OO0OO), len(O0O0OO0OO0OO))
                OO0OO000O00OO[0, 0].set(xlabel=None, ylabel='Count')
                OO0OO000O00OO[0, 1].set(xlabel=None, ylabel='Count')
                OOO0O0O000O = [OO0000O0O0, OO00O00O0OO]
                OO00000000 = pd.DataFrame(OOO0O0O000O).transpose()
                OO00000000.columns = [O0OO0OO00O00O, 'No of observatios']
                O0OO0OOO0O = sns.color_palette('Blues', as_cmap=True)
                OO0OOOO0000 = sns.color_palette('Greys', as_cmap=True)
                OO0OO000O00OO[1, 0] = sns.heatmap(ax=OO0OO000O00OO[1, 0], data=np.asarray([OO00O00O0OO]), xticklabels=OO0000O0O0, yticklabels=False, annot=True, cbar=False, fmt='.0f', cmap=O0OO0OOO0O)
                OO0OO000O00OO[1, 0].set(xlabel=O0OO0OO00O00O, ylabel='Count')
                OO0OO000O00OO[1, 1] = sns.heatmap(ax=OO0OO000O00OO[1, 1], data=np.asarray([O0O0OO0OO0OO]), xticklabels=O000O0O000OOO, yticklabels=False, annot=True, cbar=False, fmt='.0f', cmap=OO0OOOO0000)
                OO0OO000O00OO[1, 1].set(xlabel=O0OO0OO00O00O, ylabel='Count')
                O00OO0OO0OOO0 = ''
                O0OO0OOOO000 = 'Entire dataset'
                if O000OO0OO0O:
                    if len(O0O00O0OOOO00['cedents_struct']['cond']) > 0:
                        O0OO0OOOO000 = O0O00O0OOOO00['cedents_str']['cond']
                        O00OO0OO0OOO0 = ' & ' + O0O00O0OOOO00['cedents_str']['cond']
                OO0OO000O00OO[0, 1].set(title=O0OO0OOOO000)
                if O000OO0OO0O:
                    O00OOO00OO0 = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']['ante'] + O00OO0OO0OOO0
                else:
                    O00OOO00OO0 = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']['cond']
                OO0OO000O00OO[0, 0].set(title='\n'.join(wrap(O00OOO00OO0, 30)))
                O00000O000O = OOO0O00OOOO.result['rules'][rule_id - 1]['cedents_str']
                O0OO0OOOO000 = 'Condition : ' + O00000O000O['cond']
                if O000OO0OO0O:
                    O0OO0OOOO000 = O0OO0OOOO000 + '\nAntecedent : ' + O00000O000O['ante']
                O00O0O0O000.suptitle(O0OO0OOOO000, x=0, ha='left', size='small')
                O00O0O0O000.tight_layout()
            else:
                print('Unsupported task type for rule details')
                return
            if filename is not None:
                plt.savefig(filename=filename)
            if show:
                plt.show()
            print('')
        else:
            print('No such rule.')

    def get_rulecount(OOO0O000OO0O, not_hidden_only=False):
        """
        Gets number of rules.
        :return: number of rules in the resultset
        :rtype: int
        """
        if not OOO0O000OO0O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if not_hidden_only:
            if OOO0O000OO0O.hidearray == None:
                return len(OOO0O000OO0O.result['rules'])
            else:
                return sum((not bool(O0O00000O00) for O0O00000O00 in OOO0O000OO0O.hidearray))
        return len(OOO0O000OO0O.result['rules'])

    def get_fourfold(O0OO000O0O, rule_id, order=0):
        """
        Gets a fourfold table for a specified rule.
        :param int rule_id: identification of the rule (rule number)
        :param int order: order of the fourfold table to be returned where more than one fourfold table is available (used for SD4ft-Miner, possible values are 1 and 2)
        :return: fourfold table as array of four integers
        :rtype: list
        """
        if not O0OO000O0O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= len(O0OO000O0O.result['rules']):
            if O0OO000O0O.result['taskinfo']['task_type'] == '4ftMiner':
                OO000OO0O0OOO = O0OO000O0O.result['rules'][rule_id - 1]
                return OO000OO0O0OOO['params']['fourfold']
            elif O0OO000O0O.result['taskinfo']['task_type'] == 'CFMiner':
                print('Error: fourfold for CFMiner is not defined')
                return None
            elif O0OO000O0O.result['taskinfo']['task_type'] == 'SD4ftMiner':
                OO000OO0O0OOO = O0OO000O0O.result['rules'][rule_id - 1]
                if order == 1:
                    return OO000OO0O0OOO['params']['fourfold1']
                if order == 2:
                    return OO000OO0O0OOO['params']['fourfold2']
                print('Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).')
                return None
            else:
                print('Unsupported task type for rule details')
        else:
            print('No such rule.')

    def get_hist(OO00O0O0OOO0O, rule_id, fullCond=True):
        """
        Gets a histogram for the specified rule.
        :param int rule_id: identification of the rule (rule number)
        :param bool fullCond: (applicable for UIC Miner only) when True, show full histogram (given only by condition), when False, histogram given by condition and antecedent is shown
        :return: histogram as array of integers with length of unique values of the target variable
        :rtype: list
        """
        if not OO00O0O0OOO0O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= len(OO00O0O0OOO0O.result['rules']):
            if OO00O0O0OOO0O.result['taskinfo']['task_type'] == 'CFMiner':
                OOO00O00OOO00 = OO00O0O0OOO0O.result['rules'][rule_id - 1]
                return OOO00O00OOO00['params']['hist']
            elif OO00O0O0OOO0O.result['taskinfo']['task_type'] == 'UICMiner':
                OOO00O00OOO00 = OO00O0O0OOO0O.result['rules'][rule_id - 1]
                OOO0OO00O00O = None
                if fullCond:
                    OOO0OO00O00O = OOO00O00OOO00['params']['hist_cond']
                else:
                    OOO0OO00O00O = OOO00O00OOO00['params']['hist']
                return OOO0OO00O00O
            elif OO00O0O0OOO0O.result['taskinfo']['task_type'] == 'SD4ftMiner':
                print('Error: SD4ft-Miner has no histogram')
                return None
            elif OO00O0O0OOO0O.result['taskinfo']['task_type'] == '4ftMiner':
                print('Error: 4ft-Miner has no histogram')
                return None
            else:
                print('Unsupported task type for rule details')
        else:
            print('No such rule.')

    def get_hist_cond(O00O0O0000, rule_id):
        """
        Gets a histogram on a full dataset (given by condition in case of UIC Miner)
        :param rule_id: identification of the rule (rule number)
        :return: histogram as array of integers with length of unique values of the target variable
        :rtype: list
        """
        if not O00O0O0000._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= len(O00O0O0000.result['rules']):
            if O00O0O0000.result['taskinfo']['task_type'] == 'UICMiner':
                OOO0O0O0000 = O00O0O0000.result['rules'][rule_id - 1]
                return OOO0O0O0000['params']['hist_cond']
            elif O00O0O0000.result['taskinfo']['task_type'] == 'CFMiner':
                OOO0O0O0000 = O00O0O0000.result['rules'][rule_id - 1]
                return OOO0O0O0000['params']['hist']
            elif O00O0O0000.result['taskinfo']['task_type'] == 'SD4ftMiner':
                print('Error: SD4ft-Miner has no histogram')
                return None
            elif O00O0O0000.result['taskinfo']['task_type'] == '4ftMiner':
                print('Error: 4ft-Miner has no histogram')
                return None
            else:
                print('Unsupported task type for rule details')
        else:
            print('No such rule.')

    def get_quantifiers(OOOO0OOO0O0, rule_id, order=0):
        """
        Gets a list of all quantifiers available for the rule


        :param int rule_id: identification of the rule (rule number)
        :param int order: (depreciated; kept for compatibility for a limited time)
        :return: dictionary with quantifiers and their values
        :rtype: list
        """
        if not OOOO0OOO0O0._is_calculated():
            print('ERROR: Task has not been calculated.')
            return None
        if rule_id <= len(OOOO0OOO0O0.result['rules']):
            O0O0OOOOOOO = OOOO0OOO0O0.result['rules'][rule_id - 1]
            if OOOO0OOO0O0.result['taskinfo']['task_type'] == '4ftMiner':
                return O0O0OOOOOOO['params']
            elif OOOO0OOO0O0.result['taskinfo']['task_type'] == 'CFMiner':
                return O0O0OOOOOOO['params']
            elif OOOO0OOO0O0.result['taskinfo']['task_type'] == 'SD4ftMiner':
                return O0O0OOOOOOO['params']
            else:
                print('Unsupported task type for rule details')
        else:
            print('No such rule.')

    def get_varlist(O0O00O00OO000):
        """
        Gets a list of variables in the processed dataset
        :return [str]: array of variable names
        """
        return O0O00O00OO000.result['datalabels']['varname']

    def get_category_names(OOO0O0O000OO0, varname=None, varindex=None):
        """
        Gets a list of category names for a required variable. The variable can be specified either by name or the index in variable list. Either varname or varindex must be specified.
        :param str varname: name of the variable
        :param int varindex: index of the variable
        :return: list of category names for a required variable
        :rtype: list
        """
        OOOO0OO0000 = 0
        if varindex is not None:
            if OOOO0OO0000 >= 0 & OOOO0OO0000 < len(OOO0O0O000OO0.get_varlist()):
                OOOO0OO0000 = varindex
            else:
                print('Error: no such variable.')
                return
        if varname is not None:
            OOOOOOO0000O = OOO0O0O000OO0.get_varlist()
            OOOO0OO0000 = OOOOOOO0000O.index(varname)
            if OOOO0OO0000 == -1 | OOOO0OO0000 < 0 | OOOO0OO0000 >= len(OOO0O0O000OO0.get_varlist()):
                print('Error: no such variable.')
                return
        return OOO0O0O000OO0.result['datalabels']['catnames'][OOOO0OO0000]

    def print_data_definition(O00000OO00):
        """
        Prints how CleverMiner understands categorical pandas dataset to be processed. Shows a list of variabes with number of categories for each variable.
        """
        OO0OOOO0OO = O00000OO00.get_varlist()
        print(f'Dataset has {len(OO0OOOO0OO)} variables.')
        for OOO00OO0O00 in OO0OOOO0OO:
            OO0OO00O000OO = O00000OO00.get_category_names(OOO00OO0O00)
            O0OOOOO0O0 = ''
            for O00O0O0O00OO in OO0OO00O000OO:
                O0OOOOO0O0 = O0OOOOO0O0 + str(O00O0O0O00OO) + ' '
            O0OOOOO0O0 = O0OOOOO0O0[:-1]
            print(f'Variable {OOO00OO0O00} has {len(OO0OO00O000OO)} categories: {O0OOOOO0O0}')

    def _is_calculated(OO0O0OO000):
        O0O00O000O00O = False
        if 'taskinfo' in OO0O0OO000.result:
            O0O00O000O00O = True
        return O0O00O000O00O

    def save(O000OO0000, fname, savedata=False, embeddata=True, fmt='pickle'):
        if not O000OO0000._is_calculated():
            print('ERROR: Task has not been calculated.')
            return None
        OOO0OOO00000O = {'program': 'CleverMiner', 'version': O000OO0000.get_version_string()}
        OO000O0000O = {}
        OO000O0000O['control'] = OOO0OOO00000O
        OO000O0000O['result'] = O000OO0000.result
        OO000O0000O['stats'] = O000OO0000.stats
        OO000O0000O['options'] = O000OO0000.options
        OO000O0000O['profiles'] = O000OO0000.profiles
        if savedata:
            if embeddata:
                OO000O0000O['data'] = O000OO0000.data
                OO000O0000O['df'] = O000OO0000.df
            else:
                O0000OOO0O = {}
                O0000OOO0O['data'] = O000OO0000.data
                O0000OOO0O['df'] = O000OO0000.df
                print(f'CALC HASH {datetime.now()}')
                O000O0O0000O0 = O000OO0000._get_fast_hash(O0000OOO0O)
                print(f'CALC HASH ...done {datetime.now()}')
                OO00O00000OO0 = os.path.join(O000OO0000.cache_dir, O000O0O0000O0 + '.clmdata')
                O00O0O00OO0 = open(OO00O00000OO0, 'wb')
                pickle.dump(O0000OOO0O, O00O0O00OO0, protocol=pickle.HIGHEST_PROTOCOL)
                OO000O0000O['datafile'] = OO00O00000OO0
        if fmt == 'pickle':
            OO000OO00OO00 = open(fname, 'wb')
            pickle.dump(OO000O0000O, OO000OO00OO00, protocol=pickle.HIGHEST_PROTOCOL)
        elif fmt == 'json':
            OO000OO00OO00 = open(fname, 'w')
            json.dump(OO000O0000O, OO000OO00OO00)
        else:
            print(f'Unsupported format - {fmt}. Supported formats are pickle, json.')

    def load(OO00O00OOO, filename, fmt='pickle'):
        OOO0OOO00OOOO = False
        if '://' in filename:
            OOO0OOO00OOOO = True
        if fmt == 'pickle':
            if OOO0OOO00OOOO:
                OO0O0OOO00 = pickle.load(urllib.request.urlopen(filename))
            else:
                O000O0OOOOOOO = open(filename, 'rb')
                OO0O0OOO00 = pickle.load(O000O0OOOOOOO)
        elif fmt == 'json':
            if OOO0OOO00OOOO:
                OO0O0OOO00 = json.load(urllib.request.urlopen(filename))
            else:
                O000O0OOOOOOO = open(filename, 'r')
                OO0O0OOO00 = json.load(O000O0OOOOOOO)
        else:
            print(f'Unsupported format - {fmt}. Supported formats are pickle, json.')
            return
        if not 'control' in OO0O0OOO00:
            print('Error: not a CleverMiner save file (1)')
            return None
        OOOO0OO0OO00O = OO0O0OOO00['control']
        if not 'program' in OOOO0OO0OO00O or not 'version' in OOOO0OO0OO00O:
            print('Error: not a CleverMiner save file (2)')
            return None
        if not OOOO0OO0OO00O['program'] == 'CleverMiner':
            print('Error: not a CleverMiner save file (3)')
            return None
        OO00O00OOO.result = OO0O0OOO00['result']
        OO00O00OOO.stats = OO0O0OOO00['stats']
        OO00O00OOO.options = OO0O0OOO00['options']
        if 'profiles' in OO0O0OOO00:
            OO00O00OOO.profiles = OO0O0OOO00['profiles']
        if 'data' in OO0O0OOO00:
            OO00O00OOO.data = OO0O0OOO00['data']
            OO00O00OOO.OOOOOOO0OOOO0 = True
        if 'df' in OO0O0OOO00:
            OO00O00OOO.df = OO0O0OOO00['df']
        if 'datafile' in OO0O0OOO00:
            try:
                O0OO00OOOOO = open(OO0O0OOO00['datafile'], 'rb')
                O00O000000 = pickle.load(O0OO00OOOOO)
                OO00O00OOO.data = O00O000000['data']
                OO00O00OOO.df = O00O000000['df']
                print(f"...data loaded from file {OO0O0OOO00['datafile']}.")
            except:
                print(f'Error loading saved file. Linked data file does not exists or it is in incorrect structure or path. If you are transferring saved file to another computer, please embed also data.')
                exit(1)
        print(f'File {filename} loaded ok.')

    def get_version_string(OOO0O00000O00):
        """
        Gets a version string for CleverMiner package.

        :return str: version number
        """
        return OOO0O00000O00.version_string

    def get_rule_cedent_list(O0OO00O00OO00, rule_id):
        """
        Gets list of cedents used in the rule. Can be used in further processing.
        :param int rule_id: identification of the rule (rule number)
        :return: list of cedents for the specified rule
        :rtype: list[str]
        """
        if not O0OO00O00OO00._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= 0 or rule_id > O0OO00O00OO00.get_rulecount():
            if O0OO00O00OO00.get_rulecount() == 0:
                print('No such rule. There are no rules in result.')
            else:
                print(f'No such rule ({rule_id}). Available rules are 1 to {O0OO00O00OO00.get_rulecount()}')
            return None
        O00OOOO000O = []
        O0O0OOOO00 = O0OO00O00OO00.result['rules'][rule_id - 1]
        O00OOOO000O = list(O0O0OOOO00['trace_cedent_dataorder'].keys())
        return O00OOOO000O

    def get_rule_variables(OOOOO0OOOOO0, rule_id, cedent, get_names=True):
        """
        Gets list of variables in a specified cedent used in the rule. Can be used in further processing.
        :param int rule_id: identification of the rule (rule number)
        :param str cedent: identification of the cedent
        :param bool get_names: if True, return names, if False, return indices
        :return: list of variables for a specified cedent in the specified rule
        :rtype: list[str] / list[int]
        """
        if not OOOOO0OOOOO0._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= 0 or rule_id > OOOOO0OOOOO0.get_rulecount():
            if OOOOO0OOOOO0.get_rulecount() == 0:
                print('No such rule. There are no rules in result.')
            else:
                print(f'No such rule ({rule_id}). Available rules are 1 to {OOOOO0OOOOO0.get_rulecount()}')
            return None
        OOO00O0000 = []
        OOOOO0000O = OOOOO0OOOOO0.result['rules'][rule_id - 1]
        O0OOOO0O0OOO = OOOOO0OOOOO0.result['datalabels']['varname']
        if not cedent in OOOOO0000O['trace_cedent_dataorder']:
            print(f'ERROR: cedent {cedent} not in result.')
            exit(1)
        for O0OO0OO0O0 in OOOOO0000O['trace_cedent_dataorder'][cedent]:
            if get_names:
                OOO00O0000.append(O0OOOO0O0OOO[O0OO0OO0O0])
            else:
                OOO00O0000.append(O0OO0OO0O0)
        return OOO00O0000

    def get_rule_categories(O00000O00O0OO, rule_id, cedent, variable, get_names=True):
        """
        Gets list of categories for a specified cedent in the rule. Can be used in further processing.
        :param int rule_id: identification of the rule (rule number)
        :param str cedent: identification of the cedent
        :param str variable: identification of the variable
        :param bool get_names: if True, return names, if False, return indices
        :return: list of categories for a specified variable in specified cedent of the specified rule
        :rtype: list[str] / list[int]
        """
        if not O00000O00O0OO._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        if rule_id <= 0 or rule_id > O00000O00O0OO.get_rulecount():
            if O00000O00O0OO.get_rulecount() == 0:
                print('No such rule. There are no rules in result.')
            else:
                print(f'No such rule ({rule_id}). Available rules are 1 to {O00000O00O0OO.get_rulecount()}')
            return None
        OO000000OOO0 = []
        O0OO0OOOO0O0 = O00000O00O0OO.result['rules'][rule_id - 1]
        OO0000O0OOO00 = O00000O00O0OO.result['datalabels']['varname']
        if variable in OO0000O0OOO00:
            OO00O00OOO0 = OO0000O0OOO00.index(variable)
            OO0O0O00O00OO = O00000O00O0OO.result['datalabels']['catnames'][OO00O00OOO0]
            if not cedent in O0OO0OOOO0O0['trace_cedent_dataorder']:
                print(f'ERROR: cedent {cedent} not in result.')
                exit(1)
            OO0OO0OOOO0OO = O0OO0OOOO0O0['trace_cedent_dataorder'][cedent].index(OO00O00OOO0)
            for O00OO00OO00OO in O0OO0OOOO0O0['traces'][cedent][OO0OO0OOOO0OO]:
                if get_names:
                    OO000000OOO0.append(OO0O0O00O00OO[O00OO00OO00OO])
                else:
                    OO000000OOO0.append(O00OO00OO00OO)
        else:
            print(f'ERROR: variable not found: {cedent},{variable}. Possible variables are {OO0000O0OOO00}')
            exit(1)
        return OO000000OOO0

    def get_dataset_variable_count(O00OO0OO0O):
        """
        Gets count of variables in the dataset. Can be used in further processing.
        :return: count of variables in the dataset
        :rtype: int
        """
        if not O00OO0OO0O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        O00O00O00OO0O = O00OO0OO0O.result['datalabels']['varname']
        return len(O00O00O00OO0O)

    def get_dataset_variable_list(OO0O000000):
        """
        Gets list of variables in the dataset. Can be used in further processing.
        :return: list of variables in the dataset
        :rtype: list[str]
        """
        if not OO0O000000._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        O000OOO00O0 = OO0O000000.result['datalabels']['varname']
        return O000OOO00O0

    def get_dataset_variable_name(OO0OOOO00000, idx):
        """
        Gets name of the variable for a given index. Can be used in further processing.
        :param int idx: index of the variable
        :return: variable name for a specified index
        :rtype: str
        """
        if not OO0OOOO00000._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        O00OO0OOO0 = OO0OOOO00000.get_dataset_variable_list()
        if idx >= 0 and idx < len(O00OO0OOO0):
            return O00OO0OOO0[idx]
        else:
            print(f'ERROR: dataset has only {len(O00OO0OOO0)} variables, required index is {idx}, but available values are 0-{len(O00OO0OOO0) - 1}.')
            exit(1)

    def get_dataset_variable_index(O00O0O0O0O, varname):
        """
        Gets index of the variable for a given variable name. Can be used in further processing.
        :param str varname: name of the variable
        :return: index of the variable for a specified name
        :rtype: int
        """
        if not O00O0O0O0O._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        OO0000OOOOO0 = O00O0O0O0O.get_dataset_variable_list()
        if varname in OO0000OOOOO0:
            return OO0000OOOOO0.index(varname)
        else:
            print(f'ERROR: attribute {varname} is not in dataset. The list of attribute names is  {OO0000OOOOO0}.')
            exit(1)

    def get_dataset_category_list(OOOO00O000OOO, variable):
        """
        Gets list of categories for the variable in the dataset. Can be used in further processing.
        :param str/int variable: name or index of the variable
        :return: list of categories for the variable in the dataset
        :rtype: list[str]
        """
        if not OOOO00O000OOO._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        O000OOO0O0O = OOOO00O000OOO.result['datalabels']['catnames']
        O0000O0O00 = None
        if isinstance(variable, int):
            O0000O0O00 = variable
        else:
            O0000O0O00 = OOOO00O000OOO.get_dataset_variable_index(variable)
        if O0000O0O00 >= 0 and O0000O0O00 < len(O000OOO0O0O):
            return O000OOO0O0O[O0000O0O00]
        else:
            print(f'ERROR: dataset has only {len(O000OOO0O0O)} variables, required index is {O0000O0O00}, but available values are 0-{len(O000OOO0O0O) - 1}.')
            exit(1)

    def get_dataset_category_count(O0O0O00OOOOO, variable):
        """
        Gets count of categories for the variable in the dataset. Can be used in further processing.
        :param str/int variable: name or index of the variable
        :return: count of categories for the given variable in the dataset
        :rtype: int
        """
        if not O0O0O00OOOOO._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        OOO0000000O = None
        if isinstance(variable, int):
            OOO0000000O = variable
        else:
            OOO0000000O = O0O0O00OOOOO.get_dataset_variable_index(variable)
        O0O0O00OOOOO0 = O0O0O00OOOOO.get_dataset_category_list(OOO0000000O)
        return len(O0O0O00OOOOO0)

    def get_dataset_category_name(O000000O00OO, variable, cat_idx):
        """
        Gets the name of the category for a given variable and cateory index in the dataset. Can be used in further processing.
        :param str/int variable: name or index of the variable
        :param str cat_idx: index of the category of the variable
        :return: category name in the dataset for the value and category index
        :rtype: str
        """
        if not O000000O00OO._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        O0O00OO0O0O0O = None
        if isinstance(variable, int):
            O0O00OO0O0O0O = variable
        else:
            O0O00OO0O0O0O = O000000O00OO.get_dataset_variable_index(variable)
        O0OOOO0OOOO = O000000O00OO.get_dataset_category_list(O0O00OO0O0O0O)
        if cat_idx >= 0 and cat_idx < len(O0OOOO0OOOO):
            return O0OOOO0OOOO[cat_idx]
        else:
            print(f'ERROR: variable has only {len(O0OOOO0OOOO)} categories, required index is {cat_idx}, but available values are 0-{len(O0OOOO0OOOO) - 1}.')
            exit(1)

    def get_dataset_category_index(OO0OOO000O00, variable, cat_name):
        """
        Gets the index of the category name for a given variable in the dataset. Can be used in further processing.
        :param str/int variable: name or index of the variable.
        :param str cat_name: name of the category
        :return: index of the category in the dataset for the variable and given category name
        :rtype: int
        """
        if not OO0OOO000O00._is_calculated():
            print('ERROR: Task has not been calculated.')
            return
        O0O0O00000O00 = None
        if isinstance(variable, int):
            O0O0O00000O00 = variable
        else:
            O0O0O00000O00 = OO0OOO000O00.get_dataset_variable_index(variable)
        OO00000OOO00 = OO0OOO000O00.get_dataset_category_list(O0O0O00000O00)
        if cat_name in OO00000OOO00:
            return OO00000OOO00.index(cat_name)
        else:
            print(f'ERROR: value {cat_name} is invalid for the variable {OO0OOO000O00.get_dataset_variable_name(O0O0O00000O00)}. Available category names are {OO00000OOO00}.')
            exit(1)

def clm_vars(a, minlen=1, maxlen=3, type='con'):
    out = []
    for itm in a:
        if isinstance(itm, dict):
            d = itm
        else:
            d = {}
            d['name'] = itm
            d['type'] = 'subset'
            d['minlen'] = 1
            d['maxlen'] = 1
        out.append(d)
    tot = {}
    tot['attributes'] = out
    tot['minlen'] = minlen
    tot['maxlen'] = maxlen
    tot['type'] = type
    return tot

def clm_subset(v, minlen=1, maxlen=1):
    d = {}
    d['name'] = v
    d['type'] = 'subset'
    d['minlen'] = minlen
    d['maxlen'] = maxlen
    return d

def clm_seq(v, minlen=1, maxlen=2):
    d = {}
    d['name'] = v
    d['type'] = 'seq'
    d['minlen'] = minlen
    d['maxlen'] = maxlen
    return d

def clm_lcut(v, minlen=1, maxlen=2):
    d = {}
    d['name'] = v
    d['type'] = 'lcut'
    d['minlen'] = minlen
    d['maxlen'] = maxlen
    return d

def clm_rcut(v, minlen=1, maxlen=2):
    d = {}
    d['name'] = v
    d['type'] = 'rcut'
    d['minlen'] = minlen
    d['maxlen'] = maxlen
    return d
