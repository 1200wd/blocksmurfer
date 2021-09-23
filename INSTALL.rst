Blocksmurfer Installation
=========================

Install packages needed for Bitcoinlib:

.. code-block:: bash

    $ sudo apt install build-essential python-dev python3-dev libgmp3-dev libssl-dev python3-virtualenv


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

Configuration
-------------

* Copy config.example.py to config.py 
* Update secret key!
* Select the networks you would like to support and update other settings if you like in the configuration

Please note:
* Remove Blocksmurfer from Bitcoinlib's provider definitions in ./bitcoinlib/providers.json to avoid recursive loops.
* In the Bitcoinlib config file (./bitcoinlib/config.ini) you can change the loglevel, log location, timeout for requests and other settings

Database
--------

In production environments you should use another database such as PostgreSQL instead of SQLite for fast and reliable caching.

Apache
------

Check the Apache config file example in blocksmurfer/examples/apache-example.conf
to see how to configure Blocksmurfer with Apache.
