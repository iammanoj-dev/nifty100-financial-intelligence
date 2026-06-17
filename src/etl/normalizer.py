import re


def normalize_ticker(ticker):
    """
    Convert ticker to uppercase and remove spaces.
    """

    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_year(year_value):
    """
    Convert:
    Mar-23 -> 2023-03
    Dec-22 -> 2022-12
    """

    if year_value is None:
        return None

    year_value = str(year_value).strip()

    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    match = re.match(r"([A-Za-z]{3})-(\d{2})", year_value)

    if not match:
        return year_value

    month = month_map[match.group(1)]
    year = "20" + match.group(2)

    return f"{year}-{month}"
