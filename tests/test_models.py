import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from annotate import models, class_from_filename

def test_models():
  result = models('tests/fixture_models')
  result.sort()
  result = list(map( lambda x: os.path.split(x)[1], result))
  assert result == ['fixture_model_1.py', 'fixture_model_2.py']

def test_class_from_filename():
  assert class_from_filename('class_name.py') == 'ClassName'

def test_class_from_filename_multiple():
  assert class_from_filename('class_name_sfsaa.py') == 'ClassNameSfsaa'