from ontologysim.ProductionSimulation.sim.Enum import Label


class Product:
    """
    handles the product onto
    """
    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

        self.start_number_products=0
        self.logging_number_products=0

    def createProduct(self,product_type_onto):
        """
        creates product in onto

        :param product_type_onto: onto
        :return: product onto
        """

        productInstance = self.simCore.central.product_class(Label.Product.value+ str(self.simCore.product_id))

        self.simCore.product_id += 1

        productInstance.has_for_product_type.append(product_type_onto)
        productInstance.has_for_product_state = product_type_onto.is_product_type_of_source
        #[state for state in product_type_onto.is_product_type_of_state if str(state.state_name) == "source"]
        productInstance.marking = "source"
        productInstance.blocked_for_transporter=0
        productInstance.blocked_for_machine=0
        productInstance.end_of_production_time=0
        return productInstance

    def endBlockForTransporter(self, event_onto):
        """
        when a product is set to a deadlock queue, it gets blocked for transportation. this method removes the transporter blocking.

        :param event_onto:
        """
        self.simCore.event.remove_from_event_list(event_onto)

        time = event_onto.time
        product_onto = event_onto.has_for_product_event.__getitem__(0)
        product_onto.blocked_for_transporter = 0

        self.simCore.event.store_event(event_onto)

    def setStartTime(self,product,time):
        """
        sets start of production

        :param product: onto
        :param time: double
        """
        product.start_of_production_time =time


    def getNextProcess(self,product_onto):
        """
        calculates the next process in the pnml-net

        :param product_onto: onto
        :return: [process id list]
        """
        """
        product_Type = product_onto.has_for_product_type.__getitem__(0)

        net = self.simCore.product_type.dict[product_Type.name]
        initial_marking = Marking()
        current_marking = product_onto.marking

        for p in list(net.places):
            if str(p) == current_marking:
                initial_marking[p] = 1

        transitions = list(semantics.enabled_transitions(net, initial_marking))

        process_id_list=[]
        for t in transitions:

            process_id_list.append(t.label)
        """
        state_onto = product_onto.has_for_product_state.__getitem__(0)
        prod_process_list = state_onto.has_for_prod_type_process_state
        process_id_list = [prod_process.is_for_prod_type_process_of[0].process_id for prod_process in prod_process_list]

        return process_id_list

    def getSuitableAndAvailableMachine(self,process_id):
        """
        calculates all suitabel machines

        :param process_id: id (int) not label
        :return: [[machine onto, free positions,prod process onto]]
        """
        erg=[]
        for prod_porcesses in self.simCore.central.all_prod_processes:

            if int(self.simCore.prod_process.getID(prod_porcesses))==int(process_id):
                machine_onto=prod_porcesses.is_prodprocess_of.__getitem__(0)
                if machine_onto.is_defect_machine==0:
                    input_queue_list=machine_onto.has_for_input_queue
                    free_position=0
                    sum_size=0
                    for input_queue in input_queue_list:
                        for position in input_queue.has_for_position:
                            if position.blockedSpace==0:
                                free_position+=1
                        sum_size+=input_queue.size

                    if free_position>0:
                        erg.append([machine_onto,sum_size-free_position,prod_porcesses])

        return erg

    def init_number_of_products(self):
        """
        calculates the start number of products and the logging number of product
        """

        self.start_number_products = sum([task.number for task in self.simCore.central.task_list if task.task_type=="start"])
        self.logging_number_products = sum([task.number for task in self.simCore.central.task_list if task.task_type=="logging"])

    def evaluateFinishedProduct(self, event_onto):
        """
        handles the finishing of a product, triggers a order release process

        :param event_onto: onto
        """
        product_onto = event_onto.has_for_product_event.__getitem__(0)
        product_onto.end_of_production_time = event_onto.time
        product_type = product_onto.has_for_product_type.__getitem__(0)
        time_diff = product_onto.end_of_production_time - product_onto.start_of_production_time



        self.simCore.logger.evaluatedInformations([{'type':event_onto.type,
                                                    'event_onto_time':event_onto.time,
                                                    'start_time':product_onto.start_of_production_time,
                                                     'end_time':product_onto.end_of_production_time,
                                                    'AOET':product_onto.end_of_production_time-product_onto.start_of_production_time,
                                                    'product_name':product_onto.name}])



        self.simCore.order_release.current_number_of_products -= 1
        self.simCore.number_of_finshed_products+=1

        position_onto=product_onto.is_position_of[0]
        product_onto.is_position_of=[]
        position_onto.blockedSpace=0

        """
        position_list = self.simCore.central.end_queue_list[0].has_for_position
        number_of_finished_products = - self.start_number_products
        for position in position_list:
            if position.blockedSpace == 1 and len(position.has_for_product) == 1:
                number_of_finished_products += 1
        """
        self.simCore.event.remove_from_event_list(event_onto)
        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.store_event(event_onto)

        if self.logging_number_products == self.simCore.number_of_finshed_products- self.start_number_products:
            self.simCore.end = True


        self.simCore.order_release.orderReleaseController.evaluateCreateOrderRelease()

    def transformToDict(self, id):
        """
        transform to dict
        :param id: string, one label or "all"
        :return:
        """

        response_dict = {}
        if (id == "all"):
            product_list = [product_onto for product_onto in
                                 self.simCore.onto.search(type=self.simCore.central.product_class)]
        else:
            product_list = [self.simCore.onto[id]]
        if product_list == [None]:
            return {'error': "id_not_found"}
        for product_onto in product_list:
            response_dict[product_onto.name] = {}
            stateName= product_onto.has_for_product_state[0].state_name
            productTypeName= product_onto.has_for_product_type[0].name
            response_dict[product_onto.name]["percentage"]= self.simCore.product_type.percentageDict[productTypeName][stateName]
            response_dict[product_onto.name]["product_type"]= productTypeName
            response_dict[product_onto.name]["state"]= stateName
            response_dict[product_onto.name]["blocked_for_transporter"] = product_onto.blocked_for_transporter
            response_dict[product_onto.name]["blocked_for_machine"] = product_onto.blocked_for_machine
            response_dict[product_onto.name]["end_of_production_time"] = product_onto.end_of_production_time
            response_dict[product_onto.name]["queue_input_time"] = product_onto.queue_input_time
            response_dict[product_onto.name]["start_of_production_time"] = product_onto.start_of_production_time

        return response_dict