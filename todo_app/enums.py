from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __str__(self):
        names = {
            Priority.LOW: "низкий",
            Priority.MEDIUM: "средний",
            Priority.HIGH: "высокий",
        }
        return names[self]