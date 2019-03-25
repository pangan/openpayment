"""
By Amir Mofakhar <amir@mofakhar.info>
"""


def _make_readable(input_string):
    output_string = input_string.replace('_', ' ')
    output_string = output_string.capitalize()

    return output_string


def get_keys_from_dict(input_dict):
    fields = [*input_dict]
    ret_list_of_tuples = []
    for item in fields:
        ret_list_of_tuples.append((item, _make_readable(item)))
    return ret_list_of_tuples


def get_all_values_of_a_key_from_list_of_dict(list_of_dict, key):
    return_list = set([d[key] for d in list_of_dict if key in d])
    return list(return_list)


def get_keys_from_dict_2(input_dict):
    return [*input_dict]


def get_data_from_dict(list_of_dicts, field_to_search, keyword):
    return_list = list(filter(lambda d: d.get(field_to_search) == keyword, list_of_dicts))
    return return_list


# TODO: use this method for getting list of all keys!
def get_all_keys_new(input_list_of_dict):
    a = set().union(*(d.keys() for d in mylist))
    return a