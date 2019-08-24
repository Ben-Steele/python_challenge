import requests
import json
import pprint
import SimpleCache

class RDAPLookup():
    """
    This class handles connections to an RDAP serverxb
    """
    
    BASE_URL = "https://rdap.arin.net/bootstrap/ip/"
    rdap_cache = SimpleCache.SimpleCache(save_file='RDAPCacheFile.txt', expiration_limit=30)
    
    def get_rdap_info(self, ip):
        """
        return the rdap info from arin.net for the given ip address
        input:
            - ip: an ip address
        output:
            The rdap info in a dictionary
        """
        cache_value = self.rdap_cache.get(ip)
        
        if cache_value is not None:
            rdap_info = cache_value
        else:
            url = self.BASE_URL + ip
            try:
                response = requests.request("GET", url)
                rdap_info = json.loads(response.text)
            except ValueError:
                # The ip was not found, return an empty dict
                if response.status_code == 404:
                    rdap_info = {}
                else:
                    raise
            self.rdap_cache.set(ip, rdap_info)
            
        return rdap_info

    def save_cache(self):
        """
        Save the cache of rdap data
        """
        self.rdap_cache.save()
        
if __name__ == "__main__":
    conn = RDAPLookup()
    pprint.pprint(conn.get_rdap_info('45.5.24.47'))
    conn.save_cache()
