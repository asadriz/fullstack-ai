import secrets
import string
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation  # Add this import

from django.utils import timezone
from django.utils.dateparse import parse_date

from utils.exceptions.errors import DatesError
from utils.exceptions.exceptions import CoreException


def _to_decimal(value, *, field_name: str) -> Decimal:
    """
    Parse a value into Decimal safely.
    Accepts strings/numbers; raises ValueError on invalid input.
    """
    if value is None or value == "":
        raise ValueError(f"{field_name} is required")

    try:
        # Normalize floats/ints to string first to avoid float precision surprises
        if isinstance(value, (int, float)):
            value = str(value)
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{field_name} must be a valid decimal string")


def parse_start_and_end_dates(start_date_str, end_date_str):
    """
    Input: start_date_str (start date in string format)
           end_date_str (end date in string format)

    Output: start_date and end_date in datetime format parsed
    """
    if not start_date_str or not end_date_str:
        raise CoreException(error=DatesError.BOTH_DATES_REQUIRED_ERROR)

    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError:
        raise CoreException(error=DatesError.INVALID_DATE_FORMAT_ERROR)

    if start_date > end_date:
        raise CoreException(error=DatesError.START_DATE_BEFORE_END_DATE_ERROR)

    return start_date, end_date


def get_dates_range(
    start_date: date, end_date: date, limit_to_current_date: bool = True
):
    # Set end_date to the current date if limit_to_current_date is True
    if limit_to_current_date:
        current_date = datetime.now().date()
        end_date = min(end_date, current_date)

    dates_range = []
    current_date = start_date

    while current_date <= end_date:
        dates_range.append(current_date)
        current_date += timedelta(days=1)
    return dates_range


def generate_cache_key(keys: list) -> str:
    return ":".join(keys)


def break_string_to_list(stringified_list: str, dtype=int) -> list:
    """
    Input: "a,b,c,d"
    Output: ['a','b','c','d']
    If dtype is set to str it will return string array by default it will return integer array
    """
    if stringified_list is None or stringified_list == "":
        return []
    else:
        return list(map(dtype, stringified_list.split(",")))


def sort_list_of_dicts(lst, sort_by) -> list:
    """
    - The function takes a list of dictionaries 'lst' and a sorting key 'sort_by' as arguments.
    - 'sort_by' can start with a '-' to indicate descending order; otherwise, it sorts in ascending order.
    - The 'lst' is sorted in-place based on the specified key.
    - If 'sort_by' starts with '-', the sorting is done in descending order.

    Args:
        lst (list of dict): List of dictionaries to be sorted.
        sort_by (str): The key by which to sort the list. If it starts with a '-', it sorts in descending order; otherwise, in ascending order.

    """
    # Check if the sorting direction is specified as descending (if it starts with '-').
    if sort_by[0] == "-":
        reverse_sort = True
        sort_key = sort_by[1:]  # Remove the '-' to get the key to sort by.
    else:
        reverse_sort = False
        sort_key = sort_by

    # Sort the list of dictionaries based on the specified key.
    # The key parameter of the sort() function is used to determine the sorting order.

    # Here, a lambda function is used to extract the value of the specified key from each dictionary.
    # The lambda function returns a tuple with two elements:
    #   - The first element is a boolean indicating whether the value is None (True for None, False otherwise).
    #   - The second element is the actual value for sorting.

    # When sorting in ascending order, the tuple will ensure that None values come at the end.
    # When sorting in descending order, the reverse parameter is set to True.
    lst.sort(
        key=lambda x: (x.get(sort_key) is None, x.get(sort_key)), reverse=reverse_sort
    )
    return lst


def get_formatted_current_datetime(format="%Y-%m-%d %H:%M:%S") -> str:
    """
    Get the current date and time in the specified format.

    Parameters:
    - format (str): The format string for the date and time. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
    - str: A string representing the current date and time in the specified format.
    """
    return timezone.now().strftime(
        format
    )  # Use datetime module to get current date and time, then format it


def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
