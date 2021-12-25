Ontologysim: a Owlready2 library for applied production simulation
=====================================================================

Ontologysim is an open-source deep production simulation framework, with an emphasis on modularized flexible library design and straightforward usability for applications in research and practice. Ontologysim is built on top of Owlready2 framework and requires Python >3.7.

Ontologysim follows a set of high-level design choices which differentiate it from other similar libraries:

* the simulation can be saved at any time and started from a defined point
* high degrees of freedom and possibilities due to the ontology

## Table of Contents
1. [Installation](#installation)
2. [First Start](#first-start)
3. [Flask](#flask)


Installation
==============

git lab
-----------

A stable version of Production simulation is periodically updated on the master and installed as follows:

````bash
git clone https://git.scc.kit.edu/ov0653/ontologysim.git
cd ontologysim
pip3 install -r requirements.txt
````



First Start
===============

Go to the ``/example/Main.py`` and run this python file.

Flask
==============

to start the Flask server run:

````bash
py Flask/FlaskMain.py
````


Problem handling
==================

Owlready2.0
---------------
**Java Path**``

* to use owlready correctly, your java path needs to be set in the ``owl_config.ini`` 
    * [owl introduction](../configs/owl/owl_config)

**Java Memory**

if this error occurs

````bash
owlready2.base.OwlReadyJavaError: Java error message is:
Error occurred during initialization of VM
Could not reserve enough space for 2048000KB object heap
````

then you need to reduce the java memory

1. got to "site-packages\owlready2\reasoning.py"
2. reduce the Java Memory variable to 500


**How to check if everything works**

run in the example folder the `Main.py`