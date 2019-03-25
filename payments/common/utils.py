"""
By Amir Mofakhar <amir@mofakhar.info>
"""


def get_keys_from_dict(input_dict):
    fields = [*input_dict]
    ret_list_of_tuples = []
    for item in fields:
        ret_list_of_tuples.append((item, item))
    return ret_list_of_tuples


def get_all_values_of_a_key_from_list_of_dict(list_of_dict, key):
    return_list = set([d[key] for d in list_of_dict if key in d])
    return list(return_list)
