import os
from functools import partial
from orator import DatabaseManager
from collections import OrderedDict

from .settings import get_config_file


def table_name_from_filename(model_file):
    return os.path.splitext(
        model_file)[0]


def class_from_filename(model_file):
    return os.path.splitext(
        model_file)[0].replace('_', ' ').title().replace(' ', '')


def models(model_path='models'):
    partial_join = partial(os.path.join, model_path)
    return list(map(os.path.abspath,
                    list(map(partial_join, os.listdir(model_path)))))


def get_model_path_info_map(model_path, config_path, **kwargs):
    db = DatabaseManager(get_config_file(config_path, **kwargs))
    schema_manager = db.get_schema_manager()
    file_info_map = OrderedDict()
    for model_path in models(model_path):
        _, model_file = os.path.split(model_path)
        table_name = table_name_from_filename(model_file)
        columns_description = _get_column_description_from_object(
            schema_manager, table_name)
        if not columns_description:
            continue
        indices_description = _get_indices_description_from_oject(
            schema_manager, table_name)
        file_info_map[model_path] = OrderedDict([
            ('columns', columns_description),
            ('indices', indices_description),
            ('table_name', table_name)
        ])
    return file_info_map


def _get_indices_description_from_oject(schema_manager, table_name):
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


def _get_column_description_from_object(schema_manager, table_name):
    columns_description = OrderedDict()
    column_name_obj_map = schema_manager.list_table_columns(table_name)
    for column_name in column_name_obj_map.keys():
        column_obj = column_name_obj_map[column_name]
        columns_description[column_name] = column_obj.to_dict()
    return columns_description
