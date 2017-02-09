# OTX-Apps-TAXII
Alienvault OTX TAXII connector

Set your Alienvault OTX API key and Taxii server in config.cfg.

This script can then be used to download pulses from OTX, and import them into your Taxii compliant client.

Run with:

- python2.7 otx-taxii.py first_run

the first time, then:

- python2.7 otx-taxii.py check_new

for updates


### Setting up config.cfg

Taxii server using HTTPS
```
[taxii]
server_ip=https://192.168.1.187 
```
- if your providing hostname _*or*_ IP address add https://

What is the diffrence _discovery_path_ vs _uri_?
```
[taxii]
discovery_path=/taxii-discovery-service/
uri=/taxii-data
```
- While in the vast majority of cases {Example: _Soltra Edge Taxii Server_} the _discovery_path_ and _uri_ can be used interchangeablely as the post_request captured independent of destination, there are some case where it does matter {Example: _DHS AIS Taxii inbox'ing(push)_}.
- In the rare cases where it does matter, you will need to looking at the TAXII Server's collection_info to find the path needed.
 

