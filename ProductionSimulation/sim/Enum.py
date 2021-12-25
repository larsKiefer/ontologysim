from enum import Enum


class Machine_Enum(Enum):
    """
    Enum for Machine, defines the different states
    """
    Defect = "MachineDefect"
    SetUp = "SetUp"
    Wait = "Wait_Machine"
    Process = "Process"


class Queue_Enum(Enum):
    """
    Enum for Queue, defines the different change types
    """
    Change = "Change"
    AddToTransporter = "AddToTransporter"
    RemoveFromTransporter = "RemoveFromTransporter"
    StartProcess = "StartProcess"
    StartProcessStayBlocked = "StartProcessStayBlocked"
    EndProcess = "EndProcess"
    Default = "Default"
    RemoveFromTransporterDeadlock = "RemoveFromTransporterDeadlock"
    StartOfProduction="StartOfProduction"


class Transporter_Enum(Enum):
    """
    Enum for transporter, defines all states of transporter
    """
    Defect = "TransporterDefect"
    Wait = "Wait_Transport"
    Transport = "Transport"


class Evaluate_Enum(Enum):
    """
    Enum for evaluation, defines which onto category gets evaluated
    """
    Machine = "Machine"
    Transporter = "Transporter"
    Product = "Product"
    OrderRelease = "OrderRelease"
    ProductFinished = "ProductFinished"
    TransporterDefect = "EvTransporterDefect"
    MachineDefect = "EvMachineDefect"


class OrderRelease_Enum(Enum):
    """
    Enum for order release, defines the states for order release
    """
    Release = "Release"


class Product_Enum(Enum):
    """
    Enum for Product, defines the states of product
    """
    Wait = "Wait"
    Defect = "Defect"
    Transport = "Transport"
    Process = "Process"
    EndBlockForTransporter = "EndBlockForTransporter"



class Defect_Type_Enum(Enum):
    """
    Enum for defect, defines the type of defect
    """
    Short = "short"
    Medium = "medium"
    Long = "long"


class Label(Enum):
    """
    is part of the id/name of the enum instance
    each onto name starts with one of these labels
    """
    Transporter = "t"
    Machine = "m"
    Distribution = "d"
    NormalDistribution = "normald"
    RandomDistribution = "randomd"
    Location = "l"
    Product = "p"
    Queue = "q"
    ProductType = "p_t"
    Position = "po"
    Process = "pr"
    ProdProcess ="ppr"
    ProdTypeProcess = "ptpr"
    State = "state"
    Event = "e"
    LoggerEvent = "logger_e"
    EventList = "e_l"
    StartQueue = "start_q"
    EndQueue = "end_q"
    SetUp = "setup"
    SimCore = "sim_core"
    ShortTermLogger = "short_term_logger"
    Task = "task"
    DeadlockQueue = "deadlock_q"
    Logger = "logger"
    Defect = "defect"
    SubDefect = "sub_defect"
    MachineService = "machine_service"
    MachineServiceOperator = "machine_service_operator"
    TransporterService = "transport_service"
    TransporterServiceOperator = "transport_service_operator"
    CombineProcessData = "combine_process_data"
