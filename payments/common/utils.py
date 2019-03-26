"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging
_LOG = logging.getLogger()

def _make_readable(input_string):
    output_string = input_string.replace('_', ' ')
    output_string = output_string.capitalize()

    return output_string


def get_all_values_of_a_key_from_list_of_dict(list_of_dict, key):
    return_list = set([d[key] for d in list_of_dict if key in d])
    return list(return_list)


def get_data_from_dict(list_of_dicts, field_to_search, keyword):
    return_list = list(filter(lambda d: d.get(field_to_search) == keyword, list_of_dicts))
    return return_list


def get_keys_from_dict(input_list_of_dict):
    _LOG.info('----->{}'.format(input_list_of_dict))
    keys_set = set().union(*(d.keys() for d in input_list_of_dict))
    fields = list(keys_set)
    fields.sort()
    ret_list_of_tuples = []
    for item in fields:
        ret_list_of_tuples.append((item, _make_readable(item)))

    return ret_list_of_tuples
