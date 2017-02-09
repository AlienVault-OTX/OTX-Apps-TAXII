
import sys
import urllib2
import libtaxii
import libtaxii.clients as tc
import libtaxii.messages_11 as tm11


class Client:

    BINDING_STIX = 'urn:stix.mitre.org:xml:1.1.1'
    BINDING_TAXII = 'urn:taxii.mitre.org:message:xml:1.1'
    CLIENT_MSG = 'OTX Transform Client | rev 0'

    def __init__(self):
        # HTTP Server Connection
        self.scheme = None
        self.host = None
        self.port = None
        self.path = None
        self.query = None
        self.usr_name = None
        self.usr_pass = None
        self.usr_cert_pub = None
        self.usr_cert_prv = None
        self.svr_cert_pub = None  # This is typical the server CA pem file

        # libTAXII Support
        self.is_https = False

        # TAXII API Support
        self.collection = None
        self.subscription = None
        self.msg_type = None

    def _gen_client(self):
        if self.host:

            tc.socket.setdefaulttimeout(60)  # in seconds
            client = tc.HttpClient()

            if self.scheme:
                if 'https' in self.scheme.lower():
                    client.setUseHttps(True)

            if self.usr_pass:
                client.setAuthType(client.AUTH_BASIC)

            if self.usr_cert_prv:
                client.setAuthType(client.AUTH_CERT_BASIC)

            client.setAuthCredentials({
                    'username' : self.usr_name,
                    'password' : self.usr_pass,
                    'key_file' : self.usr_cert_prv,
                    'cert_file': self.usr_cert_pub
                })

            return client

    def gen_post(self, msg_type, xml):
        content_block = tm11.ContentBlock(tm11.ContentBinding(Client.BINDING_STIX), xml)

        if msg_type.lower() == 'inbox':
            post = tm11.InboxMessage(tm11.generate_message_id())
            post.content_blocks.append(content_block)
            post.message = Client.CLIENT_MSG

            if self.subscription:
                post.subscription_id = self.subscription

            if self.collection:
                post.destination_collection_names.append(self.collection)

            return post

    def snd_post(self, msg_type, xml):

        try:
            client = self._gen_client()

            return client.call_taxii_service2(
                host=self.host,
                port=self.port,
                path='/%s' % self.path,
                message_binding=Client.BINDING_TAXII,
                post_data=self.gen_post(msg_type, xml).to_xml(),
                get_params_dict=None,
                content_type=None,
                headers=None
                )

        except ValueError as err:
            msg = "CRITICAL: ValueError_Post: %s" % err

        except urllib2.HTTPError as err:
            msg = "CRITICAL: urllib2.HTTPError: %s , %s, " % err

        except urllib2.URLError as err:
            msg = "CRITICAL: urllib2.URLError: %s" % err

        except:
            msg = "UNKNOWN: %s :: \r \-> Response %s" % (str(sys.exc_info()[0]), None)

        print '%s | %s | %s' % (sys._getframe(), 'except', msg)

    def from_dict(self, d):
        if isinstance(d, dict):

            # Handle Server Config
            # ### URL scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]
            if d.get('server_ip'):
                self.host = str(d.get('server_ip'))
            if d.get('server_name'):
                self.host = str(d.get('server_name'))

            if self.host:
                if '://' in self.host:
                    scheme, host = self.host.split('://')
                    self.host = host
                    self.scheme = scheme

                if ':' in self.host:
                    host, port = self.host.split(':')
                    self.host = host
                    self.port = port

                if '/' in self.host:
                    host, path = self.host.split('/')
                    self.host = host
                    self.path = path

            if d.get('server_port'):
                self.port = str(d.get('server_port'))

            if self.port:
                if '/' in self.port:
                    port, path = self.port.split('/')
                    self.port = port
                    self.path = path

            # Handle TAXII Config
            if d.get('discovery_path'):
                self.path = str(d.get('discovery_path'))
            if self.path:
                if self.path[0] == '/':
                    self.path = self.path[1:]
                if self.path[-1] == '/':
                    self.path = self.path[:-1]

            if d.get('collection_name'):
                self.collection = str(d.get('collection_name'))

            #self._gen_client()

        else:
            print 'parameter passed: not dict() type'

    def push(self, xml, bind, collection_names, uri):
        # ### backward support of original script
        Client.BINDING = bind
        type_ = 'inbox'
        self.collection = collection_names
        self.path = uri
        self.gen_post(type_, xml)
