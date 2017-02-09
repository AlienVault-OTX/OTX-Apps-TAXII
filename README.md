# OTX-Apps-TAXII
Alienvault OTX TAXII connector

Set your Alienvault OTX API key and Taxi server in config.cfg.
This script can then be used to download pulses from OTX, and import them into your Taxii complient client

Run with:

- python2.7 otx-taxii.py first_run

the first time, then:

- python2.7 otx-taxii.py check_new

for updates