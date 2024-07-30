import unittest
from unittest.mock import patch, MagicMock

from utils.const import ColonyConfig
from ALL_flight_handling import (
    ALL_flight_handling,
    update_flight_message,
    update_flight_message_to_error,
    handle_success_flight,
)

class TestUpdateFlightMessageToError(unittest.TestCase):
    
    
    @patch("utils.redis_actions.RedisActions.get_names_failed_children")
    @patch("utils.redis_actions.RedisActions.update_count_sub_flight")
    def test_ALL_flight_handling_success(self, mock_update_count_sub_flight, mock_get_names_failed_children):
        flight_message = {"payload": {"folder": "test_folder"}, "flightData": {"flightPath": "test_path"}}
        mock_get_names_failed_children.return_value = []
        mock_update_count_sub_flight.return_value = 0
        ALL_flight_handling(flight_message)
        mock_get_names_failed_children.assert_called()
        mock_update_count_sub_flight.assert_called()

    @patch("utils.redis_actions.RedisActions.get_names_failed_children")
    @patch("utils.redis_actions.RedisActions.update_count_sub_flight")
    def test_ALL_flight_handling_exception(self, mock_update_count_sub_flight, mock_get_names_failed_children):
        flight_message = {"payload": {"folder": "example_folder"}, "flightData": {"flightPath": "example_path"}}
        ALL_flight_handling(flight_message)
        mock_get_names_failed_children.assert_called()
        mock_update_count_sub_flight.assert_called()

    @patch("utils.rabbitmq_actions.RabbitmqActions.publish")
    @patch("utils.redis_actions.RedisActions.delete_data_flight")
    def test_handle_success_flight(self, mock_delete_data_flight, mock_rabbitmq_publish):
        flight_message = {"flightData": None}
        mock_rabbitmq = MagicMock()
        mock_redis = MagicMock()
        parent_name = "TestParentName"
        update_flight_message_return_value = {"updated_flight_data": "updated"}
        mock_redis.delete_data_flight.return_value = None
        mock_rabbitmq.publish.return_value = None
        with patch("ALL_flight_handling.update_flight_message", return_value=update_flight_message_return_value):
            handle_success_flight(flight_message, mock_rabbitmq, mock_redis, parent_name)
        self.assertEqual(flight_message["flightData"], update_flight_message_return_value)
        mock_rabbitmq_publish.assert_not_called()
        mock_redis.delete_data_flight.assert_called_with(parent_name)

    def test_update_flight_message_to_error(self):
        mock_redis = MagicMock()
        parent_name = "TestParent"
        mock_failed_children = ["Child1", "Child2"]
        mock_redis.get_failed_children_and_error_description.return_value = mock_failed_children
        mock_flight_message = {
            "payload": {"errorDescription": "", "failuresChildren": [], "mailTo": ""},
            "flightData": "some data",
        }
        expected_result = {
            "errorDescription": "There are sub-flight that failed",
            "failuresChildren": mock_failed_children,
            "mailTo": ColonyConfig.EMAILS,
        }

        result = update_flight_message_to_error(mock_flight_message, mock_redis, parent_name)
        self.assertEqual(result, expected_result)
        self.assertNotIn("flightData", mock_flight_message)

    def test_update_flight_message(self):
        flight_name = "TestFlight"
        expected_result = {
            "flightPath": flight_name,
            "flightFormat": "ALL",
            "flightType": "NAVAD",
            "flightName": flight_name,
            "parent": None,
        }
        result = update_flight_message(flight_name)
        self.assertEqual(result, expected_result)
