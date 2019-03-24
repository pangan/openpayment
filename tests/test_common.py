"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from unittest import TestCase

from payments.common import utils


class UtilsTestCase(TestCase):
    def test_get_keys_from_dict(self):
        testing_dict = {'key1': 1, 'key2': 2, 'key3': 3}
        self.assertListEqual([('key1', 'key1'), ('key2', 'key2'), ('key3', 'key3')],
        utils.get_keys_from_dict(
            testing_dict))
