from ParseFile import IPParser
from GeoIPLookup import GeoIPLookup
from RDAPLookup import RDAPLookup
import pprint

class IPLookup():

    ip_parser = IPParser()
    geo_lookup = GeoIPLookup()
    rdap_lookup = RDAPLookup()

    def get_ip_info(self, ips, filter=None):
        ip_info = {}
        for ip in ips:
            ip_data = self.geo_lookup.get_geo_info(ip)
            ip_data.update(self.rdap_lookup.get_rdap_info(ip))
            ip_info[ip] = ip_data
        return ip_info

    def get_ips_from_text(self, text):
        return self.ip_parser.get_ip_addresses(text)

    def get_ips_from_file(self, file_path):
        return self.ip_parser.get_ip_addresses(file_path, from_file=True)

    def save_caches(self):
        self.geo_lookup.save_cache()
        self.rdap_lookup.save_cache()
    
if __name__ == "__main__":
    lookup = IPLookup()
    try:
        ips = lookup.get_ips_from_file('list_of_ips.txt')
        info = lookup.get_ip_info(ips)
        print len(info)
        pprint.pprint(info[ips[44]].keys())
        lookup.save_caches()
    except:
        lookup.save_caches()
        raise
    
