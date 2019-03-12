import os
from functools import  partial
def models(model_path = 'models'):
  partial_join = partial(os.path.join, model_path)
  return list(map(os.path.abspath,
    list(map(partial_join, os.listdir(model_path)))))

def main():
  for model_path in models:
    model_dir, model_file = os.path.split(model_path)
    model_class = class_from_filename(model_file)

def class_from_filename(model_file):
  return os.path.splitext(
    model_file)[0].replace('_', ' ').title().replace(' ', '')