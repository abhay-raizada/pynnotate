import os
from functools import  partial
from orator import DatabaseManager
from collections import OrderedDict
import yaml

def models(model_path = 'models'):
    partial_join = partial(os.path.join, model_path)
    return list(map(os.path.abspath,
    list(map(partial_join, os.listdir(model_path)))))

def get_model_path_info_map(model_path, config_path):
    db = DatabaseManager(get_config_file(config_path))
    schema_manager = db.get_schema_manager()
    file_info_map = OrderedDict()
    for model_path in models(model_path):
        _, model_file = os.path.split(model_path)
        table_name = table_name_from_filename(model_file)
        columns_description = get_column_description_from_object(schema_manager, table_name)
        if not columns_description:
            continue
        indices_description = get_indices_description_from_oject(schema_manager, table_name)
        file_info_map[model_path] = OrderedDict([
            ('columns', columns_description),
            ('indices', indices_description),
            ('table_name', table_name)
        ])
    return file_info_map

def write_to_file(model_path, config_path = 'orator.py'):
    path_info_map = get_model_path_info_map(model_path, config_path)
    for model_file in path_info_map.keys():
        add_data_to_file(model_file, path_info_map[model_file])

def add_data_to_file(model_file, model_data):
    with open(model_file, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        model_data_string = formate_data(model_data)
        if content.startswith(model_data_string):
            return
        f.write(model_data_string + "\n" + content)

def formate_data(model_data):
    columns = model_data['columns']
    start_string = \
'''"""
====== Schema information

'''
    columns_string = ''
    for _,column in columns.items():
        columns_string += format_column(column)
    end_string = \
'''
"""
'''
    return start_string + columns_string + end_string

def format_column(column_hash):
    column_type = column_hash['type']
    if column_hash['length'] :
        column_type += '(' + column_hash['length'] + ')'
    notnull = ''
    if column_hash['notnull']:
        notnull = 'not null'
    default = ''
    if column_hash['default']:
        default = 'default(' + column_hash['default'] + ')'
    pk = ''
    if column_hash['pk']:
        pk = 'primary_key'
    return (column_hash['name'] + ' ' + column_type + ' ' + notnull + ' ' + default + ' ' + pk).strip() + '\n'

def get_indices_description_from_oject(schema_manager, table_name):
    indices_description = OrderedDict()
    index_name_obj_map = schema_manager.list_table_indexes(table_name)
    for index_name in index_name_obj_map.keys():
        index_obj = index_name_obj_map[index_name]
        indices_description[index_name] = {
            'columns': index_obj.get_unquoted_columns(),
            'is_unique?': index_obj.is_unique(),
            'is_primary?': index_obj.is_primary()
        }
    return indices_description

def  get_column_description_from_object(schema_manager, table_name):
    columns_description = OrderedDict()
    column_name_obj_map = schema_manager.list_table_columns(table_name)
    for column_name in column_name_obj_map.keys():
        column_obj = column_name_obj_map[column_name]
        columns_description[column_name] = column_obj.to_dict()
    return columns_description

def get_config_file(config_path):
    config = {}
    exec(open(config_path).read(), {}, config)
    return config.get("databases", config.get("DATABASES", {}))

def table_name_from_filename(model_file):
    return os.path.splitext(
    model_file)[0]

def class_from_filename(model_file):
    return os.path.splitext(
    model_file)[0].replace('_', ' ').title().replace(' ', '')