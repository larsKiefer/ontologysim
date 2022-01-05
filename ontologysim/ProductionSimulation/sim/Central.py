from owlready2 import *

from ontologysim.ProductionSimulation.sim.Enum import Label


class Central:
    """
    storage location for classes and important instances from ontology,
    excluded from the simCore to make the simCore class smaller
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore
        self.task_class = None
        self.queue_class = None
        self.event_class = None
        self.event_of_logger_class = None
        self.normal_distribution_class = None
        self.short_term_logger_class = None
        self.distribution_class = None
        self.sim_class = None
        self.transporter_class = None
        self.location_class = None
        self.product_type_class = None
        self.process_class = None
        self.state_class = None
        self.prod_process_class = None
        self.merge_process_class=None
        self.combine_process_data = None
        self.product_class = None
        self.end_queue_class = None
        self.transport_queue_class = None
        self.event_list_class = None
        self.logger_class = None
        self.position_class = None
        self.setup_class = None
        self.machine_class = None
        self.inputqueue_class = None
        self.outputqueue_class = None
        self.random_distribution_class = None
        self.defect_class = None
        self.sub_defect_class = None
        self.service_class = None
        self.machine_service_class = None
        self.machine_service_operator_class = None
        self.transporter_service_class = None
        self.transporter_service_operator_class = None

        self.simInstance = None
        self.machine_list = None
        self.transporter_list = None
        self.task_list = None
        self.all_prod_processes = None
        self.queue_list = None
        self.queue_list_not_transport_and_end = None
        self.start_queue_list = None
        self.end_queue_list = None
        self.dead_lock_list = None
        self.machine_queue_list = None
        self.queue_list_not_transport_end_process=None
        self.number_of_start_positions = 0

        self.queue_to_machine = {}
        self.queue_to_transporter = {}



    def init_class(self):
        """
        initialization of all ontology classes
        """
        self.task_class = self.simCore.onto.search(iri="*#Task").__getitem__(0)
        self.queue_class = self.simCore.onto.search(iri="*#Queue").__getitem__(0)
        self.transporter_class = self.simCore.onto.search(iri="*#Transporter").__getitem__(0)
        self.event_class = self.simCore.onto.search(iri="*#Event").__getitem__(0)
        self.event_list_class = self.simCore.onto.search(iri="*#EventList").__getitem__(0)
        self.short_term_logger_class = self.simCore.onto.search(iri="*#ShortTermLogger").__getitem__(0)
        self.logger_class = self.simCore.onto.search(iri="*#Logger").__getitem__(0)
        self.event_of_logger_class = self.simCore.onto.search(iri="*#EventOfLogger").__getitem__(0)
        self.normal_distribution_class = self.simCore.onto.search(iri="*#NormalDistribution").__getitem__(0)
        self.sim_class = self.simCore.onto.search(iri="*#Sim").__getitem__(0)
        self.position_class = self.simCore.onto.search(iri="*#Position").__getitem__(0)
        self.location_class = self.simCore.onto.search(iri="*#Location").__getitem__(0)
        self.product_type_class = self.simCore.onto.search(iri="*#ProductType").__getitem__(0)
        self.prod_process_class = self.simCore.onto.search(iri="*#ProdProcess").__getitem__(0)
        self.prod_type_process_class = self.simCore.onto.search(iri="*#ProdTypeProcess").__getitem__(0)
        self.process_class = self.simCore.onto.search(iri="*#Process").__getitem__(0)
        self.combine_process_data_class = self.simCore.onto.search(iri="*#CombineProcessData").__getitem__(0)
        self.state_class = self.simCore.onto.search(iri="*#State").__getitem__(0)
        self.merge_process_class = self.simCore.onto.search(iri="*#MergeProcess").__getitem__(0)
        self.setup_class = self.simCore.onto.search(iri="*#SetUp").__getitem__(0)
        self.machine_class = self.simCore.onto.search(iri="*#Machine").__getitem__(0)
        self.inputqueue_class = self.simCore.onto.search(iri="*#InputQueue").__getitem__(0)
        self.outputqueue_class = self.simCore.onto.search(iri="*#OutputQueue").__getitem__(0)
        self.product_class = self.simCore.onto.search(iri="*#Product").__getitem__(0)
        self.end_queue_class = self.simCore.onto.search(iri="*#EndQueue").__getitem__(0)
        self.transport_queue_class = self.simCore.onto.search(iri="*#TranspQueue").__getitem__(0)
        self.random_distribution_class = self.simCore.onto.search(iri="*#RandomDistribution").__getitem__(0)
        self.distribution_class = self.simCore.onto.search(iri="*#Distribution").__getitem__(0)

        self.defect_class = self.simCore.onto.search(iri="*#Defect").__getitem__(0)
        self.sub_defect_class = self.simCore.onto.search(iri="*#SubDefect").__getitem__(0)

        self.service_class = self.simCore.onto.search(iri="*#Service").__getitem__(0)
        self.machine_service_class = self.simCore.onto.search(iri="*#Machine_Service").__getitem__(0)
        self.machine_service_operator_class = self.simCore.onto.search(iri="*#Machine_Service_Operator").__getitem__(0)
        self.transporter_service_class = self.simCore.onto.search(iri="*#Transporter_Service").__getitem__(0)
        self.transporter_service_operator_class = self.simCore.onto.search(
            iri="*#Transporter_Service_Operator").__getitem__(0)

    def init_instance(self):
        """
        initialization of important ontology instances to reduce the computing time:
        queue_list, queue_list_not_transport_and_end, task_list, all_prod_processes
        """
        self.queue_list = self.simCore.onto.search(type=self.queue_class)
        self.queue_list_not_transport_and_end = [queue for queue in self.queue_list if
                                                 len(queue.is_transp_queue_of) == 0 and not (
                                                         Label.EndQueue.value in queue.name)]

        self.queue_list_not_transport_end_process = [queue for queue in self.queue_list if
                                                 len(queue.is_transp_queue_of) == 0 and not (
                                                         Label.EndQueue.value in queue.name) and len(queue.is_for_queue_process_of) == 0]
        self.machine_list = [machine for machine in  self.simCore.onto.search(type=self.machine_class)]
        self.transporter_list = [transporter for transporter in self.simCore.onto.search(type=self.transporter_class)]

        self.start_queue_list = [queue for queue in self.queue_list if
                                 Label.StartQueue.value in queue.name]
        self.end_queue_list = [queue for queue in self.queue_list if
                               Label.EndQueue.value in queue.name]
        self.dead_lock_list = [queue for queue in self.queue_list if
                               Label.DeadlockQueue.value in queue.name]

        self.task_list = self.simCore.onto.search(type=self.task_class)
        self.all_prod_processes = self.simCore.onto.search(type=self.prod_process_class)
        self.machine_queue_list=[]
        for machine_onto in self.simCore.onto.search(type=self.machine_class):
            prod_queue_list = machine_onto.has_for_queue_process
            for prod_queue in prod_queue_list:
                self.queue_to_machine[prod_queue.name] = machine_onto.name

            for queue_onto in machine_onto.has_for_input_queue:
                if queue_onto not in self.machine_queue_list:
                    self.machine_queue_list.append(queue_onto)

            for queue_onto in machine_onto.has_for_output_queue:
                if queue_onto not in self.machine_queue_list:
                    self.machine_queue_list.append(queue_onto)



        for transport_onto in self.simCore.onto.search(type=self.transporter_class):
            queue_list = transport_onto.has_for_transp_queue
            for queue in queue_list:
                self.queue_to_transporter[queue.name] = transport_onto.name

        self.number_of_start_positions = sum([self.simCore.queue.get_number_of_free_positions(queue_onto) for queue_onto in self.start_queue_list])

    def init_all_ids(self):
        """
        sets all ids from the different types, important when an owl-file is imported
        """
        self.simCore.machine_id = len(self.simCore.onto.search(type=self.simCore.central.machine_class))
        self.simCore.queue_id = len(self.simCore.onto.search(type=self.simCore.central.queue_class))
        self.simCore.position_id = len(self.simCore.onto.search(type=self.simCore.central.position_class))
        self.simCore.prod_process_id = len(self.simCore.onto.search(type=self.simCore.central.prodProcess_class))
        self.simCore.prod_type_process_id = len(self.simCore.onto.search(type=self.simCore.central.prod_type_process_class))
        self.simCore.combine_process_data = len(self.simCore.onto.search(type=self.simCore.central.combine_process_data_class))

        self.simCore.product_id = len(self.simCore.onto.search(type=self.simCore.central.product_class))
        self.simCore.event_id = max([self.extract_id_from_name(event.name) for event in
                                     self.simCore.onto[Label.EventList.value + "0"].has_for_event]) + 1
        self.simCore.product_type_id = len(self.simCore.onto.search(type=self.simCore.central.product_type_class))
        self.simCore.distribution_id = len(self.simCore.onto.search(type=self.simCore.central.distribution_class))
        self.simCore.location_id = len(self.simCore.onto.search(type=self.simCore.central.location_class))
        self.simCore.transport_id = len(self.simCore.onto.search(type=self.simCore.central.transporter_class))
        self.simCore.set_up_id = len(self.simCore.onto.search(type=self.simCore.central.setup_class))
        self.simCore.task_id = len(self.simCore.onto.search(type=self.simCore.central.task_class))
        self.simCore.sub_defect_id = len(self.simCore.onto.search(type=self.simCore.central.sub_defect_class))
        self.simCore.defect_id = len(self.simCore.onto.search(type=self.simCore.central.defect_class))
        self.simCore.machine_service_id = len(self.simCore.onto.search(type=self.simCore.central.machine_service_class))
        
        self.simCore.state_id = len(self.simCore.onto.search(type=self.simCore.central.state_class))
        self.simCore.process_id = len(self.simCore.onto.search(type=self.simCore.central.process_class))
        
        self.simCore.machine_service_operator_id = len(
            self.simCore.onto.search(type=self.simCore.central.machine_service_operator_class))
        self.simCore.transporter_service_id = len(
            self.simCore.onto.search(type=self.simCore.central.transporter_service_class))
        self.simCore.transporter_service_operator_id = len(
            self.simCore.onto.search(type=self.simCore.central.transporter_service_operator_class))

    def extract_id_from_name(self, name):
        """
        every id starts with a string and ends with a number

        :param name: name of onto
        :return: id
        """
        return int(re.search(r'\d+', name).group())


    def getIds(self,type):
        """
        get all ids from type e.g. machine
        for accessing all Ids type==all

        :param type: str
        :return: dict{}
        """
        dictIDs={}

        if(type=="transporter" or type=="all"):
            transporter_onto_list=self.simCore.onto.search(type=self.simCore.central.transporter_class)
            dictIDs['transporter']=[transport_onto.name for transport_onto in transporter_onto_list]

        if (type == "machine" or type == "all"):
            machine_onto_list = self.simCore.onto.search(type=self.simCore.central.machine_class)
            dictIDs['machine'] = [machine_onto.name for machine_onto in machine_onto_list]

        if (type == "start_queue" or type == "all"):
            dictIDs['start_queue'] = [queue_onto.name for queue_onto in self.start_queue_list]

        if (type == "deadlock_queue" or type == "all"):
            dictIDs['deadlock_queue'] = [queue_onto.name for queue_onto in self.dead_lock_list]

        if (type == "end_queue" or type == "all"):
            dictIDs['end_queue'] = [queue_onto.name for queue_onto in self.end_queue_list]

        if (type == "machine_queue" or type == "all"):
            dictIDs['machine_queue'] = [queue_onto.name for queue_onto in self.machine_queue_list]

        if (type == "transporter_queue" or type == "all"):
            dictIDs['transporter_queue'] = [queue_name for queue_name in self.queue_to_transporter.keys()]



        return dictIDs

    def fromIdGetType(self,id):
        """
        given a onto name, the type is extracted

        :param id: str
        :return: enum.name
        """

        for enum in Label:
            label_suitable=False
            for i in range(len(enum.value)):
                if enum.value[i]!=id[i]:
                    label_suitable=False
                    break;
                else:
                    label_suitable = True
            if label_suitable:
                return enum.name

        return "id not found"


