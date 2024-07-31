from azure_operations.azure_connection import AzureConnection
from azure_operations.azure_container import AzureContainer

from utils.const import AzureConfig


def get_container(flight_name: str) -> AzureContainer:
    azure_connection = AzureConnection(AzureConfig.CONNECTION_STRING)
    container = azure_connection.get_azure_container(flight_name)
    return container
