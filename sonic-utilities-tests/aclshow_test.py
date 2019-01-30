import sys
import os
from StringIO import StringIO
import mock

test_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(test_path)
scripts_path = os.path.join(modules_path, "scripts")
sys.path.insert(0, modules_path)

from imp import load_source
load_source('aclshow', scripts_path+'/aclshow')
from aclshow import *

import mock_tables.dbconnector

default_output = ''+ \
"""RULE NAME     TABLE NAME      PACKETS COUNT    BYTES COUNT
------------  ------------  ---------------  -------------
RULE_9        DATAACL                   901            900
RULE_7        DATAACL                   701            700
RULE_6        DATAACL                   601            600
RULE_4        DATAACL                   401            400
RULE_3        DATAACL                   301            300
RULE_2        DATAACL                   201            200
RULE_1        DATAACL                   101            100
DEFAULT_RULE  DATAACL                     2              1
"""

all_output = '' + \
"""RULE NAME     TABLE NAME      PACKETS COUNT    BYTES COUNT
------------  ------------  ---------------  -------------
RULE_9        DATAACL                   901            900
RULE_7        DATAACL                   701            700
RULE_6        DATAACL                   601            600
RULE_4        DATAACL                   401            400
RULE_3        DATAACL                   301            300
RULE_2        DATAACL                   201            200
RULE_1        DATAACL                   101            100
DEFAULT_RULE  DATAACL                     2              1
RULE_05       DATAACL                     0              0
RULE_0        DATAACL                     0              0
RULE_08       DATAACL                     0              0
"""

rule1_dataacl_output = '' + \
"""RULE NAME    TABLE NAME      PACKETS COUNT    BYTES COUNT
-----------  ------------  ---------------  -------------
RULE_1       DATAACL                   101            100
"""

rule5_all_output = ''+ \
"""RULE NAME    TABLE NAME      PACKETS COUNT    BYTES COUNT
-----------  ------------  ---------------  -------------
RULE_05      DATAACL                     0              0
"""

rule0_output = '' + \
"""RULE NAME    TABLE NAME    PACKETS COUNT    BYTES COUNT
-----------  ------------  ---------------  -------------
"""

rule4_rule6_verbose_output = '' + \
"""Reading ACL info...
Total number of ACL Tables 4:
Total number of ACL Rules: 11

RULE NAME    TABLE NAME      PACKETS COUNT    BYTES COUNT
-----------  ------------  ---------------  -------------
RULE_6       DATAACL                   601            600
RULE_4       DATAACL                   401            400
"""

everflow_output = '' + \
"""RULE NAME    TABLE NAME    PACKETS COUNT    BYTES COUNT
-----------  ------------  ---------------  -------------
"""

dataacl_output = '' + \
"""RULE NAME     TABLE NAME      PACKETS COUNT    BYTES COUNT
------------  ------------  ---------------  -------------
RULE_9        DATAACL                   901            900
RULE_7        DATAACL                   701            700
RULE_6        DATAACL                   601            600
RULE_4        DATAACL                   401            400
RULE_3        DATAACL                   301            300
RULE_2        DATAACL                   201            200
RULE_1        DATAACL                   101            100
DEFAULT_RULE  DATAACL                     2              1
"""

all_after_clear_output = '' + \
"""RULE NAME     TABLE NAME      PACKETS COUNT    BYTES COUNT
------------  ------------  ---------------  -------------
RULE_3        DATAACL                     0              0
RULE_2        DATAACL                     0              0
RULE_1        DATAACL                     0              0
RULE_05       DATAACL                     0              0
RULE_0        DATAACL                     0              0
RULE_7        DATAACL                     0              0
RULE_9        DATAACL                     0              0
RULE_6        DATAACL                     0              0
RULE_08       DATAACL                     0              0
DEFAULT_RULE  DATAACL                     0              0
RULE_4        DATAACL                     0              0
"""

clear_output = ''

class Aclshow():
    def __init__(self, *args, **kwargs):
        """
        nullify_on_start, nullify_on_exit will call nullify_counters()
        before and/or after the test. By default - clear on start and exit.
        """
        self.nullify_on_start, self.nullify_on_exit = args if args else (True, True)
        self.kwargs = kwargs
        self.setUp()
        self.runTest()
        self.tearDown()

    def nullify_counters(self):
        """
        This method is used to empty dumped counters
        if exist in /tmp/.counters_acl.p (by default).
        """
        if os.path.isfile(COUNTER_POSITION):
            with open(COUNTER_POSITION, 'wb') as fp:
                json.dump([], fp)

    def runTest(self):
        """
        This method invokes main() from aclshow utility (parametrized by argparse)
        parametrized by mock argparse.
        """
        @mock.patch('argparse.ArgumentParser.parse_args', return_value = argparse.Namespace(**self.kwargs))
        def run(mock_args):
            main()
        run()

    def setUp(self):
        if self.nullify_on_start:
            self.nullify_counters()
        self.old_stdout = sys.stdout
        self.result = StringIO()
        sys.stdout = self.result

    def tearDown(self):
        if self.nullify_on_exit:
            self.nullify_counters()
        sys.stdout = self.old_stdout
        print self.result.getvalue()

def test_default():
    test = Aclshow(all = None, clear = None, rules = None, tables = None, verbose = None)
    assert test.result.getvalue() == default_output

def test_all():
    test = Aclshow(all = True, clear = None, rules = None, tables = None, verbose = None)
    assert test.result.getvalue() == all_output

def test_rule1_dataacl():
    test = Aclshow(all = None, clear = None, rules = 'RULE_1', tables = 'DATAACL', verbose = None)
    assert test.result.getvalue() == rule1_dataacl_output

def test_rule05_all():
    test = Aclshow(all = True, clear = None, rules = 'RULE_05', tables = None, verbose = None)
    assert test.result.getvalue() == rule5_all_output

def test_rule0():
    test = Aclshow(all = None, clear = None, rules = 'RULE_0', tables = None, verbose = None)
    assert test.result.getvalue() == rule0_output

def test_rule4_rule6_verbose():
    test = Aclshow(all = None, clear = None, rules = 'RULE_4,RULE_6', tables = None, verbose = True)
    assert test.result.getvalue() == rule4_rule6_verbose_output

def test_everflow():
    test = Aclshow(all=None, clear=None, rules=None, tables='EVERFLOW', verbose=None)
    assert test.result.getvalue() == everflow_output

def test_dataacl():
    test = Aclshow(all=None, clear=None, rules=None, tables='DATAACL', verbose=None)
    assert test.result.getvalue() == dataacl_output

def test_clear():
    test = Aclshow(all=None, clear=True, rules=None, tables=None, verbose=None)
    assert test.result.getvalue() == clear_output

def test_all_after_clear():
    nullify_on_start, nullify_on_exit = True, False
    test = Aclshow(nullify_on_start, nullify_on_exit, all=True, clear=True, rules=None, tables=None, verbose=None)
    assert test.result.getvalue() == clear_output
    nullify_on_start, nullify_on_exit = False, True
    test = Aclshow(nullify_on_start, nullify_on_exit, all=True, clear=False, rules=None, tables=None, verbose=None)
    assert test.result.getvalue() == all_after_clear_output
