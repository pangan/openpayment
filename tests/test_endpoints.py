# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from mock import patch

from faker import Faker

from tests.base import BaseTestCase

_FAKE = Faker()


class EndpointsTestCase(BaseTestCase):
    def setUp(self):
        super(EndpointsTestCase, self).setUp()

    def tearDown(self):
        super(EndpointsTestCase, self).tearDown()

    def test_open_payments_get_method(self):
        self.client.get('/')
        self.assert_template_used('search.html')
        expected_context = [
            ('search_field', None),
            ('search_keyword', None),
            ('search_result', None), ('column_titles', None)]
        for key, value in expected_context:
            self.assert_context(key, value)

    def test_open_payments_selecting_field(self):
        self.client.post('/')
        self.assert_template_used('search.html')
        expected_context = [
            ('search_field', None),
            ('search_keyword', None),
            ('search_result', None), ('column_titles', None)]
        for key, value in expected_context:
            self.assert_context(key, value)

    def test_open_payments_searching(self):
        field_to_search = _FAKE.pystr()
        search_string = _FAKE.pystr()
        self.client.post('/', data={'submit_search': True, 'search_data': search_string,
                                    'field_to_search': field_to_search})
        self.assert_template_used('search.html')
        expected_context = [
            ('search_field', field_to_search),
            ('search_keyword', search_string),
            ('search_result', []), ('column_titles', [])]
        for key, value in expected_context:
            self.assert_context(key, value)

    def test_autocomplete(self):
        test_autocomplete_data = _FAKE.pylist(10, True, 'str')
        with patch(
                'payments.endpoints.open_payments.autocomplete_data',
                test_autocomplete_data):

            response = self.client.get('/_autocomplete')

        self.assertEqual(response.mimetype,  'application/json')
        self.assertListEqual(test_autocomplete_data, response.json)

    def test_download_xls(self):
        with patch('payments.endpoints.download.get_data_from_celery') as mocked_get_data:
            with patch(
                    'payments.endpoints.download.get_fields_from_celery') as mocked_get_fields:
                test_field_name = _FAKE.pystr()
                test_data = _FAKE.pystr()
                mocked_get_data.return_value = [{test_field_name: test_data}]
                mocked_get_fields.return_value = [(test_field_name, test_field_name)]
                response = self.client.get('/download_excel',
                                        query_string={'field': test_field_name,
                                                      'keyword': test_data})

        self.assertEqual(response.mimetype, 'application/vnd.ms-excel')
        self.assertIn('payments.xls', response.headers['Content-Disposition'])
