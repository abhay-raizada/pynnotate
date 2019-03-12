import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from annotate import models

def test_models():
  result = models('tests/fixture_models')
  result.sort()
  assert result == ['fixture_model_1.py', 'fixture_model_2.py']