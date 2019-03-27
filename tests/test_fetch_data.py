"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from faker import Faker
from mock import patch

from payments.fetch_data.tasks import get_data_from_celery, get_payments_data_from_api
from tests.base import BaseTestCase

_FAKE = Faker()


class MockedCeleryResult:
    def __init__(self, return_data=None, raise_exception=False):
        self.return_data = return_data
        self.raise_exception = raise_exception

    @staticmethod
    def ready():
        return True

    def get(self, **kwargs):
        if self.raise_exception:
            raise Exception
        return self.return_data


class MockRequestsGet:
    def __init__(self, return_json={}, status_code=200):
        self.return_json = return_json
        self.status_code = status_code

    def json(self):
        return self.return_json


class TasksTestCase(BaseTestCase):
    def setUp(self):
        super(TasksTestCase, self).setUp()

    def tearDown(self):
        super(TasksTestCase, self).tearDown()

    def test_get_data(self):
        expected_data = _FAKE.pydict()

        with patch('payments.fetch_data.tasks.AsyncResult') as mocked_async_result:
            mocked_async_result.return_value = MockedCeleryResult(return_data=expected_data)
            actual_data = get_data_from_celery()

        self.assertDictEqual(actual_data, expected_data)

    def test_get_data_return_none_on_celery_exception(self):
        with patch('payments.fetch_data.tasks.AsyncResult') as mocked_async_result:
            mocked_async_result.return_value = MockedCeleryResult(raise_exception=True)

            self.assertIsNone(get_data_from_celery())

    def test_get_payments_data_from_api(self):
        with patch('payments.fetch_data.tasks.requests') as mocked_request:
            expected_response = _FAKE.pydict()
            mocked_request.get.return_value = MockRequestsGet(return_json=expected_response)

            self.assertDictEqual(get_payments_data_from_api(), expected_response)

    def test_get_payments_data_from_api_returns_none_on_not_200_from_api(self):
        with patch('payments.fetch_data.tasks.requests') as mocked_request:
            mocked_request.get.return_value = MockRequestsGet(status_code=400)
            self.assertIsNone(get_payments_data_from_api())

            mocked_request.get.side_effect = Exception()
            self.assertIsNone(get_payments_data_from_api())
