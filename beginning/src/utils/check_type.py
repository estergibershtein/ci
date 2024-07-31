from dotenv import load_dotenv

from utils.const import FlightFormat, FlightType, DataFlight
from azure_operations.azure_connection import AzureContainer
from utils.azLogger import create_logger

load_dotenv()
logger = create_logger(__name__)


def get_flight_type(container: AzureContainer, flight_folder: str):
    try:
        flight_files = container.get_files_from_folder(flight_folder)
        folder_list = container.get_contents_of_folder_without_depth_layers(flight_folder)

        flight_type = check_flight_type(flight_files, flight_folder)
        flight_format = FlightFormat.ONE.value

        if flight_type == FlightType.NAVAD.value:
            flight_format = check_navad_flight_format(flight_folder, folder_list)
        return DataFlight(flight_type=flight_type, flight_format=flight_format)

    except Exception as error:
        logger.error(f"Error getting flight type for flight {flight_folder} - {error}")
        raise ValueError(f"Error getting flight type for flight {flight_folder} - {error}")


def check_flight_type(flight_files: dict, flight_folder: str) -> str:
    if check_image_suffix(flight_files, ".raw"):
        return FlightType.NAVAD.value
    if check_image_suffix(flight_files, ".iiq"):
        return FlightType.TELEM.value
    raise ValueError(f"Error checking flight type for flight {flight_folder}")


def check_image_suffix(files: dict, suffix: str):
    return any(file.lower().endswith(suffix) for file in files)


def check_navad_flight_format(flight_folder: str, folder_list: list) -> str:
    if is_all_flight(flight_folder):
        return FlightFormat.ALL
    if is_one_flight(folder_list):
        return FlightFormat.ONE
    if is_merge_flight(folder_list):
        return FlightFormat.MERGE
    raise ValueError(f"Error checking flight format for flight {flight_folder}")


def is_all_flight(flight_folder: str):
    return flight_folder.lower().endswith((FlightFormat.ALL.value.lower()))


def is_one_flight(folder_list: list):
    count_input_folders, count_misc_folders = count_misc_input_folders(folder_list)
    return count_input_folders == count_misc_folders == 1


def is_merge_flight(folder_list: list):
    count_input_folders, count_misc_folders = count_misc_input_folders(folder_list)
    return count_input_folders > 1 and count_misc_folders > 1


def count_misc_input_folders(folder_list: list):
    count_input_folders = count_folders_by_name(folder_list, "input")
    count_misc_folders = count_folders_by_name(folder_list, "misc")
    return count_input_folders, count_misc_folders


def count_folders_by_name(folder_list: dict, name: str):
    return len([folder_name for folder_name in folder_list if name in folder_name.lower()])
