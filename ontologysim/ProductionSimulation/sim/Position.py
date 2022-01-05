from ontologysim.ProductionSimulation.sim.Enum import Label


class Position:
    """
    handles the onto queue
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

    def createPosition(self):
        """
        creat position
        :return: onto
        """

        positionInstance = self.simCore.central.position_class(Label.Position.value + str(self.simCore.position_id),
                                                               namespace=self.simCore.onto)
        positionInstance.blockedSpace = 0
        self.simCore.position_id += 1

        return positionInstance

    # TODO transform to dict add kpis
    def transformToDict(self, id):
        """
        transform the onto and the kpis into dict

        :param id: str, label
        :return: {}
        """

        response_dict = {}
        if (id == "all"):
            id_list = [queue_onto.name for queue_onto in
                       self.simCore.onto.search(type=self.simCore.central.position_class)]
        else:
            id_list = [id]

        for id in id_list:
            position_onto = self.simCore.onto[id]

            response_dict[position_onto.name] = {}
            response_dict[position_onto.name]['blockedSpace'] = position_onto.blockedSpace

            response_dict[position_onto.name]['product_name'] = ""

            if(len(position_onto.has_for_product)!=0):
                response_dict[position_onto.name]['product_name'] = position_onto.has_for_product[0].name

        return response_dict