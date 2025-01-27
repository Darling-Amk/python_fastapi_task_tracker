
import enum


# Enum для статуса задачи
class TaskStatus(str, enum.Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"