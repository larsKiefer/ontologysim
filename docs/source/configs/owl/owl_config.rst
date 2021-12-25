OWL ini
==============

in this ini the owl-path and save options are defined.

Main structure
----------------

after each controller type e.g. machine, there needs to be a dict with the following keys:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - java_path
     - defines the java path to your jre or jdk java version
   * - owl_save_path
     - default list of save options [{'type','save':bool (True or False),'path':relative_path}]

the following types are defined:

* production_without_task_defect: saves the plain production without task and defect in an owl-file
* production: saves the complete production in an owl-file

Example
---------

this file is available in ``example/config/owl_config.ini``

.. code-block:: JSON

    [OWL]
    java_path="C:/Program Files (x86)/Java/jre1.8.0_261/bin/java.exe"
    owl_save_path=[{'type':"production_without_task_defect",'save':True,'path':"/example/owl/production_without_task_defect.owl"},
                {'type':"production",'save':True,'path':"/example/owl/production.owl"}
                ]

