############
Demo project
############

The :file:`demo/` folder holds a demo project to illustrate django-chartjs
usage.


***********************
Browse demo code online
***********************

See `demo folder in project's repository`_.


***************
Deploy the demo
***************

System requirements:

* `Python`_ version 2.7 or 3.3, available as ``python`` command.
  
  .. note::

     You may use `virtualenv`_ to make sure the active ``python`` is the right
     one.

* ``make`` and ``wget`` to use the provided :file:`Makefile`.

Execute:

.. code-block:: sh

   git clone git@github.com:peopledoc/django-chartjs.git
   cd django-chartjs/
   make demo

It installs and runs the demo server on localhost, port 8000. So have a look
at http://localhost:8000/

.. note::

   If you cannot execute the Makefile, read it and adapt the few commands it
   contains to your needs.

Browse and use :file:`demo/demoproject/` as a sandbox.


**********
References
**********

.. target-notes::

.. _`demo folder in project's repository`:
   https://github.com/peopledoc/django-chartjs/tree/master/demo/demoproject/

.. _`Python`: http://python.org
.. _`virtualenv`: http://virtualenv.org
