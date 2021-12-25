
import os
import inspect

import sys
from functools import reduce

from deprecated.sphinx import deprecated



class PnmlTest:
    """
    Tests a given Pnml file
    """

    @classmethod
    @deprecated(version='0.1.0', reason="pm4py excluded")
    def check_pnml(cls, net):
        """
        deprecated
        checks if the structure of the pnml is correct
        checked:
        - sink, source available?
        - check in and out arc
        - check if every place is connected

        :param net: pnml-net
        :return: bool

        # place.name==id
        # transistion.name == id
        # transistion.label == text

        # transistion.label != place
        """

        import pm4py
        from pm4py.objects.petri import utils
        from pm4py.objects.petri import semantics

        cycles = utils.get_cycles_petri_net_places(net)
        if len(cycles) != 0:
            raise Exception("cycle found")

        places = net.places
        transitions = net.transitions
        arcs = net.arcs

        if len([place.name for place in places if place.name == "source"]) != 1:
            raise Exception("number of sources is incorrect")
        if len([place.name for place in places if place.name == "sink"]) != 1:
            raise Exception("number of sinks is incorrect")

        for place in places:
            if place.name == "source":
                if len(place.in_arcs) != 0:
                    raise Exception("source not correct initialised, in arc")
            elif place.name == "sink":
                if len(place.out_arcs) != 0:
                    raise Exception("sink not correct initialised, out arc")
            else:
                if len(place.out_arcs) == 0 or len(place.in_arcs) == 0:
                    raise Exception("place connection is wrong")

            for arc in place.in_arcs:
                if not isinstance(arc.source, pm4py.objects.petri.petrinet.PetriNet.Transition):
                    raise Exception(str(place) + " in arc is incorrect")

            for arc in place.out_arcs:
                if not isinstance(arc.target, pm4py.objects.petri.petrinet.PetriNet.Transition):
                    raise Exception(str(place) + " out arc is incorrect")

        for trans in transitions:

            if len(trans.in_arcs) == 0:
                raise Exception(str(trans), " connection is wrong")

            if len(trans.out_arcs) == 0:
                raise Exception(str(trans), " connection is wrong")

            for arc in trans.in_arcs:
                if not isinstance(arc.source, pm4py.objects.petri.petrinet.PetriNet.Place):
                    raise Exception(str(trans) + " arc source is incorrect")

            for arc in trans.out_arcs:
                if not isinstance(arc.target, pm4py.objects.petri.petrinet.PetriNet.Place):
                    raise Exception(str(trans) + " arc target is incorrect")

        place_id_list = [place.name for place in places]
        trasistion_id_list = [trans.name for trans in transitions]

        if len(place_id_list) != len(set(place_id_list)):
            raise Exception("place id not unique")

        if len(trasistion_id_list) != len(set(trasistion_id_list)):
            raise Exception("place id not unique")

        if len(reduce(set.intersection, [set(trasistion_id_list), set(place_id_list)])) > 0:
            raise Exception("place and transistion id not unique")

        return True
