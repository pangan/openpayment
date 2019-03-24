# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from mock import patch

from faker import Faker
from flask import json

from tests.base import BaseTestCase

_FAKE = Faker()


class EndpointsTestCase(BaseTestCase):
    def setUp(self):
        super(EndpointsTestCase, self).setUp()

    def tearDown(self):
        super(EndpointsTestCase, self).tearDown()

    def test_open_payments(self):
        with patch('payments.endpoints.open_payments.get_data_from_celery') as mocked_get_data:
            mocked_get_data.return_value = {}
            response = self.app.get('/search')

        self.assertEqual(response.status_code,  200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertDictEqual(json.loads(response.data), {'data': {}})
