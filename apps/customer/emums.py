from enum import Enum

class CustomerStatus(Enum):
    VERIFIED = "Verified"
    UNVERIFIED = "Unverified"
    BLOCKED = "Blocked"

    @classmethod
    def choices(cls):
        return [(status.value,status.name.title()) for status in cls]
