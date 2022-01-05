from ontologysim.ProductionSimulation.controller.transporter_controller import TransporterController


class TransporterController_EDD(TransporterController.TransporterController):
    """
    sort products on transporter based on Earlist Deadline first, currently there is no due time elemented. Therefore the start of production is set as reference.
    SQF used
    """

    def sort_products_on_transporter(self, transport_onto):
        """
        sort products on transporter after EDD

        :param transport_onto:
        :return: [product name,int]
        """
        products_on_transporter = []

        queue_list = transport_onto.has_for_transp_queue

        for queue in queue_list:
            for position in queue.has_for_position:
                for product in position.has_for_product:
                    if product.blocked_for_transporter == 0 and self.transport.end_queue_allowed(transport_onto,product):
                        products_on_transporter.append([product.name, product.start_of_production_time])

        products_on_transporter.sort(key=lambda x: x[1])

        return products_on_transporter

    def sort_products_not_on_transporter(self,transport_onto=None):
        """
        sort products not on transporter after EDD

        :param transport_onto:
        :return:
        """
        event_list = []
        products_not_on_transporter = []

        for queue in self.transport.get_queue_transportation_allowed(transport_onto):
            for position in queue.has_for_position:
                for product in position.has_for_product:
                    if product.blocked_for_transporter == 0:
                        if product.blocked_for_transporter == 0 and  self.transport.end_queue_allowed(transport_onto,product):
                            products_not_on_transporter.append([product.name, product.start_of_production_time])

        products_not_on_transporter.sort(key=lambda x: x[1])
        #print("EDD",products_not_on_transporter)
        return products_not_on_transporter

    def sort_products(self, products_on_transporter, products_not_on_transporter):
        """
        combines products not on transporter with on transporter and sort after EDD

        :param products_on_transporter:
        :param products_not_on_transporter:
        :return:
        """
        type_on = "on"
        type_not_on = "not_on"
        elements = products_on_transporter + products_not_on_transporter
        type_list = [type_on] * len(products_on_transporter) + [type_not_on] * len(products_not_on_transporter)

        for x, y in zip(elements, type_list):
            x.append(y)

        elements.sort(key=lambda x: x[1])
        return elements