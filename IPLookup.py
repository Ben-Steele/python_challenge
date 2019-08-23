from ParseFile import IPParser
from GeoIPLookup import GeoIPLookup
from RDAPLookup import RDAPLookup
from Filter import QueryManager

import argparse
import pprint

class IPLookup():

    ip_parser = IPParser()
    geo_lookup = GeoIPLookup()
    rdap_lookup = RDAPLookup()
    query_manager = QueryManager()

    def get_ip_info(self, ips, query=None):
        ip_info = {}
        for ip in ips:
            ip_data = self.geo_lookup.get_geo_info(ip)
            ip_data.update(self.rdap_lookup.get_rdap_info(ip))
            ip_info[ip] = ip_data
        if query:
            ip_info = self.query_manager.execute_query(ip_info, query)
        return ip_info

    def get_ips_from_text(self, text):
        return self.ip_parser.get_ip_addresses(text)

    def get_ips_from_file(self, file_path):
        return self.ip_parser.get_ip_addresses(file_path, from_file=True)

    def save_caches(self):
        self.geo_lookup.save_cache()
        self.rdap_lookup.save_cache()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='ip_file', help = 'The path to the file containing ip addresses')
    parser.add_argument('-q', dest='query', help = 'The query string to filter results')
    
    return parser.parse_args()

        
if __name__ == "__main__":
    lookup = IPLookup()
    args = parse_args()
    
    try:
        ips = lookup.get_ips_from_file(args.ip_file)
        info = lookup.get_ip_info(ips, args.query)#"GET events, ipVersion, city WHERE country_name = United States AND region_code < CO")
        pprint.pprint(info)
        print len(info)
        lookup.save_caches()
    except:
        lookup.save_caches()
        raise
    
