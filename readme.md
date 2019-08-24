IPLookup

This project allows you to parse text for valid ip addresses, then retrieve and filter RDAP and geoip data for those ips.

Thoughts:

The biggest issue with this implementation is that geoip and RDAP must be queried one ip at a time.  The caching helps with
this, but if tens of thousands of new ips are being queried at the same time it can take hours to load all the RDAP and geoip
data.  This was a limitation of the APIs I chose to use and in a production environment I would spend much more time looking
through APIs to see if there is something that can handle larger batches of ip addresses.  I decided my time is better spent
showing my coding abilities than doing that.

It is also not ideal that the symbols used for syntax in the query language cannot be used anywhere else.  With more time,
I would handle quotations so that text within quotes is not processed for query syntax.

Setup:

The only dependency this project has is the Requests python module.  Requests must be installed before the IPLookup can be run.

I suggest that you use the cache files provided in the project because it can take a long time to load all the data if you
are querying thousands of ip addresses.  As long as the cache files are in the same folder as the rest of the project and
no names are changed, they will be used automatically.

The program is run through the command line. The options are listed below.

-h, --help  show this help message and exit
-f IP_FILE  The path to the file containing ip addresses
-q QUERY    The query string to filter results

Example queries:

python IPLookup.py -f list_of_ips.txt -q "GET city, region_name, country_name WHERE country_name = Spain, Brazil AND region_code > H"

python IPLookup.py -f list_of_ips.txt -q "GET * WHERE country_name = United States AND region_code = CO"



Query Language Definition:

All queries start with "GET", signifying you want to retrieve data.
e.g.
    GET ...

After GET, you may list fields that you want to recieve by writing the names of the fields separated by commas.
  You may use "*" to signify that you want to recieve all fields available.
e.g.
    GET field1, field2, field3 ...
    GET * ...

After indicating the fields you want to recieve, you may filter the results using a "where" clause.  
The "where" clause must start with the keyword "WHERE" and it can contain multiple conditions separated by the keyword "AND".
e.g.
    GET field1, field2, field3 WHERE condition1 AND condition2 AND condition3

Conditions can use three operations; "=", "<", ">".  The condition must list the field name first, then the operator, then the comparison value.
  All values will be compared as string objects.
e.g.
    field1 > 5
    field4 = my condition's value

You may specify that a single field can be one of many values by having a comma separated list of values after a "=" operator.
e.g.
    field2 = my condition's value, 5, another value

Examples of a full query expression:
    GET field1, field2, field3 WHERE field1 > 5 AND field2 = my condition's value, 5, another value AND field6 < 255
    GET * WHERE field3 = abcde

"GET", "WHERE", "AND", ",", "=", ">", and "<" are reserved words and cannot be used except as syntax in the query.



