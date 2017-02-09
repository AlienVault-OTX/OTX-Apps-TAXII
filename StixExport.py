from stix.core import STIXPackage, STIXHeader
from cybox.core import Observable
from cybox.objects.address_object import Address
from cybox.objects.uri_object import URI
from cybox.objects.domain_name_object import DomainName
from cybox.objects.file_object import File
from stix.exploit_target import Vulnerability
from cybox.objects.mutex_object import Mutex
from cybox.common import Hash
from stix.indicator import Indicator, CompositeIndicatorExpression
from stix.common import InformationSource, Identity
from cybox.common import Time
from lxml import etree as et
from stix.common.vocabs import PackageIntent
from stix.core import STIXPackage
from mixbox.idgen import set_id_namespace
from mixbox.namespaces import Namespace
from IPy import *

PULSE_SERVER_BASE = "https://otx.alienvault.com/"
STIXNAMESPACE =  Namespace("https://otx.alienvault.com", "alienvault-otx")
set_id_namespace(STIXNAMESPACE)

class StixExport:
    def __init__(self, pulse):
        self.stix_package = STIXPackage()
	self.stix_header = STIXHeader()
        self.pulse = pulse
        self.hash_translation = {"FileHash-MD5": Hash.TYPE_MD5, "FileHash-SHA1": Hash.TYPE_SHA1,
                                 "FileHash-SHA256": Hash.TYPE_SHA256}
        self.address_translation = {"IPv4": Address.CAT_IPV4, "IPv6": Address.CAT_IPV6}
        self.name_translation = {"domain": URI.TYPE_DOMAIN, "hostname": URI.TYPE_DOMAIN}

    def build(self):
        self.stix_header.title = self.pulse["name"]
        self.stix_header.description = self.pulse["description"]
        self.stix_header.short_description = "%spulse/%s" % (PULSE_SERVER_BASE, str(self.pulse["id"]))
        self.stix_header.package_intents.append(PackageIntent.TERM_INDICATORS)
        self.stix_header.information_source = InformationSource()
        self.stix_header.information_source.time = Time()
        self.stix_header.information_source.description = "Alienvault OTX - https://otx.alienvault.com/"
        self.stix_header.information_source.time.produced_time = self.pulse["modified"]
        self.stix_header.information_source.identity = Identity()
        self.stix_header.information_source.identity.name = "Alienvault OTX"

        self.stix_package.stix_header = self.stix_header

    	hashes = []
    	addresses = []
    	domains = []
    	urls = []
    	mails = []


        for p_indicator in self.pulse["indicators"]:
            if p_indicator["type"] in self.hash_translation:
                new_ind = Indicator()
                new_ind.description = p_indicator["description"]
                new_ind.title = "%s from %spulse/%s" % (p_indicator["indicator"], PULSE_SERVER_BASE, str(self.pulse["id"]))
                file_ = File()
                hash_ = Hash(p_indicator["indicator"], self.hash_translation[p_indicator["type"]])
                file_.add_hash(hash_)
                observable_ = Observable(file_)


            elif p_indicator["type"] in self.address_translation:
                new_ind = Indicator()
                new_ind.description = p_indicator["description"]
                new_ind.title = "%s from %spulse/%s" % (p_indicator["indicator"], PULSE_SERVER_BASE, str(self.pulse["id"]))
                ipv4_ = Address.from_dict({'address_value': p_indicator["indicator"],
                                           'category': self.address_translation[p_indicator["type"]]})
                observable_ = Observable(ipv4_)


            elif p_indicator["type"] in self.name_translation:
                new_ind = Indicator()
                new_ind.description = p_indicator["description"]
                new_ind.title = "%s from %spulse/%s" % (p_indicator["indicator"], PULSE_SERVER_BASE, str(self.pulse["id"]))
                domain_ = DomainName.from_dict({'value': p_indicator["indicator"], 'type':'FQDN'})                
                observable_ = Observable(domain_)


            elif p_indicator["type"] == "URL":
                new_ind = Indicator()
                new_ind.description = p_indicator["description"]
                new_ind.title = "%s from %spulse/%s" % (p_indicator["indicator"], PULSE_SERVER_BASE, str(self.pulse["id"]))
                url_ = URI.from_dict({'value': p_indicator["indicator"], 'type': URI.TYPE_URL})
                observable_ = Observable(url_)


            elif p_indicator["type"] == "email":
                email_ = Address.from_dict({'address_value': p_indicator["indicator"], 'category': Address.CAT_EMAIL})
                observable_ = Observable(email_)

            #elif p_indicator["type"] == "CVE":
            #    vuln_ = Vulnerability()
            #    vuln_.cveid = p_indicator["indicator"].upper()
            #    observable_ = Observable(vuln_)

            elif p_indicator["type"] == "Mutex":
                mutex_ = Mutex.from_dict({'named': True, 'name': p_indicator["indicator"]})
                observable_ = Observable(mutex_)

            elif p_indicator["type"] == "CIDR":
                nrange = IP(p_indicator["indicator"])
                nrange_values = nrange.strNormal(3).replace("-", ",")
                ipv4_ = Address.from_dict({'address_value': nrange_values, 'category': Address.CAT_IPV4})
                ipv4_.address_value.condition = "InclusiveBetween"
                observable_ = Observable(ipv4_)

            else:
                continue


            mind = Indicator()
            mind.description = p_indicator["description"]
            mind.title = "%s from %spulse/%s" % (p_indicator["indicator"], PULSE_SERVER_BASE, str(self.pulse["id"]))
            observable_.title = "%s - %s" % (p_indicator["type"], p_indicator["indicator"])
            mind.add_observable(observable_)
            self.stix_package.add_indicator(mind)

            
	   
    def to_xml(self):
        return self.stix_package.to_xml()
