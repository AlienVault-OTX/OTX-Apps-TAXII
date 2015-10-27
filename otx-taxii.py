from StixExport import StixExport
from OTXv2 import OTXv2
from cabby import create_client
import ConfigParser
import datetime
import sys

binding = 'urn:stix.mitre.org:xml:1.1.1'

config = ConfigParser.ConfigParser()
config.read('config.cfg')


otx = OTXv2(config.get('otx', 'key'))
client = create_client(config.get('taxii', 'server_ip'), discovery_path=config.get('taxii', 'discovery_path'))
client.set_auth(username=config.get('taxii', 'username'), password=config.get('taxii', 'password'))


def saveTimestamp(timestamp=None):
	mtimestamp = timestamp
	if not timestamp:
		mtimestamp = datetime.datetime.now().isoformat()

	fname = "timestamp"
	f = open(fname, "w")
	f.write(mtimestamp)
	f.close()

def readTimestamp():
	fname = "timestamp"
	f = open(fname, "r")
	mtimestamp = f.read()
	f.close()
	return mtimestamp

def sendTAXII(first=True):
	if first:
		mtimestamp = None
	else:
		mtimestamp = readTimestamp()

	if first:
		for pulse in otx.getall_iter():
			if not mtimestamp:
				mtimestamp = pulse["modified"]
			st = StixExport(pulse)
			st.build()
			print "Sending %s" % pulse["name"]
			client.push(st.to_xml(), binding, collection_names=[config.get('taxii', 'collection_name')], uri=config.get('taxii', 'uri'))
		saveTimestamp(mtimestamp)
	else:
		pulses = otx.getsince(mtimestamp)
		mtimestamp = None
		for pulse in pulses:
                        if not mtimestamp:
                                mtimestamp = pulse["modified"]
                        st = StixExport(pulse)
                        st.build()
                        print "Sending %s" % pulse["name"]
                        client.push(st.to_xml(), binding, collection_names=[config.get('taxii', 'collection_name')], uri=config.get('taxii', 'uri'))
		saveTimestamp(mtimestamp)
		print "%d new pulses" % len(pulses)

def usage():
	print "Usage:\n\totx-taxii.py [first_run|check_new]"
	sys.exit(0)

if __name__ == "__main__":
	try:
		op = sys.argv[1]
	except:
		usage()
	if op == "first_run":
		sendTAXII(True)
	elif op == "check_new":
		sendTAXII(None)
	else:
		usage()
