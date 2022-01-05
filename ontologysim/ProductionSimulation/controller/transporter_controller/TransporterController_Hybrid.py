import operator

from ontologysim.ProductionSimulation.controller.transporter_controller import TransporterController
from ontologysim.ProductionSimulation.sim.Enum import Queue_Enum, Label, Evaluate_Enum
from ontologysim.ProductionSimulation.utilities.sub_class_utilities import SubClassUtility
from ontologysim.ProductionSimulation.controller.transporter_controller.TransporterController_Enum import Queue_Selection

class TransporterController_Hybrid(TransporterController.TransporterController):
    """
    Combines multiple transporter controller strategies
    """
    def __init__(self):
        self.transport=None #add it over machine.addMachineController
        self.counter=0
        self.controller_parameter_dict={}
        self.controller_instance_dict={}


    def addControllerDict(self ,controller_dict):
        """
        adding all controller in a dict, value must be between 0 and 1


        :param controller_dict: {Klass:int [0:1]}
        """
        for python_class ,v in controller_dict.items():

            if python_class in SubClassUtility.get_all_subclasses(TransporterController.TransporterController) or python_class == TransporterController:
                if v> 1 or v < 0:
                    raise Exception(str(v) + " out of range")
                self.controller_parameter_dict[python_class.__name__] = v
                python_instance = python_class()
                python_instance.transport = self.transport
                self.controller_instance_dict[python_class.__name__] = python_instance
            else:
                raise Exception(str(python_class) + " not subclass of MachineController")



    def combine_products(self, transport_onto):
        """
        calculates for all controller strategies the ordered product hirachy

        :param transport_onto:
        :return: [product_name, time, when NFJ then queue_name ]
        """
        erg_dict = {}
        product_dict = {}
        product_dict_value = {}
        queue_dict_value={}
        for queue_selection in Queue_Selection:
            queue_dict_value[queue_selection.value]={}
            product_dict_value[queue_selection.value]={}
        erg_list = []
        for k, v in self.controller_instance_dict.items():
            if self.controller_parameter_dict[k] != 0:

                erg_dict[k] = v.combine_products(transport_onto)

                len_erg = len(erg_dict[k])
                if len_erg > 0:
                    value=100/len_erg
                    increment=value/len_erg
                    for erg in erg_dict[k]:
                        product_onto_name = erg[0]

                        if product_onto_name in product_dict.keys():
                            product_dict[product_onto_name] += value * self.controller_parameter_dict[k]
                        else:
                            product_dict[product_onto_name] = value * self.controller_parameter_dict[k]


                        if product_onto_name in queue_dict_value[v.queue_selection].keys():
                            queue_dict_value[v.queue_selection][product_onto_name] += value * self.controller_parameter_dict[k]
                        else:
                            queue_dict_value[v.queue_selection][product_onto_name] = value * \
                                                                                      self.controller_parameter_dict[k]
                            product_dict_value[v.queue_selection][product_onto_name] = erg

                        value -= increment

        if len(product_dict) > 0:

            sorted_products = sorted(product_dict.items(), key=operator.itemgetter(1), reverse=True)

            for k, v in sorted_products:
                max_value = 0
                erg = []
                for queue_selection in Queue_Selection:
                    if k in queue_dict_value[queue_selection.value].keys():
                        if queue_dict_value[queue_selection.value][k] > max_value:
                            max_value = queue_dict_value[queue_selection.value][k]
                            erg = product_dict_value[queue_selection.value][k]
                    else:
                        #print("product no in dict" , queue_selection.value,k)
                        pass

                erg_list.append(erg)

        return erg_list

