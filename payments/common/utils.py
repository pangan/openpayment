"""
By Amir Mofakhar <amir@mofakhar.info>
"""


def get_keys_from_dict(input_dict):
    fields = [*input_dict]
    ret_list_of_tuples = []
    for item in fields:
        ret_list_of_tuples.append((item, item))
    return ret_list_of_tuples
