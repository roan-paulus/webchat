import itertools
import re


RESERVED_NAME_START = "User"
RESERVED_NAME_PATTERN = re.compile(RESERVED_NAME_START + r"\d+")


def reserved_name_generator():
    for n in itertools.count(start=1):
        yield f"{RESERVED_NAME_START}{n}"


def is_name_reserved(name: str) -> bool:
    return bool(RESERVED_NAME_PATTERN.match(name))

