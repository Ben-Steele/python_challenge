"""
"GET", "WHERE", "AND", ",", "=", ">", and "<" are reserved words



GET * WHERE country = us 

{'key': country,
 'operation': =,
 'value': ['us']

"""

import copy

class Filter():

    def parse_query(self, query_string):
        
        query_string = query_string.strip()
        if not query_string[:4] == "GET ":
            raise ValueError('Invalid Query Format, must start with "GET"')

        query_string = query_string[4:]
        components = query_string.split('WHERE')
        fields = components[0]
        
        if len(components) > 2:
            raise ValueError('Invalid use of reserved word "WHERE"')
        elif len(components) = 1:
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

    def filter(self, data, conditions):
        filter_data = copy.deepcopy(data)
        ips_to_remove = set()
        for condition in conditions:
            key = condition['key']
            operation = condition['operation']
            value = condition['value']
            for ip, fields in filter_data.iteritems():
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
                del filter_data['ip']
