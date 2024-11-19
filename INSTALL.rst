Blocksmurfer Installation
=========================

Install packages needed for Bitcoinlib:

.. code-block:: bash

    $ sudo apt install build-essential python3-dev libgmp3-dev libssl-dev python3-virtualenv


Create a virtual environment

.. code-block:: bash

    $ python3 -m venv venv/blocksmurfer
    $ source venv/blocksmurfer/bin/activate


Download Blocksmurfer and install requirements.

.. code-block:: bash

    $ git clone https://github.com/1200wd/blocksmurfer.git
    $ cd blocksmurfer
    $ python3 -m pip install -r requirements.txt

Copy configuration file and update secret key

.. code-block:: bash

    $ cp config.example.py config.py
    $ nano config.py

Now you can test your install and run flask directly

.. code-block:: bash

    $ flask run
    $ #  or if you want to accept connection from other hosts
    $ flask run --host 0.0.0.0


or with gunicorn

.. code-block:: bash

    $ ./boot.sh

Blocksmurfer should run now on http://localhost:5000


Docker
------

You can also create a basic local node with a docker image

.. code-block:: bash

    $ docker container run --rm --name blocksmurfer -d -p 5000:5000 blocksmurfer/blocksmurfer

For more information about this image: https://hub.docker.com/r/blocksmurfer/blocksmurfer

Or build and run locally from Dockerfile configuration

.. code-block:: bash

    $ docker build -t blocksmurfer:latest .
    $ docker run --rm -p 0.0.0.0:5000:5000 -it blocksmurfer


Configuration
-------------

* Please do not forget to enter a new secret key!
* Select the networks you would like to support and update other settings if you like in the configuration

Please note:

* Remove Blocksmurfer from Bitcoinlib's provider definitions in ./bitcoinlib/providers.json to avoid recursive loops.
* Preferably use your own Bcoin node, or request for an API key at one of the providers to avoid provider errors.
* In the Bitcoinlib config file (./bitcoinlib/config.ini) you can change the loglevel, log location, timeout for requests and other settings
* If you use your own Bcoin node or have an API key, you might want to increase the max_transaction setting in config.ini to 100 or more.
* If you get errors when trying to retrieve blocks or see negative numbers in confirmations, this probably means the blockchain is not fully synced yet. This can take several days for a Bcoin or Bitcoind node.


Database
--------

In production environments you should use another database such as PostgreSQL instead of SQLite for fast and reliable caching.

To install PostgreSQL:

.. code-block:: bash

    $ apt install postgresql postgresql-contrib libpq-dev
    $ pip install psycopg2

Apache
------

Check the Apache config file example in blocksmurfer/examples/apache-example.conf to configure Blocksmurfer with Apache.

* Install Apache and create log directories

.. code-block:: bash

    $ sudo apt install apache2
    $ sudo mkdir /var/log/apache2/blocksmurfer

* Add the proxy modules

.. code-block:: bash

    $ sudo a2enmod ssl
    $ sudo a2enmod proxy
    $ sudo a2enmod proxy_http

* Copy the apache config file to /etc/apache2/sites-available, update the settings and create the link in /etc/apache2/sites-available

* Now run blocksmurfer/boot.sh and your blockexplorer should be up and running
