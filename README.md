bikestats
=========

Scrape and save information from motorcyclespecs.co.za. This is for local usage and consumption
of data for statistics or whatever, and to have an offline copy.

Usage
-----

After cloning this repository, you should first scrape the entire website by running

    download.sh

During or after website scrape (which may take 3-4 hours depending), set up your virtualenv:

    virtualenv .
    source bin/activate
    pip install -r requirements.txt

Add 'bikestats' to your INSTALLED_APPS. To ingest the scraped data, run models.parse_all:

    from bikestats.models import parse_all
    parse_all('www.motorcyclespecs.co.za')

TODO
----

* Fix wet weight to always be in lbs
* Fix torque to always be ft-lbs

License
-------

Copyright (c) 2016 Jon Robison

See included LICENSE for licensing information
