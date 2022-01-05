
class State:
    """
    handles the petri nets and the production process onto
    """
    def __init__(self,simCore):
        """

        :param simCore: simcore
        """
        self.simCore=simCore

    def createState(self):


        pass

    def transformToDict(self, id ):
        """

        transform to state
        :param id: label or "all
        :return:
        """

        response_dict = {}
        if (id == "all"):
            state_list = [state_onto for state_onto in
                                 self.simCore.onto.search(type=self.simCore.central.state_class)]
        else:
            state_list = [self.simCore.onto[id]]
        if state_list == [None]:
            return {'error': "id_not_found"}
        for state_onto in state_list:
            response_dict[state_onto.name] = {}
            response_dict[state_onto.name]['str_state_number'] = state_onto.str_stat_number
            response_dict[state_onto.name]['str_state_number'] = state_onto.state_name
            response_dict[state_onto.name]['current_number_of_products'] = state_onto.current_number_of_products
            response_dict[state_onto.name]['goal_number_of_products'] = state_onto.goal_number_of_products
            response_dict[state_onto.name]["prod_type_process"] = [prod_type_process_onto.name for prod_type_process_onto in state_onto.has_for_prod_type_process_state]
            response_dict[state_onto.name]["reverse_prod_type_process"] = [prod_type_process_onto.name for prod_type_process_onto in state_onto.has_for_reverse_prod_type_process_state ]
            response_dict[state_onto.name]["combine_processes"] =[combine_process_data_onto.name for combine_process_data_onto in state_onto.is_state_of_combine_process_data]


        return response_dict
