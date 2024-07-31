import unittest
from unittest.mock import patch, MagicMock

from beginning import (
    beginning,
    update_before_publish_to_colony,
    handle_sub_flight,
    all_flights_management,
    get_flight_data,
)

class TestBeginnerFunction(unittest.TestCase):
    @patch("beginning.get_flight_data")
    def test_handle_sub_flight(self, mock_get_flight_data):
        container = "Container123"
        flight_message = {"FlightData": None}
        parent_name = "ParentFlight"
        flight_name = "ChildFlight"
        mock_rabbitmq = MagicMock()
        handle_sub_flight(container, mock_rabbitmq, flight_message, parent_name, flight_name)
        mock_get_flight_data.assert_called_once()

    def test_update_flight_message(self):
        flight_message = {"payload": {"folder": "TestFolder", "errorDescription": {}, "mailTo": ""}}
        test_error = "TestError"
        updated_message = update_before_publish_to_colony(flight_message, test_error)
        self.assertEqual(updated_message["action"], "VerifyError")
        self.assertIn(flight_message["payload"]["folder"], updated_message["payload"]["errorDescription"])
        self.assertTrue(updated_message["payload"]["mailTo"])
        self.assertNotIn("flightData", updated_message)

    @patch("utils.redis_actions.RedisActions.save_data_flight")
    @patch("beginning.handle_sub_flight")
    def test_all_flights_management(self, mock_handle_sub_flight, mock_save_data_flight):
        rabbitmq = MagicMock()
        container = MagicMock()
        flight_message = {"payload": {"folder": "testFolder"}}
        mock_folder_list = ["Flight1", "Flight2", "Flight3"]
        container.get_folders_from_external_folder.return_value = mock_folder_list
        all_flights_management(container, rabbitmq, flight_message)
        mock_save_data_flight.assert_called_once()
        mock_handle_sub_flight.assert_called()

    @patch("beginning.get_container")
    @patch("beginning.get_flight_data")
    @patch("beginning.all_flights_management")
    def test_beginner(self, mock_all_flights_management, mock_update_flight_message, mock_get_azure_container):
        flight_message = {"payload": {"container": "testContainer", "folder": "testFolder", "flightFormat": "TEST"}}
        container = MagicMock()
        flight_data = {"FlightFormat": "TEST"}
        mock_get_azure_container.return_value = container
        mock_update_flight_message.return_value = flight_data
        beginning(flight_message)
        if flight_data["FlightFormat"] != "ALL":
            mock_all_flights_management.assert_not_called()
        else:
            mock_all_flights_management.assert_called_once()

    @patch("beginning.get_flight_type")
    def test_get_flight_data(self, mock_get_flight_type):
        container = MagicMock()
        parent_name = "ParentName"
        flight_name = "FlightName"
        flight_path = f"{parent_name}/{flight_name}"
        objedt_before_update = {
            "flightPath": flight_path,
            "flightType": None,
            "flightFormat": None,
            "flightName": flight_name,
            "parent": parent_name,
        }
        result = get_flight_data(container, flight_name, parent_name)
        assert objedt_before_update != result
