# OTX-Apps-TAXII
Alienvault OTX TAXII connector

Set your Alienvault OTX API key and TAXII server in config.cfg.

This script can then be used to download pulses from OTX, and import them into your Taxii compliant client.

Run with:

- python2.7 otx-taxii.py first_run

the first time, then:

- python2.7 otx-taxii.py check_new

for updates.





### Setting up Config.cfg

For example a Taxii server using HTTPS might look like:
```
[taxii]
server_ip=https://192.168.1.187 
```
- You need to include https:// - whether its a hostname or an IP address

What is the difference between _discovery_path_ and _uri_?
```
[taxii]
discovery_path=/taxii-discovery-service/
uri=/taxii-data
```
- In most cases _discovery_path_ and _uri_ can be used interchangeablely - as the post_request captured is independent of the destination.
  
  {Example: _Soltra Edge Taxii Server_} 
  
  However there are some cases where it does matter:
  
 {Example: _DHS AIS Taxii inbox'ing(push)_}
 
- When it does matter, you will need to look at the TAXII Server's collection_info to find the path needed.
 

