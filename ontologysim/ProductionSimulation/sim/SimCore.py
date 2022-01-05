import logging

from owlready2 import *

from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum, Label, Evaluate_Enum, Queue_Enum, Transporter_Enum, \
    OrderRelease_Enum, Product_Enum
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest


class SimCore:
    """
    main class, connection point for all side classes
    """
    prefixString = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX ns: <http://test.org/onto.owl#>"""

    def __init__(self):
        """

        """
        self.onto = owlready2.get_ontology("http://test.org/onto.owl")

        self.currentRunID = ""
        self.data_base = None

        self.machine_id = 0
        self.queue_id = 0
        self.position_id = 0
        self.prod_process_id = 0
        self.prod_type_process_id = 0
        self.process_id = 0
        self.state_id = 0
        self.combine_process_data_id = 0
        self.product_id = 0
        self.event_id = 0
        self.product_type_id = 0
        self.distribution_id = 0
        self.location_id = 0
        self.transport_id = 0
        self.set_up_id = 0
        self.task_id = 0
        self.sub_defect_id = 0
        self.defect_id = 0
        self.machine_service_id = 0
        self.machine_service_operator_id = 0
        self.transporter_service_id = 0
        self.transporter_service_operator_id = 0

        self.machine = None
        self.queue = None
        self.product = None
        self.product_type = None
        self.transport = None
        self.task = None
        self.order_release = None
        self.defect = None
        self.repair_service_machine = None
        self.repair_service_transporter = None
        self.event = None
        self.distribution = None
        self.location = None
        self.central = None
        self.event_logger = None
        self.logger = None
        self.event_utilities = None
        self.prod_process = None
        self.process = None
        self.position = None
        self.state = None

        self.run_as_api=False
        self.stateStorage=None
        self.changeStorageState=False

        self.save_time = -1

        self.random_seed_add_value = 0

        self.db=None

        self.end = False

    def destroyOnto(self):
        """
        destroys the complete onto, important for restart
        """

        self.onto._destroy_cached_entities()
        logging.info("_destroy_cached_entities")

        self.onto.destroy()
        logging.info("destroyed")

        self.onto = None


    def setRandomSeedAddValue(self, value):
        """
        sets the random seed add value

        :param value: int
        """
        self.random_seed_add_value = value

    def set_save_time(self, save_time):
        """
        sets the time, where the ontology should be saved to owl

        :param save_time: double
        """
        self.save_time = save_time


    def save_ontology(self,path="/ontologysim/example/owl/test.owl"):
        """
        saves the ontology to owl-file

        :param path:
        """
        self.onto.save(file=PathTest.check_dir_path(path), format="rdfxml")

    def createSimInstance(self):
        """
        creates sim instance in onto and sets time to 0
        """
        self.central.simInstance = self.central.sim_class(Label.SimCore.value + "0")
        self.central.simInstance.current_timestep = 0
        self.central.simInstance.allStartTasksFinished = False
        self.central.simInstance.allLoggingTasksFinished = False
        self.number_of_finshed_products = 0

    def main(self):
        """
        main method which is used while running simulation
        """


        self.run = True

        self.order_release.orderReleaseController.evaluateCreateOrderRelease()

        while (self.run):
            self.runNextEvent()

        time = self.getCurrentTimestep()
        self.logger.finale_evaluate(time)

        """
        self.logger.machineLogger.test_object_name_all()
        self.logger.transporterLogger.test_object_name_all()
        #self.logger.simLogger.test_object_name_all()
        #self.logger.productAnalyseLogger.test_object_name_all()
        self.logger.machineLogger.test_time_summary()
        self.logger.transporterLogger.test_time_summary()
        self.logger.productAnalyseLogger.test_time_summary()
        #self.logger.simLogger.test_time_summary()
        """

    def runNextEvent(self):
        """
        calculates next event and for every event type the necessaries steps are introduced

        :return: [event_onto]
        """
        event_onto, event_type = self.event.getNextEvent()
        self.setCurrentTimeStep(event_onto.time)

        event_list=[]

        if event_onto.time >= self.save_time and self.save_time >= 0:
            self.save_ontology()
            sys.exit()

        #self.event.getNumberOfEvents()
        if event_onto == None:
            self.run = False
            return

        if self.run_as_api:
            event_list = self.event_utilities.transfromEventOntoToList(event_onto)

        if (self.changeStorageState):
            self.stateStorage.changeState(event_onto)


        #print([self.event_utilities.transfromEventOntoToList(event_onto) for event_onto in self.onto[Label.EventList.value + "0"].has_for_event])
        #print([self.event_utilities.transfromEventOntoToList(event_onto) for event_onto in self.onto[Label.ShortTermLogger.value +"0"].has_for_event_short_term_logger])


        if event_type == Evaluate_Enum.Machine.value:
            if not self.machine.evaluateDefect(event_onto):
                self.machine.machineController.evaluateMachine(event_onto)
        elif event_type == Evaluate_Enum.Product.value:
            raise Exception("event type currently not implemented")
        elif event_type == Evaluate_Enum.Transporter.value:

            if not self.transport.evaluateDefect(event_onto):
                self.transport.transportController.evaluateTransport(event_onto)
        elif event_type == Evaluate_Enum.ProductFinished.value:
            self.product.evaluateFinishedProduct(event_onto)
        elif event_type == Evaluate_Enum.OrderRelease.value:
            self.order_release.orderReleaseController.evaluateOrderRelease(event_onto)
        elif event_type == Machine_Enum.Defect.value:
            self.repair_service_machine.repair(event_onto)
        elif event_type == Machine_Enum.SetUp.value:
            self.machine.set_up(event_onto)
        elif event_type == Machine_Enum.Wait.value:
            self.machine.wait(event_onto)
        elif event_type == Machine_Enum.Process.value:
            self.machine.process(event_onto)
        elif event_type == Queue_Enum.Change.value:
            self.queue.change(event_onto)
        elif event_type == Transporter_Enum.Defect.value:
            self.repair_service_transporter.repair(event_onto)
        elif event_type == Transporter_Enum.Transport.value:
            self.transport.transport(event_onto)
        elif event_type == Transporter_Enum.Wait.value:
            self.transport.wait(event_onto)
        elif event_type == OrderRelease_Enum.Release.value:
            self.order_release.release(event_onto)
        elif event_type == Evaluate_Enum.TransporterDefect.value:
            self.repair_service_transporter.serviceController.evaluateService(event_onto)
        elif event_type == Evaluate_Enum.MachineDefect.value:
            self.repair_service_machine.serviceController.evaluateService(event_onto)
        elif event_type == Product_Enum.EndBlockForTransporter.value:
            self.product.endBlockForTransporter(event_onto)
        else:
            raise Exception("event type does not exist: " + str(event_type) + ", " + str(event_onto))

        self.logger.plot.update_plot(self.getCurrentTimestep())

        if self.end == True:
            self.run = False



        return event_list

    def createOWLStructure(self):
        """
        owl classes, methods, attributes
        """

        with self.onto:
            '''
            for element in classesList:
                types.new_class(element,(Thing,))
            '''

            class Sim(owlready2.Thing): pass

            class number_of_finshed_products(Sim >> int, owlready2.FunctionalProperty): pass

            class current_timestep(Sim >> float, owlready2.FunctionalProperty): pass

            class allStartTasksFinished(Sim >> bool, owlready2.FunctionalProperty): pass

            class allLoggingTasksFinished(Sim >> bool, owlready2.FunctionalProperty): pass

            class Transporter(owlready2.Thing): pass

            class transporter_waiting_time(Transporter >> float, owlready2.FunctionalProperty): pass

            class start_current_location(Transporter >> float, owlready2.FunctionalProperty): pass

            class speed(Transporter >> float, owlready2.FunctionalProperty): pass

            class route_type(Transporter >> str, owlready2.FunctionalProperty): pass

            class Queue(owlready2.Thing): pass

            class Location(owlready2.Thing): pass

            class x(Location >> float, owlready2.FunctionalProperty): pass

            class y(Location >> float, owlready2.FunctionalProperty): pass

            class z(Location >> float, owlready2.FunctionalProperty): pass

            class TodoQueue(Queue): pass

            class TranspQueue(Queue): pass

            class InputQueue(Queue): pass

            class OutputQueue(Queue): pass

            class EndQueue(Queue): pass

            class current_size(Queue >> int, owlready2.FunctionalProperty): pass

            class size(Queue >> int, owlready2.FunctionalProperty): pass

            class Product(owlready2.Thing): pass

            class Task(owlready2.Thing): pass

            class number(Task >> int, owlready2.FunctionalProperty): pass

            class todo_number(Task >> int, owlready2.FunctionalProperty): pass

            class due_date(Product >> float, owlready2.FunctionalProperty): pass

            class start_time(Task >> float, owlready2.FunctionalProperty): pass

            class task_type(Task >> str, owlready2.FunctionalProperty): pass

            # python_name = "cost"
            class blocked_for_transporter(Product >> float, owlready2.FunctionalProperty): pass

            class blocked_for_machine(Product >> float, owlready2.FunctionalProperty): pass

            class marking(Product >> str, owlready2.FunctionalProperty): pass

            class start_of_production_time(Product >> float, owlready2.FunctionalProperty): pass

            class end_of_production_time(Product >> float, owlready2.FunctionalProperty): pass

            class queue_input_time(Product >> float, owlready2.FunctionalProperty): pass

            class SubProduct(owlready2.Thing): pass

            class has_for_sub_product(owlready2.ObjectProperty):
                domain = [SubProduct]
                range = [SubProduct]

            class is_sub_product_of(owlready2.ObjectProperty):
                domain = [SubProduct]
                range = [SubProduct]
                inverse_property = has_for_sub_product

            class start_of_sub_production_time(SubProduct >> float, owlready2.FunctionalProperty): pass

            class end_of_sub_production_time(SubProduct >> float, owlready2.FunctionalProperty): pass

            class sub_product_type(SubProduct >> str, owlready2.FunctionalProperty): pass


            class ProductType(owlready2.Thing): pass

            class has_for_product_type(owlready2.ObjectProperty):
                domain = [Product]
                range = [ProductType]

            class is_product_of(owlready2.ObjectProperty):
                domain = [ProductType]
                range = [Product]
                inverse_property = has_for_product_type

            class sum_number_of_products(ProductType >> float, owlready2.FunctionalProperty): pass

            class planned_number_of_products(ProductType >> float, owlready2.FunctionalProperty): pass

            class str_number_of_products(ProductType >> str, owlready2.FunctionalProperty): pass

            class pnml(ProductType >> str, owlready2.FunctionalProperty): pass

            class has_for_product_type_task(owlready2.ObjectProperty):
                domain = [Task]
                range = [ProductType]

            class ProdProcess(owlready2.Thing): pass

            class Machine(owlready2.Thing): pass

            class machine_waiting_time(Machine >> float, owlready2.FunctionalProperty): pass

            class has_for_last_process(owlready2.ObjectProperty):
                domain = [Machine]
                range = [ProdProcess]

            class Distribution(owlready2.Thing): pass

            class seed(Distribution >> int, owlready2.FunctionalProperty): pass

            class distribution_type(Distribution >> str, owlready2.FunctionalProperty): pass

            class RandomDistribution(Distribution): pass

            class min_value(RandomDistribution >> int, owlready2.FunctionalProperty): pass

            class max_value(RandomDistribution >> int, owlready2.FunctionalProperty): pass

            class NormalDistribution(Distribution): pass

            class mean(NormalDistribution >> float, owlready2.FunctionalProperty): pass

            class deviation(NormalDistribution >> float, owlready2.FunctionalProperty): pass

            class has_for_add_time(owlready2.ObjectProperty):
                domain = [Queue]
                range = [Distribution]

            class has_for_remove_time(owlready2.ObjectProperty):
                domain = [Queue]
                range = [Distribution]

            class Position(owlready2.Thing): pass

            class blockedSpace(Position >> float, owlready2.FunctionalProperty): pass

            class has_for_product(owlready2.ObjectProperty):
                domain = [Position]
                range = [Product]

            class is_position_of(owlready2.ObjectProperty):
                domain = [Product]
                range = [Position]
                inverse_property = has_for_product

            class SetUp(owlready2.Thing): pass


            class has_for_start_process(owlready2.ObjectProperty):
                domain = [SetUp]
                range = [ProdProcess]

            class is_start_process_of(owlready2.ObjectProperty):
                domain = [ProdProcess]
                range = [SetUp]
                inverse_property = has_for_start_process

            class has_for_end_process(owlready2.ObjectProperty):
                domain = [SetUp]
                range = [ProdProcess]

            class is_end_process_of(owlready2.ObjectProperty):
                domain = [ProdProcess]
                range = [SetUp]
                inverse_property = has_for_end_process

            class has_for_set_up_distribution(owlready2.ObjectProperty):
                domain = [SetUp]
                range = [Distribution]

            class has_for_prod_distribution(owlready2.ObjectProperty):
                domain = [ProdProcess]
                range = [Distribution]

            class has_for_set_up(owlready2.ObjectProperty):
                domain = [Machine]
                range = [SetUp]

            class is_set_up_of(owlready2.ObjectProperty):
                domain = [SetUp]
                range = [Machine]
                inverse_property = has_for_set_up

            class EventList(owlready2.Thing): pass

            class ShortTermLogger(EventList): pass

            class Logger(owlready2.Thing): pass

            class Event(owlready2.Thing): pass

            class waiting_time(Event >> float, owlready2.FunctionalProperty): pass

            class time_diff(Event >> float, owlready2.FunctionalProperty): pass

            class time(Event >> float, owlready2.FunctionalProperty): pass

            class type(Event >> str, owlready2.FunctionalProperty): pass

            class number_of_products(Event >> int, owlready2.FunctionalProperty): pass

            class additional_type(Event >> str, owlready2.FunctionalProperty): pass

            class EventOfLogger(owlready2.Thing): pass

            class time_logger(EventOfLogger >> float, owlready2.FunctionalProperty): pass

            class type_logger(EventOfLogger >> str, owlready2.FunctionalProperty): pass

            class additional_type_logger(EventOfLogger >> str, owlready2.FunctionalProperty): pass

            class number_of_products_logger(Event >> int, owlready2.FunctionalProperty): pass

            class time_diff_logger(EventOfLogger >> float, owlready2.FunctionalProperty): pass

            class has_for_task_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Task]

            class has_for_task_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Task]

            class is_task_of(owlready2.ObjectProperty):
                domain = [Task]
                range = [Event]
                inverse_property = has_for_task_event

            class has_for_todo_queue(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [TodoQueue]

            class is_todo_queue_of(owlready2.ObjectProperty):
                domain = [TodoQueue]
                range = [Transporter]
                inverse_property = has_for_todo_queue

            class has_for_transp_queue(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [TranspQueue]

            class is_transp_queue_of(owlready2.ObjectProperty):
                domain = [TranspQueue]
                range = [Transporter]
                inverse_property = has_for_transp_queue

            class has_for_input_queue(owlready2.ObjectProperty):
                domain = [Machine]
                range = [InputQueue]

            class has_for_output_queue(owlready2.ObjectProperty):
                domain = [Machine]
                range = [OutputQueue]

            class has_for_queue_process(owlready2.ObjectProperty):
                domain = [Machine]
                range = [Queue]

            class is_for_queue_process_of(owlready2.ObjectProperty):
                domain = [Queue]
                range = [Machine]
                inverse_property = has_for_queue_process

            class is_input_queue_of(owlready2.ObjectProperty):
                domain = [InputQueue]
                range = [Machine]
                inverse_property = has_for_input_queue

            class is_output_queue_of(owlready2.ObjectProperty):
                domain = [OutputQueue]
                range = [Machine]
                inverse_property = has_for_output_queue

            class has_for_position(owlready2.ObjectProperty):
                domain = [Queue]
                range = [Position]

            class is_queue_of(owlready2.ObjectProperty):
                domain = [Position]
                range = [Queue]
                inverse_property = has_for_position

            class has_for_event(owlready2.ObjectProperty):
                domain = [EventList]
                range = [Event]

            class is_event_list_of(owlready2.ObjectProperty):
                domain = [Event]
                range = [EventList]
                inverse_property = has_for_event

            class has_for_event_short_term_logger(owlready2.ObjectProperty):
                domain = [ShortTermLogger]
                range = [Event]

            class has_for_event_of_logger(owlready2.ObjectProperty):
                domain = [Logger]
                range = [EventOfLogger]

            class is_event_short_term_logger_of(owlready2.ObjectProperty):
                domain = [Event]
                range = [ShortTermLogger]
                inverse_property = has_for_event_short_term_logger

            class is_event_of_logger_of(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Logger]
                inverse_property = has_for_event_of_logger

            class has_for_machine_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Machine]

            class has_for_machine_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Machine]

            class has_for_position_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Position]

            class has_for_position_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Position]

            class is_position_event_of(owlready2.ObjectProperty):
                domain = [Position]
                range = [Event]
                inverse_property = has_for_position_event

            class is_machine_event_of(owlready2.ObjectProperty):
                domain = [Machine]
                range = [Event]
                inverse_property = has_for_machine_event

            class has_for_location_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Location]

            class has_for_location_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Location]

            class is_location_event_of(owlready2.ObjectProperty):
                domain = [Location]
                range = [Event]
                inverse_property = has_for_location_event

            class is_transport_event_of(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [Event]

            class is_product_event_of(owlready2.ObjectProperty):
                domain = [Product]
                range = [Event]

            class has_for_transport_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Transporter]
                inverse_property = is_transport_event_of

            class has_for_transport_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Transporter]
                # inverse_property = is_tranpsort_event_of_logger_of

            class has_for_product_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Product]
                inverse_property = is_product_event_of

            class has_for_product_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Product]
                # inverse_property = is_product_event_of_logger_of

            class has_for_process_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [ProdProcess]

            class has_for_process_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [ProdProcess]

            class is_process_event_of(owlready2.ObjectProperty):
                domain = [ProdProcess]
                range = [Event]
                inverse_property = has_for_process_event

            class is_prodprocess_of(owlready2.ObjectProperty):
                domain = [ProdProcess]
                range = [Machine]

            class has_for_prodprocess(owlready2.ObjectProperty):
                domain = [Machine]
                range = [ProdProcess]
                inverse_property = is_prodprocess_of

            class has_for_transport_location(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [Location]

            class has_for_queue_location(owlready2.ObjectProperty):
                domain = [Queue]
                range = [Location]

            class has_for_machine_location(owlready2.ObjectProperty):
                domain = [Machine]
                range = [Location]

            class has_for_event_list(owlready2.ObjectProperty):
                domain = [Sim]
                range = [EventList]

            class has_for_logger(owlready2.ObjectProperty):
                domain = [Sim]
                range = [ShortTermLogger]

            class has_for_transporter(owlready2.ObjectProperty):
                domain = [Sim]
                range = [Transporter]

            class has_for_product_sim(owlready2.ObjectProperty):
                domain = [Sim]
                range = [Product]

            class has_for_machine(owlready2.ObjectProperty):
                domain = [Sim]
                range = [Machine]

            class Service(owlready2.Thing):
                pass

            class number_service_operator(Service >> float, owlready2.FunctionalProperty): pass

            class free_service_operator(Service >> float, owlready2.FunctionalProperty): pass

            class Machine_Service(Service):
                pass

            class has_for_wait_machine_service(owlready2.ObjectProperty):
                domain = [Machine_Service]
                range = [Machine]

            class Machine_Service_Operator(owlready2.Thing):
                pass

            class has_for_machine_service_operator_machine(owlready2.ObjectProperty):
                domain = [Machine_Service_Operator]
                range = [Machine]

            class is_machine_service_operator_machine_of(owlready2.ObjectProperty):
                domain = [Machine]
                range = [Machine_Service_Operator]
                inverse_property = has_for_machine_service_operator_machine

            class has_for_machine_service_operator(owlready2.ObjectProperty):
                domain = [Machine_Service]
                range = [Machine_Service_Operator]

            class Transporter_Service(Service):
                pass

            class has_for_wait_transporter_service(owlready2.ObjectProperty):
                domain = [Transporter_Service]
                range = [Transporter]

            class Transporter_Service_Operator(Thing):
                pass

            class has_for_transporter_service_operator_transporter(owlready2.ObjectProperty):
                domain = [Transporter_Service_Operator]
                range = [Transporter]

            class is_transporter_service_operator_transporter_of(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [Transporter_Service_Operator]
                inverse_property = has_for_transporter_service_operator_transporter

            class has_for_transporter_service_operator(owlready2.ObjectProperty):
                domain = [Transporter_Service]
                range = [Transporter_Service_Operator]

            class Defect(owlready2.Thing):
                pass

            class has_for_defect_type_distribution(owlready2.ObjectProperty):
                domain = [Defect]
                range = [Distribution]

            class SubDefect(owlready2.Thing):
                pass

            class defect_type(SubDefect >> str, owlready2.FunctionalProperty): pass

            class has_for_sub_defect_distribution(owlready2.ObjectProperty):
                domain = [SubDefect]
                range = [Distribution]

            class has_for_repair_distribution(owlready2.ObjectProperty):
                domain = [SubDefect]
                range = [Distribution]

            class has_for_defect_machine(owlready2.ObjectProperty):
                domain = [Machine]
                range = [Defect]

            class is_defect_of_machine(owlready2.ObjectProperty):
                domain = [Defect]
                range = [Machine]
                inverse_property = has_for_defect_machine

            class has_for_defect_transporter(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [Defect]

            class is_defect_of_transporter(owlready2.ObjectProperty):
                domain = [Defect]
                range = [Transporter]
                inverse_property = has_for_defect_transporter

            class has_for_sub_defect(owlready2.ObjectProperty):
                domain = [Defect]
                range = [SubDefect]

            class is_defect_machine(Machine >> int, owlready2.FunctionalProperty): pass

            class is_defect_transporter(Transporter >> int, owlready2.FunctionalProperty): pass

            class defect_type_machine(Machine >> str, owlready2.FunctionalProperty): pass

            class defect_type_transporter(Transporter >> str, owlready2.FunctionalProperty): pass

            class next_defect_machine(Machine >> float, owlready2.FunctionalProperty): pass

            class next_defect_transporter(Transporter >> float, owlready2.FunctionalProperty): pass

            class has_for_service_event(owlready2.ObjectProperty):
                domain = [Event]
                range = [Service]

            class has_for_service_event_of_logger(owlready2.ObjectProperty):
                domain = [EventOfLogger]
                range = [Service]


            class State(owlready2.Thing):
                pass

            #not Prodprocess
            class Process(owlready2.Thing):
                pass

            class MergeProcess(Process):
                pass

            class ProdTypeProcess(owlready2.Thing):
                pass

            class CombineProcessData(owlready2.Thing):
                pass

            class number_state(CombineProcessData >> int, owlready2.FunctionalProperty): pass

            class has_for_prod_type_process(owlready2.ObjectProperty):
                domain = [Process]
                range = [ProdTypeProcess]

            class is_for_prod_type_process_of(owlready2.ObjectProperty):
                domain = [ProdTypeProcess]
                range = [Process]
                inverse_property = has_for_prod_type_process

            class has_for_prodprocess_process(owlready2.ObjectProperty):
                domain = [Process]
                range = [ProdProcess]

            class is_prodprocess_of_process(owlready2.ObjectProperty):
                domain = [ProdProcess]
                range = [Process]
                inverse_property = has_for_prodprocess_process

            class has_for_state_combine_process_data(owlready2.ObjectProperty):
                domain = [CombineProcessData]
                range = [State]

            class is_state_of_combine_process_data(owlready2.ObjectProperty):
                domain = [State]
                range = [CombineProcessData]

            class has_for_input_combine(owlready2.ObjectProperty):
                domain = [MergeProcess]
                range = [CombineProcessData]

            class has_for_output_combine(owlready2.ObjectProperty):
                domain = [MergeProcess]
                range = [CombineProcessData]

            class is_input_combine_of(owlready2.ObjectProperty):
                domain = [CombineProcessData]
                range = [MergeProcess]
                inverse_property = has_for_input_combine

            class is_output_combine_of(owlready2.ObjectProperty):
                domain = [CombineProcessData]
                range = [MergeProcess]
                inverse_property = has_for_output_combine

            class current_number_of_products(State >> int, owlready2.FunctionalProperty): pass

            class goal_number_of_products(State >> int, owlready2.FunctionalProperty): pass

            class str_state_number_of_products(State >> str, owlready2.FunctionalProperty): pass

            class state_name(State >> str, owlready2.FunctionalProperty): pass

            class combine_process(Process >> bool, owlready2.FunctionalProperty): pass

            class process_id(Process >> int, owlready2.FunctionalProperty): pass

            class has_for_prod_type_process_state(owlready2.ObjectProperty):
                domain = [State]
                range = [ProdTypeProcess]

            class is_prod_type_process_of_state(owlready2.ObjectProperty):
                domain = [ProdTypeProcess]
                range = [State]

            class is_reverse_prod_type_process_of_state(owlready2.ObjectProperty):
                domain = [ProdTypeProcess]
                range = [State]
                inverse_property = has_for_prod_type_process_state

            class has_for_reverse_prod_type_process_state(owlready2.ObjectProperty):
                domain = [State]
                range = [ProdTypeProcess]
                inverse_property = is_prod_type_process_of_state

            class has_for_product_state(owlready2.ObjectProperty):
                domain = [Product]
                range = [State]

            class is_product_state_of(owlready2.ObjectProperty):
                domain = [State]
                range = [Product]
                inverse_property=has_for_product_state

            class has_for_product_type_state(owlready2.ObjectProperty):
                domain = [State]
                range = [ProductType]

            class is_product_type_of_state(owlready2.ObjectProperty):
                domain = [ProductType]
                range = [State]
                inverse_property=has_for_product_type_state

            class has_for_product_type_source(owlready2.ObjectProperty):
                domain = [State]
                range = [ProductType]

            class is_product_type_of_source(owlready2.ObjectProperty):
                domain = [ProductType]
                range = [State]
                inverse_property=has_for_product_type_source


    def createWorld(self):
        """
        sync reasoning of owlready2
        """
        owlready2.sync_reasoner(self.onto)

    def createEventList(self):
        """
        creates the event list onto
        """
        event_listInstance = self.central.event_list_class(Label.EventList.value + "0")
        event_listInstance.has_for_event_list = []

    def createLogger(self):
        """
        creates the short term logger onto and the normal logger
        """
        event_listInstance = self.central.short_term_logger_class(Label.ShortTermLogger.value + "0")
        event_listInstance.has_for_event_short_term_logger = []
        event_listInstance = self.central.logger_class(Label.Logger.value + "1")
        event_listInstance.has_for_event_of_logger = []

    def getCurrentTimestep(self):
        """
        get current time step in simulation

        :return: float
        """
        return self.central.simInstance.current_timestep

    def setCurrentTimeStep(self, time):
        """
        set new time step

        :param time: float
        """
        self.onto[Label.SimCore.value + "0"].current_timestep = time
