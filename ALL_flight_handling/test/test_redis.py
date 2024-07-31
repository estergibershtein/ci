import unittest
import json
from unittest.mock import MagicMock, patch

from utils.redis_actions import RedisActions


class TestUpdateCountSubFlight(unittest.TestCase):
    @patch("redis.Redis")
    def setUp(self, mock_redis):
        self.redis_actions = RedisActions()
        self.mock_redis = mock_redis
        self.mock_get_json_data = self.mock_redis.return_value.get_json_data

    def test_get_names_failed_children(self):
        test_data = {"FailuresChildren": "Child1"}
        self.redis_actions.connect_redis.get.return_value = json.dumps(test_data)
        result = self.redis_actions.get_names_failed_children("TestFlight")
        self.assertEqual(result, "Child1")

    def test_get_names_failed_children_exception(self):
        self.mock_get_json_data.side_effect = Exception("Test Error")
        with self.assertRaises(ValueError):
            self.redis_actions.get_names_failed_children("TestFlight")

    def test_update_count_sub_flight(self):
        flight_name = "Flight123"
        flight_message = {"test": "example_data", "CountSubFlight": 2}
        self.redis_actions.connect_redis.set.return_value = (flight_name, json.dumps(flight_message))
        self.redis_actions.connect_redis.update_count_sub_flight(flight_name)
        test_data = self.redis_actions.connect_redis.get.return_value = flight_message
        flight_message["CountSubFlight"] -= 1
        self.assertEqual(test_data, flight_message)

    def test_delete_data_flight(self):
        self.redis_actions.connect_redis.delete = MagicMock()
        self.redis_actions.delete_data_flight("test_flight")
        self.redis_actions.connect_redis.delete.assert_called_with("test_flight")

    @patch("utils.redis_actions.RedisActions.get_json_data")
    def test_get_names_failed_children(self, mock_get_json_data):  # noqa: F811
        expected_result = ["Child1", "Child2"]
        mock_get_json_data.return_value = {"FailuresChildren": expected_result}
        test_instance = RedisActions()
        result = test_instance.get_names_failed_children("test_flight_name")
        self.assertEqual(result, expected_result)

    def test_get_json_data_success(self):
        mock_instance = RedisActions()
        test_data = {"key": "value"}
        mock_instance.get_json_data = MagicMock(return_value=test_data)
        result = mock_instance.get_json_data("test_flight_name")
        expected_result = {"key": "value"}
        self.assertDictEqual(result, expected_result)

    def test_get_failed_children_and_error_description(self):
        mock_data_flight = {"FailuresChildren": ["Child1", "Child2"]}
        mock_instance = RedisActions()
        mock_instance.get_json_data = MagicMock(return_value=mock_data_flight)
        result = mock_instance.get_failed_children_and_error_description("TestFlight")
        self.assertEqual(result, ["Child1", "Child2"])
        mock_instance.get_json_data.assert_called_once_with("TestFlight")

    def test_get_failed_children_and_error_description_exception(self):
        mock_instance = RedisActions()
        mock_instance.get_json_data = MagicMock(side_effect=Exception("Test Error"))
        with self.assertRaises(ValueError):
            mock_instance.get_failed_children_and_error_description("TestFlight")
        mock_instance.get_json_data.assert_called_once_with("TestFlight")
