Foobar CLI Reference
====================

The ``foobar`` package provides a command-line interface:

.. code:: bash

    $ python -m foobar [OPTIONS] [COMMAND] [ARGS]
    ...

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

To see its version, run:

.. code:: bash

    $ python -m foobar --version
    foobar, version 0.1.0

The ``foo`` Command
-------------------

To run the ``foo`` command:

.. code:: bash

    $ python -m foobar foo [SUBCOMMAND] [ARGS]

The ``run`` subcommand
~~~~~~~~~~~~~~~~~~~~~~

The ``run`` subcommand runs the ``foo`` object, and prints ``foo``.

.. code:: bash

    $ python -m foobar foo run
    foo

The ``inc`` subcommand
~~~~~~~~~~~~~~~~~~~~~~

The ``inc`` subcommand receives a single argument, ``x``, increments it by one
and prints the result.

.. code:: bash

    $ python -m foobar foo inc 1
    2

The ``add`` subcommand
~~~~~~~~~~~~~~~~~~~~~~

The ``add`` subcommand receives two arguments, ``x`` and ``y``, sums them and
prints the result.

.. code:: bash

    $ python -m foobar foo add 1 2
    3

The ``bar`` command
-------------------

To run the ``bar`` command:

.. code:: bash

    $ python -m foobar bar [SUBCOMMAND] [ARGS]

The ``run`` subcommand
~~~~~~~~~~~~~~~~~~~~~~

The ``run`` subcommand runs the ``bar`` object, and prints ``bar``.

.. code:: bash

    $ python -m foobar bar run
    bar

It accepts the ``-o``, or ``--output`` option, in which case it prints ``bar``
to the specified path.

.. code:: bash

    $ python -m foobar bar run -o file.txt
    $ cat file.txt
    bar

It accepts the ``-u``, or ``--uppercase`` flag, in which case it prints ``BAR``
in capital letters.

.. code:: bash

    $ python -m foobar bar run -u
    BAR

The ``error`` subcommand
~~~~~~~~~~~~~~~~~~~~~~~~

The ``error`` subcommand raises an exception.

.. code:: bash

    $ python -m foobar bar error
    ERROR: something went terribly wrong :[


This can be used to showcase the ``--quiet`` and ``--traceback`` options of the
``foobar`` command.


.. code:: bash

    $ python -m foobar -q bar error

.. code:: bash

    $ python -m foobar -t bar error
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terribly wrong :[
