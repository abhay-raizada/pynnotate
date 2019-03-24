import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from orator import DatabaseManager
import sqlite3

from annotatelib.models import(
    models, class_from_filename,
    table_name_from_filename, _get_column_description_from_object,
    _get_indices_description_from_oject
)


def test_models():
  result = models('tests/fixture_models')
  result.sort()
  result = list(map( lambda x: os.path.split(x)[1], result))
  assert result == ['fixture_model_1.py', 'fixture_model_2.py', 'tasks.py']

def test_class_from_filename():
  assert class_from_filename('class_name.py') == 'ClassName'

def test_class_from_filename_multiple():
  assert class_from_filename('class_name_sfsaa.py') == 'ClassNameSfsaa'

def test_table_name_from_filename():
  assert table_name_from_filename('engine_model_names.py') == 'engine_model_names'

def test_get_column_description_from_object():
  database = "test.db"
  create_database(database)
  config = {
        'sqlite3': {
          'driver': 'sqlite',
          'database': database
        }
    }
  db = DatabaseManager(config)
  result = _get_column_description_from_object(db.get_schema_manager(), 'tasks')
  print(result)
  assert result == {
    'id': {'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 1, 'precision': 10, 'name': 'id', 'extra': {}, 'scale': 0, 'type': 'integer', 'notnull': False, 'fixed': False},
    'status_id': {'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 0, 'precision': 10, 'name': 'status_id', 'extra': {}, 'scale': 0, 'type': 'integer', 'notnull': True, 'fixed': False},
    'project_id': {'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 0, 'precision': 10, 'name': 'project_id', 'extra': {},'scale': 0, 'type': 'integer', 'notnull': True, 'fixed': False},
    'name': { 'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 0, 'precision': 10, 'name': 'name', 'extra': {}, 'scale': 0, 'type': 'text', 'notnull': True, 'fixed': False},
    'end_date': {'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 0, 'precision': 10, 'name': 'end_date', 'extra': {}, 'scale': 0, 'type': 'text', 'notnull': True, 'fixed': False},
    'priority': {'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 0, 'precision': 10, 'name': 'priority', 'extra': {}, 'scale': 0, 'type': 'integer', 'notnull': False, 'fixed': False},
    'begin_date': {'unsigned': False, 'autoincrement': False, 'length': None, 'default': None,
      'pk': 0, 'precision': 10, 'name': 'begin_date', 'extra': {}, 'scale': 0, 'type': 'text', 'notnull': True, 'fixed': False}}
  drop_database(database)

def test_get_indices_description_from_object():
  database = "test.db"
  create_database(database)
  config = {
        'sqlite3': {
          'driver': 'sqlite',
          'database': database
        }
    }
  db = DatabaseManager(config)
  result = _get_indices_description_from_oject(db.get_schema_manager(), 'tasks')
  print(result)
  assert result == {'primary': {'is_unique?': True, 'is_primary?': True, 'columns': ['id']}}
  drop_database(database)

def create_database(database):
  sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                  id integer PRIMARY KEY,
                                  name text NOT NULL,
                                  priority integer,
                                  status_id integer NOT NULL,
                                  project_id integer NOT NULL,
                                  begin_date text NOT NULL,
                                  end_date text NOT NULL,
                                  FOREIGN KEY (project_id) REFERENCES projects (id)
                              );"""

  # create a database connection
  conn = sqlite3.connect(database)
  # create tasks table
  c = conn.cursor()
  c.execute(sql_create_tasks_table)

def drop_database(database):
  os.remove(database)

def truncate_file(file_path):
  with open(file_path, 'r+') as f:
    f.truncate(0)