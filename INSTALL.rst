Blocksmurfer Installation
=========================

Install packages needed for Bitcoinlib:

.. code-block:: bash

    $ sudo apt install build-essential python-dev python3-dev libgmp3-dev libssl-dev


Create a virtual environment

.. code-block:: bash

    $ virtualenv -p python3 venv/blocksmurfer
    $ source venv/blocksmurfer/bin/activate


Download Blocksmurfer and install requirements.

.. code-block:: bash

    $ git clone https://github.com/1200wd/blocksmurfer.git
    $ cd blocksmurfer
    $ pip install -r requirements.txt

Now you can test your install and run flask directly

.. code-block:: bash

    $ flask run

or with gunicorn

.. code-block:: bash

    $ ./boot.sh

Blocksmurfer should run now on http://localhost:5000

Please note:
* Remove Blocksmurfer from Bitcoinlib's provider definitions in providers.json to avoid recursive loops.


Apache
------

Check the Apache config file example in blocksmurfer/examples/apache-example.conf
to see how to configure Blocksmurfer with Apache.