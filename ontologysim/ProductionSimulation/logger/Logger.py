import ast
import math
import shutil

from ontologysim.ProductionSimulation.database.models.SimulationFacts import SimulationFacts
from ontologysim.ProductionSimulation.database.models.SimulationRun import SimulationRun
from ontologysim.ProductionSimulation.database.models.User import User
from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Enum, Folder_name, Logger_Type_Enum
from ontologysim.ProductionSimulation.logger.MachineLogger import MachineLogger
from ontologysim.ProductionSimulation.logger.ProductAnalyseLogger import ProductAnalyseLogger
from ontologysim.ProductionSimulation.logger.QueueFillLevelLogger import QueueFillLevelLogger
from ontologysim.ProductionSimulation.logger.SimLogger import SimLogger
from ontologysim.ProductionSimulation.logger.TransporterDistributionLogger import TransporterDistributionLogger
from ontologysim.ProductionSimulation.logger.TransporterLocationLogger import TransporterLocationLogger
from ontologysim.ProductionSimulation.logger.TransporterLogger import TransporterLogger
from ontologysim.ProductionSimulation.logger.plot.Plot import Plot
from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum, Queue_Enum, Transporter_Enum, OrderRelease_Enum, Evaluate_Enum
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest
import datetime
import os


class Logger:
    """
    main class for the kpi logger, all information or inputs are handled by the logger,
    the subloggers  are then responsible for evaluating and calculating the kpis
    """

    def __init__(self, simCore):
        """
        defines which logger is used for which event

        :param simCore:
        """
        self.simCore = simCore
        self.dataBase = None

        self.machineLogger = MachineLogger(self)
        self.queueFillLevelLogger = QueueFillLevelLogger(self)
        self.transporterLogger = TransporterLogger(self)
        self.productAnalyseLogger = ProductAnalyseLogger(self)
        self.simLogger = SimLogger(self)
        self.transporterLocationLogger = TransporterLocationLogger(self)

        self.transporterDistributionLogger = TransporterDistributionLogger(self)
        self.transform_event_type_in_log_type = {}
        self.transform_event_type_in_log_type[Queue_Enum.Change.value] = [self.queueFillLevelLogger,
                                                                          self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.AddToTransporter.value] = [self.queueFillLevelLogger,
                                                                                    self.transporterLogger,
                                                                                    self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.RemoveFromTransporter.value] = [self.queueFillLevelLogger,
                                                                                         self.transporterLogger,
                                                                                         self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.StartProcess.value] = [self.queueFillLevelLogger,
                                                                                self.machineLogger,
                                                                                self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.EndProcess.value] = [self.queueFillLevelLogger,
                                                                              self.machineLogger,
                                                                              self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.Default.value] = [self.queueFillLevelLogger,
                                                                           self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.StartOfProduction.value] = [self.productAnalyseLogger]
        self.transform_event_type_in_log_type[Queue_Enum.RemoveFromTransporterDeadlock.value] = [
            self.queueFillLevelLogger, self.productAnalyseLogger, self.transporterLogger]
        self.transform_event_type_in_log_type[Queue_Enum.StartProcessStayBlocked.value] = [self.queueFillLevelLogger,
                                                                                           self.machineLogger,
                                                                                           self.productAnalyseLogger]

        self.transform_event_type_in_log_type[Transporter_Enum.Defect.value] = [self.transporterLogger]
        self.transform_event_type_in_log_type[Transporter_Enum.Wait.value] = [self.transporterLogger]
        self.transform_event_type_in_log_type[Transporter_Enum.Transport.value] = [self.transporterLogger,
                                                                                   self.transporterDistributionLogger,
                                                                                   self.transporterLocationLogger]

        self.transform_event_type_in_log_type[OrderRelease_Enum.Release.value] = [self.simLogger,
                                                                                  self.productAnalyseLogger]

        self.transform_event_type_in_log_type[Machine_Enum.Wait.value] = [self.machineLogger]
        self.transform_event_type_in_log_type[Machine_Enum.Defect.value] = [self.machineLogger]
        self.transform_event_type_in_log_type[Machine_Enum.SetUp.value] = [self.machineLogger]
        self.transform_event_type_in_log_type[Machine_Enum.Process.value] = [self.machineLogger,
                                                                             self.productAnalyseLogger]

        self.transform_event_type_in_log_type[Evaluate_Enum.ProductFinished.value] = [self.productAnalyseLogger,
                                                                                      self.simLogger]

        self.create_new_folder_name = True
        #default
        self.output_path = "ontologysim/example/log/"
        self.time_intervall=100

        self.start_time_logging = 0
        self.end_time_logging = 0
        self.start_logging = False
        self.end_logging = False
        self.logging_activated = False

        self.simulationRunDB = None

        self.plot = Plot(self)

    def setStartLogger(self, time):
        """
        sets the start of the logging

        :param time: double
        """
        print("start_logger", time)
        self.start_time_logging = time
        self.start_logging = True
        self.machineLogger.start_logging_multiple = math.floor(
            self.start_time_logging / self.time_intervall)
        self.machineLogger.setTTFlastValue(self.start_time_logging)
        self.transporterLogger.start_logging_multiple = math.floor(
            self.start_time_logging / self.time_intervall)
        self.transporterLogger.setTTFlastValue(self.start_time_logging)
        self.productAnalyseLogger.start_logging_multiple = math.floor(
            self.start_time_logging / self.time_intervall)
        self.productAnalyseLogger.setLastWIP(self.start_time_logging)
        self.simLogger.start_logging_multiple = math.floor(self.start_time_logging / self.time_intervall)
        self.simLogger.last_time = self.start_time_logging
        self.simLogger.setLastWIP()

        self.queueFillLevelLogger.start_logging_multiple = math.floor(
            self.start_time_logging / self.time_intervall)
        self.queueFillLevelLogger.setQueueSize(time)

        self.transporterDistributionLogger.start_logging_multiple = math.floor(
            self.start_time_logging / self.time_intervall)

        min_logger_interval = min([self.time_intervall, self.time_intervall,
                                   self.time_intervall, self.time_intervall])
        self.plot.time_intervall = min_logger_interval
        self.plot.start_logging_multiple = math.floor(self.start_time_logging / min_logger_interval)
        self.plot.startPlot(time)


    def initLogger(self, log_conf):
        """
        initialise the logger and defines what to log

        :param logger_config_path: dict
        :return:
        """
        self.kpi_configs= log_conf["KPIs"]
        self.ini_config=log_conf['ConfigIni']
        self.save_config = log_conf['Save']
        self.time_intervall =  self.kpi_configs["time_interval"]

        self.logging_activated = True
        summary_event_list=self.kpi_configs["log_summary"]
        time_event_list=self.kpi_configs["log_time"]

        if(Logger_Enum.SimLogger.value in summary_event_list and Logger_Enum.ProductLogger.value not in summary_event_list and Logger_Enum.MachineLogger.value not in summary_event_list):
            raise Exception("add "+Logger_Enum.ProductLogger.value+" to log_summary list")
        if(Logger_Enum.SimLogger.value in time_event_list and Logger_Enum.ProductLogger.value not in time_event_list and Logger_Enum.MachineLogger.value not in time_event_list):
          raise Exception("add "+Logger_Enum.ProductLogger.value+" and "+ Logger_Enum.MachineLogger.value+" to log_time list")

        log_type_dict={}
        for element in Logger_Enum:
            log_type_dict[element.value] = self.getLoggerType(element.value,summary_event_list,time_event_list)

        self.machineLogger.initSubLogger(log_type_dict)
        self.queueFillLevelLogger.initSubLogger(log_type_dict)
        self.transporterLogger.initSubLogger(log_type_dict)
        self.transporterDistributionLogger.initSubLogger(log_type_dict)
        self.transporterLocationLogger.initSubLogger(log_type_dict)
        self.productAnalyseLogger.initSubLogger(log_type_dict)
        self.simLogger.initSubLogger(log_type_dict)

        if self.save_config["csv"]:
            self.output_path = self.save_config["path"]
        else:
            self.output_path = None

        self.createPath()



    def getLoggerType(self,enum_value,summary_list,time_list):
        """
        define logger type, if summary and or time or nothing
        :param enum_value:
        :param summary_list:
        :param time_list:
        :return: string
        """
        type=""
        if (enum_value in time_list and enum_value in summary_list):
            type = Logger_Type_Enum.All.value
        elif(enum_value in time_list):
            type = Logger_Type_Enum.Time.value
        elif(enum_value in summary_list):
            type=Logger_Type_Enum.Summary.value
        else:
            type=Logger_Type_Enum.Not.value

        return type

    def evaluatedInformations(self, dict_list):
        """
        main class for the logger, interface for the simulation calsses to log some informations

        :param dict_list: [dict{},..]
        :return:
        """
        if self.start_logging == True:

            for dict_element in dict_list:

                event_type = dict_element['type']

                for sub_logger in self.transform_event_type_in_log_type[event_type]:
                    sub_logger.addElement(dict_element)

    def finale_evaluate(self, time):
        """
        when logging is finished, a finale logging have to be done

        :param time:
        """
        if self.logging_activated:
            self.machineLogger.finale_evaluate(time)
            self.transporterLogger.finale_evaluate(time)
            self.productAnalyseLogger.finale_evaluate(time)
            self.simLogger.finale_evaluate(time)
            self.queueFillLevelLogger.finale_evaluate(time)
            self.transporterDistributionLogger.finale_evaluate(time)
            self.transporterLocationLogger.finale_evaluate(time)
        self.end_time_logging = time

    def create_output(self):
        """
        main class for saving the information, calls the sub logger

        :return:
        """
        if not self.logging_activated:
            return

        self.saveInformation()
        self.queueFillLevelLogger.save(self.output_path, Folder_name.queue.value, "queue_logger")
        self.machineLogger.save(self.output_path, Folder_name.machine.value, "machine_logger")
        self.transporterLogger.save(self.output_path, Folder_name.transporter.value, "transporter_logger")
        self.simLogger.save(self.output_path, Folder_name.sim.value, "sim_logger")
        self.productAnalyseLogger.save(self.output_path, Folder_name.product.value, "product_logger")
        self.transporterDistributionLogger.save(self.output_path, Folder_name.transporter_distribution.value, "transporter_distribution_logger")
        self.transporterLocationLogger.save(self.output_path,Folder_name.transporter_location.value,"transporter_location_logger")

        self.addIni(self.output_path)

        self.commitDB()

    def commitDB(self):
        """
        commit DB, add cache to database
        :return:
        """

        if self.save_config["database"]:
            self.dataBase.session.commit()

    def createPath(self):
        """
        create new folder and save all_events
        :return:
        """
        if self.save_config["csv"]:
            path = PathTest.check_dir_path(self.output_path)
            if self.create_new_folder_name:

                number_of_machines = len(self.simCore.onto.search(type=self.simCore.central.machine_class))
                number_of_transporter = len(self.simCore.onto.search(type=self.simCore.central.transporter_class))
                now = datetime.datetime.now()
                folder_name = now.strftime("%m%d%Y_%H-%M-%S") + "_" + str(number_of_machines) + "_" + str(
                    number_of_transporter)

                newpath = path + folder_name + "/"
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                path = PathTest.check_dir_path(newpath)

                if self.kpi_configs['log_events']:

                    folder_name = Folder_name.events.value
                    newpath = path + folder_name + "/"
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    event_path = PathTest.check_dir_path(newpath)
                    self.simCore.event_logger.path_csv = event_path + 'all_events.csv'
            else:
                event_path = path
                if self.kpi_configs['log_events']:
                    self.simCore.event_logger.path_csv = event_path + "all_events.csv"
            self.output_path = path

    def saveInformation(self):
        """
        save simulationfact in database after simulation run
        :return:
        """


        if self.save_config["database"]:
            user = None
            if(self.simCore.run_as_api):
                #TODO adding user
                pass

            else:
                with open( PathTest.check_file_path("/ontologysim/ProductionSimulation/database/defaultUser.json"), "r") as f:
                    userJSON = ast.literal_eval(f.read())
                user = self.dataBase.session.query(User).filter_by(userName=userJSON["userName"]).first()

                if(not user):
                    raise Exception("default user not defined")



            self.simulationRunDB = SimulationRun(start= datetime.datetime.now())
            user.simulationRuns.append(self.simulationRunDB)
            self.dataBase.session.add(self.simulationRunDB)

            if("all" in self.productAnalyseLogger.number_of_products.keys() and "all"  in self.simLogger.summarized_kpis):
                simulationFact = SimulationFacts(numberOfParts = self.productAnalyseLogger.number_of_products['all'],loggingTime=self.simLogger.summarized_kpis['all']['logging_time'],simulationTime=self.simCore.getCurrentTimestep())
            else:
                simulationFact = SimulationFacts(numberOfParts=None,
                                                 loggingTime=(self.simCore.getCurrentTimestep() - self.start_time_logging),
                                                 simulationTime=self.simCore.getCurrentTimestep())

            self.dataBase.session.add(simulationFact)
            self.simulationRunDB.simulationFacts = simulationFact




    def addIni(self,path):
        """
        copying the ini folder with all the configs to the log folder

        :param path:
        """

        if self.ini_config['addini']:
            ini_dir=self.ini_config['path']
            ini_dir=PathTest.check_dir_path(ini_dir)
            onlyfiles = [f for f in os.listdir(ini_dir) if os.path.isfile(os.path.join(ini_dir, f))]

            folder_name="_ini"
            newpath_queue = path + folder_name + "/"
            if not os.path.exists(newpath_queue):
                os.makedirs(newpath_queue)
            path_folder = PathTest.check_dir_path(newpath_queue)
            for file in onlyfiles:
                shutil.copy(ini_dir+file, path_folder+file)


    def setDataBase(self,dataBase):
        """
        add database
        :param dataBase: database object
        :return:
        """
        self.dataBase = dataBase