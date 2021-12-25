
from enum import Enum


class Queue_Selection(Enum):
    """
    Defines the two strategies for selecting the next station
    SQF: Shortest Queue First
    NJF: Earliest Job First (nearest queue)
    """
    SQF="SQF"
    NJF="NJF"