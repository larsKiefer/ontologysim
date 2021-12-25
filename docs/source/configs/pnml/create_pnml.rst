PNML
==============
.. note:: Depreciated

the library `Pm4Py <https://pm4py.fit.fraunhofer.de/>`__ is used to create pnml-files more easily. So you can create pnml files with python. In the example-folder under ``example/create_pnml`` examples

1. initialize a net

.. code-block:: python

    net = PetriNet("new_petri_net")

2. create places

.. code-block:: python

    source = PetriNet.Place("source")
    sink = PetriNet.Place("sink")
    p_1 = PetriNet.Place("p_1")


3. add place to net

.. code-block:: python

    net.places.add(source)
    net.places.add(sink)
    net.places.add(p_1)


4. create transitions


.. code-block:: python

    t_1 = PetriNet.Transition("name_1", "1")
    t_2 = PetriNet.Transition("name_2", "2")

.. note: the second parameter must be equal to a process id

5. add transitions to net

.. code-block:: python

    net.transitions.add(t_1)
    net.transitions.add(t_2)

6. combine place with transistion

.. code-block:: python

    utils.add_arc_from_to(source, t_1, net)
    utils.add_arc_from_to(t_1, p_1, net)

* now the source is connected with place p_1 over the transistion t_1

7. initialize markings

.. code-block:: python

    initial_marking = Marking()
    final_marking = Marking()

* a selction of a place is not neccessary, but can be done as followed: initial_marking[source] = 1

8. export net

.. code-block:: python

    pnml_exporter.apply(net, initial_marking, "ontologysim/example/config/createdPetriNet.pnml", final_marking=final_marking)

9. (optional) plot pnml

.. code-block:: python

    from pm4py.visualization.petrinet import visualizer as pn_visualizer
    parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT:"svg"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
    pn_visualizer.view(gviz)
