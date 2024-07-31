import unittest
import json
from unittest.mock import MagicMock, patch

from utils.redis_actions import RedisActions


class TestUpdateCountSubFlight(unittest.TestCase):
    
    @patch('redis.Redis')
    def setUp(self, mock_redis):
        self.redis_actions = RedisActions()
        self.mock_redis = mock_redis
    
    
    def test_update_count_sub_flight(self):
        redis = RedisActions()
        flight_name = "Flight123"
        flight_message = {"test": "example_data", "CountSubFlight": 2}
        redis.connect_redis.set(flight_name, json.dumps(flight_message))
        redis.update_count_sub_flight(flight_name)
        saved_data = redis.connect_redis.get(flight_name)
        test_data = json.loads(saved_data)
        flight_message["CountSubFlight"] -= 1
        self.assertEqual(test_data, flight_message)
        redis.connect_redis.delete(flight_name)

    def test_delete_data_flight(self):
        redis = RedisActions()
        flight_name = "Flight123"
        flight_message = {"test": "example_data", "CountSubFlight": 2}
        redis.connect_redis.set(flight_name, json.dumps(flight_message))
        redis.delete_data_flight(flight_name)
        flight_exists = redis.connect_redis.exists(flight_name)
        self.assertEqual(flight_exists, 0)
        assert not flight_exists, f"Flight data {flight_name} still exists in Redis"

    @patch("utils.redis_actions.RedisActions.get_json_data")
    def test_get_names_failed_children(self, mock_get_json_data):
        expected_result = ["Child1", "Child2"]
        mock_get_json_data.return_value = {"FailuresChildren": expected_result}
        test_instance = RedisActions()
        result = test_instance.get_names_failed_children("test_flight_name")
        self.assertEqual(result, expected_result)

    def test_get_json_data_success(self):
        redis = RedisActions()
        test_data = {"key": "value"}
        redis.connect_redis.set("test_flight_name", json.dumps(test_data))
        result = redis.get_json_data("test_flight_name")
        expected_result = {"key": "value"}
        self.assertDictEqual(result, expected_result)

    def test_get_failed_children_and_error_description_success(self):
        redis = RedisActions()
        test_data = {"FailuresChildren": ["Child1", "Child2"]}
        redis.connect_redis.set("test_flight_name", json.dumps(test_data))
        result = redis.get_failed_children_and_error_description("test_flight_name")
        self.assertEqual(result, test_data["FailuresChildren"])

    def test_get_failed_children_and_error_description_exception(self):
        mock_instance = MagicMock()
        mock_instance.get_json_data.side_effect = Exception("Error getting JSON data")
        redis = RedisActions()
        with self.assertRaises(ValueError):
            redis.get_failed_children_and_error_description("test_flight_name")
