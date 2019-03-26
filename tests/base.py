# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""

#from unittest import TestCase
from flask_testing import TestCase

from mock import patch


class MockedCeleryResult:

    @staticmethod
    def ready():
        return True

    def get(self, **kwargs):
        return []


class BaseTestCase(TestCase):

    def create_app(self):

        patch_celery_result = patch('payments.fetch_data.tasks.AsyncResult')
        mocked_celery_result = patch_celery_result.start()
        mocked_celery_result.return_value = MockedCeleryResult()

        from payments.app import api
        # api.testing = True
        # self.api = api
        self.app = api.test_client()

        api.config['TESTING'] = True
        api.config['DEBUG'] = False

        #self.api = api

        #self.app_2 = api.test_client()

        return api

    def tearDown(self):
        patch.stopall()
