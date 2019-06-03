import sqlite3
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))
from annotatelib.settings import get_config_file
from annotate import write_to_file


def test_get_config_file():
    assert get_config_file('tests/fixture_models/fixture_model_1.py') == {
        'sqlite3': {'database': 'test.db', 'driver': 'sqlite'}}


def test_write_to_file():
    database = "test.db"
    create_database(database)
    file_path = 'tests/fixture_models/tasks.py'
    write_to_file(os.path.dirname(file_path),
                  'tests/fixture_models/fixture_model_1.py')
    result = open(file_path).read()
    drop_database(database)
    truncate_file(file_path)
    assert result == '''#====== Schema information
# id         integer                            primary_key
# name       text           not null
# priority   integer
# status_id  integer        not null
# project_id integer        not null
# begin_date text           not null
# end_date   text           not null

'''


def create_database(database):
    sql_create_tasks_table = \
        """CREATE TABLE IF NOT EXISTS tasks (
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
