Documentation
========================

Sphinx
-----------

The main python documentation is created by Sphinx. In the directory ``/docs/source`` are all files regarding Sphinx saved.
To build the documentation in the folder ``/docs/build`` run.

.. code-block:: python

    cd docs
    sphinx-build -b html ./source ./build

To create .rst files faster, it helps to use Sphinx auto-module

.. code-block:: python

    cd doc
    sphinx-apidoc -o ./source ../
    sphinx-build -b html ./source ./build


SwaggerUI
-----------

For Flask, swaggerUI was also set up. All swaggerUI json files are saved in ```/Flask/static``

Pypi
-----

.. code-block:: bash

    python setup.py sdist
    twine upload dist/*
