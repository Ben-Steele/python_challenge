import datetime
import os
import json

class SimpleCache():
    """
    Very simple cache class that is sufficient for this implementation
    """
    
    def __init__(self, save_file = None, expiration_limit = None):
        """
        Inputs:
            - save_file: a path to a file.  If provided, the cache can be saved to 
                                   this location on shutdown and loaded from it on instantiation
            - expiration_limit: the number of days an object can stay in the cache for before 
                                 it must be reloaded
        """

        self.save_file = save_file
        self.expiration_limit = expiration_limit
        self.memory = {}
        self.load()
        
    def get(self, cache_key):
        if cache_key in self.memory:
            cache_value =  self.memory[cache_key]
            if self.is_expired(cache_value):
                return_value = None
            else:
                return_value = cache_value['data']
        else:
            return_value = None
        return return_value

    def set(self, key, value):
        if self.expiration_limit:
            expiration = datetime.datetime.now() + datetime.timedelta(days=self.expiration_limit)
        else:
            expiration = datetime.MAXYEAR
        cache_value = {'expiration': str(expiration), 'data': value}
        self.memory[key] = cache_value
    
    def is_expired(self, cache_value):
        """
        determine whether the cache entry is expired
        """
        expiration = datetime.datetime.strptime(cache_value['expiration'], '%Y-%m-%d %H:%M:%S.%f')
        if expiration < datetime.datetime.now():
            return True
        else:
            return False
        
    def save(self):
        """
        Save cache contents into a file
        """
        if self.save_file:
            with open(self.save_file, 'w') as f:
                f.write(json.dumps(self.memory))

    def load(self):
        """
        load file contents into the cache
        """
        if self.save_file and os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                self.memory = json.loads(f.read())
