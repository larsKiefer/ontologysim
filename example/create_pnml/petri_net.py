
"""depreciated"""

"""
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri import semantics

#Not needed



net = PetriNet("new_petri_net")
# creating source, p_1 and sink place
source = PetriNet.Place("source")
sink = PetriNet.Place("sink")
p_1 = PetriNet.Place("p_1")
p_2 = PetriNet.Place("p_2")
p_3 = PetriNet.Place("p_3")
p_4 = PetriNet.Place("p_4")
# add the places to the Petri Net
net.places.add(source)
net.places.add(sink)
net.places.add(p_1)
net.places.add(p_2)
net.places.add(p_3)
net.places.add(p_4)

# Create transitions
t_1 = PetriNet.Transition("name_1", "1")
t_2 = PetriNet.Transition("name_2", "2")
t_3 = PetriNet.Transition("name_3", "2")
t_4 = PetriNet.Transition("name_4", "4")
t_5 = PetriNet.Transition("name_5", "5")
t_6 = PetriNet.Transition("name_6", "6")
# Add the transitions to the Petri Net
net.transitions.add(t_1)
net.transitions.add(t_2)
net.transitions.add(t_3)
net.transitions.add(t_4)
net.transitions.add(t_5)
net.transitions.add(t_6)

# Add arcs
from pm4py.objects.petri import utils
utils.add_arc_from_to(source, t_1, net)
utils.add_arc_from_to(t_1, p_1, net)
utils.add_arc_from_to(p_1, t_2, net)
utils.add_arc_from_to(p_1, t_3, net)
utils.add_arc_from_to(t_2, p_2, net)
utils.add_arc_from_to(t_3, p_3, net)
utils.add_arc_from_to(p_2, t_4, net)
utils.add_arc_from_to(p_3, t_5, net)
utils.add_arc_from_to(t_4, p_4, net)
utils.add_arc_from_to(t_5, p_4, net)
utils.add_arc_from_to(p_4, t_6, net)
utils.add_arc_from_to(t_6, sink, net)

# Adding tokens
initial_marking = Marking()

print(initial_marking.elements())
initial_marking[source] = 1
final_marking = Marking()
final_marking[sink] = 1

transitions = semantics.enabled_transitions(net, initial_marking)
print(transitions)
new_marking=semantics.execute(t_1,net,initial_marking)

print(semantics.is_enabled(t_1,net,initial_marking))
print(semantics.is_enabled(p_1,net,initial_marking))
print(semantics.is_enabled(source,net,initial_marking))
transitions = semantics.enabled_transitions(net, initial_marking)
print(transitions)



from pm4py.objects.petri.exporter import exporter as pnml_exporter

print(net)
pnml_exporter.apply(net, initial_marking, "ontologysim/example/config/createdPetriNet.pnml", final_marking=final_marking)
data=""
"""

"""
#with open('ontologysim/example/config/createdPetriNet1.create_pnml', 'r') as file:
    data = file.read()
    print(data)

#with open("ontologysim/example/config/createdPetriNet11.create_pnml", "w") as file:
    file.write(data)
    file.close()

from pm4py.visualization.petrinet import visualizer as pn_visualizer
parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT:"svg"}
gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
pn_visualizer.view(gviz)
"""