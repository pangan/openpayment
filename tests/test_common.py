"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from unittest import TestCase
from faker import Faker

from payments.common import utils


_FAKE = Faker()

class UtilsTestCase(TestCase):
    def test_get_keys_from_dict(self):
        testing_dict = {'key1': 1, 'key2': 2, 'key3': 3}
        self.assertListEqual([('key1', 'key1'), ('key2', 'key2'), ('key3', 'key3')],
        utils.get_keys_from_dict(
            testing_dict))

    def test_get_all_values_of_a_key_from_list_of_dict(self):

        key1 = _FAKE.pystr()
        key2 = _FAKE.pystr()

        test_data = [{key1: 'value1', key2: 'value2'},
                     {key1: 'value_one', key2: 'value_two'},
                     {key1: 'value1', key2: 'value_two'}]

        expected_1 = [test_data[0][key1], test_data[1][key1]]
        expected_2 = [test_data[0][key2], test_data[1][key2]]

        expected_1.sort()
        expected_2.sort()

        actual_1 = utils.get_all_values_of_a_key_from_list_of_dict(test_data, key1)
        actual_2 = utils.get_all_values_of_a_key_from_list_of_dict(test_data, key2)

        actual_1.sort()
        actual_2.sort()

        self.assertListEqual(expected_1, actual_1)

        self.assertListEqual(expected_2, actual_2)
