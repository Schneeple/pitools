"""
PiPull
=====

Provides
  1. Ability to pull Data from the OSIsoft server
  2. Send data to the PiServer to created Pi Tags.

Feel free to reach out for more information / suggestions.

=====
Contact Information:
    Colton Neary
    Cneary@nevadagoldmines.com
    schneeple@outlook.com
  """


from os.path import dirname, basename, isfile
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from IPython.core.interactiveshell import InteractiveShell
import json
import datetime
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import os
import datetime as DT
import seaborn as sns
import cufflinks as cf
from tqdm.notebook import tqdm
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
cf.go_offline()
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
InteractiveShell.ast_node_interactivity = "all"
global environ
global username


environ = os.environ
username = environ.get('USERNAME')

if username == None:
    # print('Welcome to pitools Squire.')
    print("""
            _____ ________              ______        
    ________ ___(_)___  __/______ ______ ___  /________
    ___  __ \__  / __  /   _  __ \_  __ \__  / __  ___/
    __  /_/ /_  /  _  /    / /_/ // /_/ /_  /  _(__  ) 
    _  .___/ /_/   /_/     \____/ \____/ /_/   /____/  
    /_/                                                
    """)



else:
    print('Welcome to pitools ' + str(username) + '.')
