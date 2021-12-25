Ontology classes
===================

Schema
---------

A simplified not complete schema. For a complete overview please use a graph tool.

![Graph](OntologysimGraph.png "Graph")

Online view
-------------
For better overview of the production simulation, you can use a dynamic graph view tool

1. open Link: [WebVOWL](http://www.visualdataweb.de/webvowl)
2. under Ontology: upload file
    * example owl files a provided under `/example/owl/`



Complete list
---------------



```python

            class Sim(owlready2.Thing): pass

            class current_timestep(Sim >> float, owlready2.FunctionalProperty): pass

            class Transporter(owlready2.Thing): pass

            class speed(Transporter >> float, owlready2.FunctionalProperty): pass

            class route_type(Transporter >> str, owlready2.FunctionalProperty): pass

            class Queue(owlready2.Thing): pass

            class has_for_drive_queue(owlready2.ObjectProperty):
                domain = [Transporter]
                range = [Queue]

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

            class task_type(Task >> str, owlready2.FunctionalProperty): pass

            # python_name = "cost"
            class blocked_for_transporter(Product >> float, owlready2.FunctionalProperty): pass

            class blocked_for_machine(Product >> float, owlready2.FunctionalProperty): pass

            class marking(Product >> str, owlready2.FunctionalProperty): pass

            class start_of_production_time(Product >> float, owlready2.FunctionalProperty): pass

            class end_of_production_time(Product >> float, owlready2.FunctionalProperty): pass

            class queue_input_time(Product >> float, owlready2.FunctionalProperty): pass

            class ProductType(owlready2.Thing): pass

            class has_for_product_type(owlready2.ObjectProperty):
                domain = [Product]
                range = [ProductType]

            class is_product_of(owlready2.ObjectProperty):
                domain = [ProductType]
                range = [Product]
                inverse_property = has_for_product_type

            class pnml(ProductType >> str, owlready2.FunctionalProperty): pass

            class has_for_product_type_task(owlready2.ObjectProperty):
                domain = [Task]
                range = [ProductType]

            class ProdProcess(owlready2.Thing): pass

            class combine(ProdProcess >> bool, owlready2.FunctionalProperty): pass

            class id(ProdProcess >> int, owlready2.FunctionalProperty): pass

            class Machine(owlready2.Thing): pass

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


```