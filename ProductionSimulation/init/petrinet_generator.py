"""depriciated"""
from deprecated.sphinx import deprecated





# every list entry is a product
# every product gets the list of needed processes, the states are automatically added
from ProductionSimulation.utilities.path_utilities import PathTest


@deprecated(version='0.1.0', reason="pm4py excluded")
def create_petrinet(product_type_id: int,product_paths: list, pnml_save_path: str, visualize=False):
    """creates a Petrinet out of a list possible productways through production given with a list of process_IDs
    e.g. products=[['0','1','2'],['0','1']]"""

    from pm4py.objects.petri.petrinet import PetriNet, Marking
    import os
    from pm4py.objects.petri import utils
    if not product_paths:
        raise Exception
    
    # create a copy, because popping would transmute the rootvar
    # cant use .copy() easily, because of nested lists
    product_paths_copy = []
    for product_path in product_paths:
        product_path_copy = []
        for process_id in product_path:
            product_path_copy.append(process_id)
        product_paths_copy.append(product_path_copy)

    # create a stringed petrinet
    product_paths_petri = []

    i = 0
    p = 0
    if visualize:
        print(product_paths_copy)
    for product_path in product_paths_copy:
        product_paths_petri.append(['p_source'])
        while product_path:
            if not len(product_path) == 1:
                product_paths_petri[p].append('t_' + str(product_path[0]))
                product_paths_petri[p].append('p_' + str(i))
                i += 1
                product_path.pop(0)
            else:
                product_paths_petri[p].append('t_' + str(product_path[0]))
                product_path.pop(0)
        product_paths_petri[p].append('p_sink')
        p += 1
    if visualize:
        print(product_paths_petri)

    net = PetriNet("new_petri_net")

    added_transitions = []
    added_places = []

    def check_if_in_set(set, name):
        exists = False
        for object in set:
            if object.name == name:
                exists = True
        return exists

    def find_in_set(set, name, label=None):
        result = None
        for object in set:
            if object.name == name:
                if label:
                    if label == object.label:
                        result = object
                else:
                    result = object
        if not result:
            raise Exception
        return result

    for product_path in product_paths_petri:
        for node in product_path:
            if node[:2] == 't_':
                # node = node[2:]
                # if not check_if_in_set(net.transitions, cutted_str):
                transition = PetriNet.Transition(node,
                                                 str(product_paths_petri.index(
                                                     product_path)))  # add product index as label
                net.transitions.add(transition)
                added_transitions.append(node)
            if node[:2] == 'p_':
                node = node[2:]
                if not check_if_in_set(net.places, node):
                    place = PetriNet.Place(node)
                    net.places.add(place)
                    added_places.append(node)
    if visualize:
        print(net.places)
        print(added_places)
        print(net.transitions)
        print(added_transitions)

    for product_path in product_paths_petri:
        for node in product_path:
            if not node[2:] == 'sink':
                index = product_path.index(node)
                node_1 = product_path[index]
                node_2 = product_path[index + 1]
                n_1 = None
                n_2 = None
                if node_1[:2] == 't_':
                    n_1 = find_in_set(net.transitions, node_1, label=str(
                        product_paths_petri.index(product_path)))  # also read the index to not doubleuse transitions
                    n_2 = find_in_set(net.places, node_2[2:])
                elif node_1[:2] == 'p_':
                    n_1 = find_in_set(net.places, node_1[2:])
                    n_2 = find_in_set(net.transitions, node_2, label=str(
                        product_paths_petri.index(product_path)))  # also read the index to not doubleuse transitions
                utils.add_arc_from_to(n_1, n_2, net)

    for transition in net.transitions:
        transition.label = transition.name[2:]
    if visualize:
        print(net.places)
        print(net.transitions)
        print(net.arcs)

    from pm4py.objects.petri.exporter import exporter as pnml_exporter

    pnml_save_path=PathTest.check_dir_path(pnml_save_path)
    pnml_exporter.apply(net, Marking(), pnml_save_path+"/product_"+str(product_type_id)+".pnml")

    if visualize:
        from pm4py.visualization.petrinet import visualizer as pn_visualizer
        parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
        gviz = pn_visualizer.apply(net, None, Marking(), parameters=parameters)
        pn_visualizer.view(gviz)

