import re

class IPParser():
    """
    This class contains methods used to extract ip addresses from text
    """
    
    def get_ip_addresses(self, input_text, from_file=False):
        """
        Given raw text, this method extracts all the valid ip addresses within it
        input can be a string or a path to a file, if it is a path to a file, file_path must be set to True
        Inputs:
            - input_text: The raw text to extract ip addresses from (either string of text or path to the file with text)
            - file_path: Set to True if input_text is a file path, otherwise set to False
        Output: A list of ip addresses
        """
        
        if from_file:
            with open(input_text, 'r') as input_file:
                raw_text = input_file.read()
        else:
            raw_text = input_text
            
        # find all ip addresses in the text, this will also find invalid ips such as 999.999.999.999
        ip_addresses = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', raw_text)

        #filter out any invalid ips that were found
        valid_ips = []
        for ip in ip_addresses:
            if self.is_valid_ip(ip):
                valid_ips.append(ip)

        return valid_ips
        
    def is_valid_ip(self, ip_address):
        """
        Validate that each component of the ip is from 0-255
        Inputs: 
            - ip_address(str): the string to validate
        output: True if ip_address is a valid ip address, False if not
        """
        components = ip_address.split('.')
        for component in components:
            if int(component) > 255:
                return False
        return True

if __name__ == "__main__":
    my_parser = IPParser()
    print my_parser.get_ip_addresses(input_text='list_of_ips.txt', file_path=True)
