"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from unittest import TestCase
from faker import Faker

from payments.common import utils


_FAKE = Faker()

class UtilsTestCase(TestCase):
    def test_get_keys_from_dict(self):
        testing_dict = {'key_one': 1, 'key_two': 2, 'key_three': 3}
        self.assertListEqual([('key_one', 'Key one'), ('key_two', 'Key two'), ('key_three',
                                                                               'Key three')],
        utils.get_keys_from_dict(
            testing_dict))

    def test_get_all_values_of_a_key_from_list_of_dict(self):

        key1 = _FAKE.pystr()
        key2 = _FAKE.pystr()

        values = []
        for _ in range(4):
            values.append(_FAKE.pystr())

        test_data = [{key1: values[0], key2: values[1]},
                     {key1: values[2], key2: values[3]},
                     {key1: values[0], key2: values[3]}]

        expected_1 = [values[0], values[2]]
        expected_2 = [values[1], values[3]]

        expected_1.sort()
        expected_2.sort()

        actual_1 = utils.get_all_values_of_a_key_from_list_of_dict(test_data, key1)
        actual_2 = utils.get_all_values_of_a_key_from_list_of_dict(test_data, key2)

        actual_1.sort()
        actual_2.sort()

        self.assertListEqual(expected_1, actual_1)
        self.assertListEqual(expected_2, actual_2)

    def test_get_data_from_dict(self):
        test_list = [{'key1': 'value1', 'key2': 'kk'}, {'key1': 'value2', 'key2': 'bb'},
                     {'key1': 'value1', 'key2': 'tt'}, {'key2': 'bb'}]

        actual = utils.get_data_from_dict(test_list, 'key1', 'value1')
        expected = [{'key1': 'value1', 'key2': 'kk'}, {'key1': 'value1', 'key2': 'tt'}]

        self.assertListEqual(actual, expected)
