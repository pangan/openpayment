# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""

from unittest import TestCase
from payments.app import api


class BaseTestCase(TestCase):
    def setUp(self):

        api.testing = True
        self.api = api
        self.app = api.test_client()

        api.config['TESTING'] = True
        api.config['DEBUG'] = False

        self.api = api

        self.app = api.test_client()

    def tearDown(self):
        pass
        #del os.environ['PAYMENTS_TESTING_MODE']

