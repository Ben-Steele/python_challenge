"""
Query Language Definition:

All queries start with "GET", signifying you want to retrieve data
e.g.
    GET ...

After GET, you may list fields that you want to recieve by writing the names of the fields separated by commas.
  You may use "*" to signify that you want to recieve all fields available
e.g.
    GET field1, field2, field3 ...
    GET * ...

After indicating the fields you want to recieve, you may filter the results using a "where" clause.  
The "where" clause must start with the keyword "WHERE" and it can contain multiple conditions separated by the keyword "AND"
e.g.
    GET field1, field2, field3 WHERE condition1 AND condition2 AND condition3

Conditions can use three operations; "=", "<", ">".  The condition must list the field name first, then the operator, then the comparison value.
  All values will be compared as string objects.
e.g.
    field1 > 5
    field4 = my condition's value

You may specify that a single field can be one of many values by having a comma separated list of values after a "=" operator
e.g.
    field2 = my condition's value, 5, another value

Example of a full query expression:
    GET field1, field2, field3 WHERE field1 > 5 AND field2 = my condition's value, 5, another value AND field6 < 255
    GET * WHERE field3 = abcde

"GET", "WHERE", "AND", ",", "=", ">", and "<" are reserved words and cannot be used except as syntax in the query



GET * WHERE country = us 
"""

import copy

class QueryManager():


    def execute_query(self, data, query):
        fields, conditions = self.parse_query(query)
        data = self.filter_data(data, conditions)
        data = self.limit_fields(data, fields)
        return data
    
    def parse_query(self, query_string):
        """
        Parse the query string into a machine readable format so it can be used to filter the results
        input:
            - query_string: the query string to be parsed
        output:
            - A tuple containing 2 elements:
                1. A list of the fields to be returned for each record
                2. A list of dictionaries where each dictionary represents a condition for the data and has the format:
                    {'key': field name,
                     'operation': either "=", "<", or ">"
                     'value': the value to compare the field against
        """
        query_string = query_string.strip()
        if not query_string[:4] == "GET ":
            raise ValueError('Invalid Query Format, must start with "GET"')

        query_string = query_string[4:]
        components = query_string.split('WHERE')
        fields = components[0]
        
        if len(components) > 2:
            raise ValueError('Invalid use of reserved word "WHERE"')
        elif len(components) == 1:
            conditions = None
        else:
            conditions = components[1]

        fields = fields.split(',')
        fields = [f.strip() for f in fields]

        condition_list = []

        if conditions:
            conditions = conditions.split('AND')
            conditions = [c.strip() for c in conditions]
            for condition in conditions:
                condition_dict = {}
                if "=" in condition:
                    condition_dict['operation'] = "="
                    condition = condition.split('=')
                    if len(condition) != 2:
                        raise ValueError('invalid condition: %s' % ''.join(condition))
                    condition_dict['key'] = condition[0].strip()
                    value = condition[1].strip()
                    if ',' in value:
                        value = value.split(',')
                        value = [v.strip() for v in value]
                    else:
                        value = [value]
                    condition_dict['value'] = value
                        
                elif ">" in condition:
                    condition_dict['operation'] = ">"
                    condition = condition.split('>')
                    if len(condition) != 2:
                        raise ValueError('invalid condition: %s' % ''.join(condition))
                    condition_dict['key'] = condition[0].strip()
                    condition_dict['value'] = condition[1].strip()
                elif "<" in condition:
                    condition_dict['operation'] = "<"
                    condition = condition.split('<')
                    if len(condition) != 2:
                        raise ValueError('invalid condition: %s' % ''.join(condition))
                    condition_dict['key'] = condition[0].strip()
                    condition_dict['value'] = condition[1].strip()
                else:
                    raise ValueError('invalid condition: %s' % ''.join(condition))
                condition_list.append(condition_dict)

        return fields, condition_list

    def filter_data(self, data, conditions):
        """
        Remove records from the data that do not match the conditions provided
        inputs:
            - data: a dictionary.  The values of all elements in this dictionary are dictionaries where the keys are field names
                {ip: {field1: _____, field2: _____}
            - conditions: a list of conditions as described in parse_query
        output:
            - The data is returned in the same format it was given in, with the records that didn't match the conditions removed
        """
        for condition in conditions:
            ips_to_remove = set()
            key = condition['key']
            operation = condition['operation']
            value = condition['value']
            for ip, fields in data.iteritems():
                # If field to filter on doesn't exist, remove this ip in the results
                if condition['key'] in fields:
                    # If the current ip's fields don't satisfy the condition, remove it from results
                    if operation == '=' and not (fields[key] in value):
                        ips_to_remove.add(ip)
                    elif operation == '>' and not (fields[key] > value):
                        ips_to_remove.add(ip)
                    elif operation == '<' and not (fields[key] < value):
                        ips_to_remove.add(ip)
                else:
                    ips_to_remove.add(ip)
                    
            for ip in ips_to_remove:
                del data[ip]
                
        return data

    def limit_fields(self, data, fields):
        """
        Takes in "data" and returns "data" with only fields that are in "fields"
        inputs:
            - data: same as filter_data
            - fields: a list of field names
        outputs:
            - the data is returned in the same format it was given in, but each record only contains fields that are in "fields"
        """
        if fields[0] == '*':
            return data
        limited_data = {}
        for ip, attributes in data.iteritems():
            new_attributes = {}
            for attribute, value in attributes.iteritems():
                if attribute in fields:
                    new_attributes[attribute] = value
            limited_data[ip] = new_attributes

        return limited_data
    
        
