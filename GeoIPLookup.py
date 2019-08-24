import requests
import json
import pprint
import SimpleCache

class GeoIPLookup():

    # I chose this geo ip api because its free, simple to set up, and simple to use
    # The big downside is that I cannot query multiple ips in one query
    BASE_URL = "https://freegeoip.app/json/"
    
    HEADERS = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    cache = SimpleCache.SimpleCache(save_file = 'GeoCacheFile.txt', expiration_limit = 30)

    def get_geo_info(self, ip):
        """
        return the geoip info from freegeoup.app for the given ip address
        input:
            - ip: an ip address
        output:
            The geoip info in a dictionary
        """
        cache_value = self.cache.get(ip)
        if cache_value is not None:
            geo_info = cache_value
        else:
            url = self.BASE_URL + ip
            response = requests.request("GET", url, headers=self.HEADERS)
            geo_info = json.loads(response.text)
            self.cache.set(ip, geo_info)

        return geo_info

    def save_cache(self):
        """
        Save the cached geoip data
        """
        self.cache.save()
        
if __name__ == "__main__":
    conn = GeoIPLookup()
    pprint.pprint(conn.get_geo_info('189.36.244.240'))
    conn.save_cache()
