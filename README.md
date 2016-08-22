SilkRoute ![SilkRoute](./silkroute.png)
=========

![image](https://img.shields.io/pypi/v/silkroute.svg%0A%20%20%20%20%20:target:%20https://pypi.python.org/pypi/silkroute)

![image](https://img.shields.io/travis/debanjum/silkroute.svg%0A%20%20%20%20%20:target:%20https://travis-ci.org/debanjum/silkroute)

![image](https://readthedocs.org/projects/silkroute/badge/?version=latest%0A%20%20%20%20%20:target:%20https://silkroute.readthedocs.io/en/latest/?badge=latest%0A%20%20%20%20%20:alt:%20Documentation%20Status)

![image](https://pyup.io/repos/github/debanjum/silkroute/shield.svg%0A%20%20:target:%20https://pyup.io/repos/github/debanjum/silkroute/%0A%20%20:alt:%20Updates)

Marketplace for Anonymous Transactions

Features
--------

-   The project-let is enabled for travis-integration and python packaging
-   Tests can be run with Nose `nose -s -v` from project root
-   Replace SQLite Transaction Database with Ethereum Smart Contracts class
    -   Modular design should make replacing the SQLite DB fairly simple
    -   Replacing with Ethereum with enable a more a distributed, resilient database across network partitions

-   REST API available with [Sandman2](https://github.com/jeffknupp/sandman2) and SQlite3 backend for querying Market state from DB
	- `sandman2ctl sqlite+pysqlite:///silkroute.db` will create a basic REST API server
	
-   Reputation Scores: Base function already has skeleton for Entity Reputation Score
-   Write Tests for the Buyer and Seller Class
-   Add Entity(Buyer, Seller, Stocker) specific functionality to their classes
-   Using Context Managers to prevent DB locks

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
[street](https://thenounproject.com/feel_urban/collection/road/?oq=road&cidx=1&i=166362) Icon created by Viktor Fedyuk from the Noun Project

Free software: MIT license
Documentation: <https://silkroute.readthedocs.io>.

