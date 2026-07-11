from enum import Enum


class LocatorsMatchOptions(Enum):
    EXACT = "="
    CONTAINS = "*="
    STARTS = "^="
    ENDS = "$="
