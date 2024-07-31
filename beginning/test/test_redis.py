import unittest
import json
import redis
from unittest.mock import MagicMock, patch

from utils.redis_actions import RedisActions


class TestSaveDataFlightInRedis(unittest.TestCase):
    @patch("redis.Redis")
    def setUp(self, mock_redis):
        self.redis_actions = RedisActions()
        self.mock_redis = mock_redis
        self.mock_get_json_data = self.mock_redis.return_value.get_json_data

    def test_save_data_flight_in_redis_integration(self):
        flight_name = "Flight123"
        flight_message = {"test": "example_data", "CountSubFlight": 2}
        self.redis_actions.connect_redis.set.return_value = (flight_name, json.dumps(flight_message))
        test_data = self.redis_actions.connect_redis.get.return_value = flight_message
        self.assertEqual(test_data, flight_message)
