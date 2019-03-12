import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from annotate import models, class_from_filename, table_name_from_filename, get_config_file
import tempfile

def test_models():
  result = models('tests/fixture_models')
  result.sort()
  result = list(map( lambda x: os.path.split(x)[1], result))
  assert result == ['fixture_model_1.py', 'fixture_model_2.py']

def test_class_from_filename():
  assert class_from_filename('class_name.py') == 'ClassName'

def test_class_from_filename_multiple():
  assert class_from_filename('class_name_sfsaa.py') == 'ClassNameSfsaa'

def test_table_name_from_filename():
  assert table_name_from_filename('engine_model_names.py') == 'engine_model_names'

def test_get_config_file():
  assert get_config_file('tests/fixture_models/fixture_model_1.py') == {'DATABASES': { 'a': 1, 'b': 2 } }