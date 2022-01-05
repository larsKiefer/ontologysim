from enum import Enum


class Logger_Enum(Enum):
    """
    Logger enum
    """

    MachineLogger="machine"
    ProductLogger="product"
    AllProductsLogger="all_products"
    QueueFillLevelLogger="queue"
    TransporterLogger="transporter"
    TransporterDistributionLogger="transporter_distribution"
    TransporterLocationLogger="transporter_location"
    SimLogger="sim"

class Logger_Type_Enum(Enum):
    """
    defines type of logging
    """
    All="all"
    Time="time"
    Summary="summary"
    Not="not"

class Folder_name(Enum):
    """
    defines the folder name for the logger
    """
    machine = "machine"
    ini = "_ini"
    product = "product"
    queue = "queue"
    events = "events"
    sim = "sim"
    transporter = "transporter"
    transporter_distribution = "transporter_distribution"
    transporter_location = "transporter_location"