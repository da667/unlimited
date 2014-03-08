REQUIRES PYTHON 2.7!

If you're interested in helping me port it to python 2.6 (for our CentOS/RHEL users out there), or Python 3.0 (for whatever reason), let me know.

Unlimited is my first foray into python scripting. It's a simple script that takes a csv file containing six values per row and writes out event_filter statements that can be included into a user's snort.conf file. 
Think of this as a rapid way of producing event_limit files for a large number of noisy rules efficiently and easily.

Usage: unlimited.py -i <infile> -o <outfile>

Infile format:

gen_id,sig_id,type_of_filter,track_by,count,seconds

gen_id: the snort generator id for the rule you want to set limits for. Numeric Value

sig_id: the snort signature ID (sid) for the rule in question. Numeric Value

type_of_filter: the type of event_filter to generate -- threshold, limit, or both

track_by: valid values include src or dst
--src: track event limits by source ip address
--dst: track event limits by destination ip address

count: number of events before triggering event_limit type. Numeric Value

seconds: amount of time, in seconds to recieve count number of limits before triggering. Numeric Value

Example: 

1,2801,limit,src,1,3600

results in....

event_filter gen_id 1, sig_id 2801, type limit, track by_src, count 1, seconds 3600

in plain english:

"for rule 1:2801, limit the number of events generated to only 1 event per hour, tracked by each unique source IP address triggering this rule."

You can then take the file generated and, using an include statement, include it in snort.conf, much the same way include is used to tell snort where the rule files are located. e.g.:

include /path/to/your/event_limit.conf

The script contains some very simple error checking, in that if a line contains less than 6 or more than 6 values, it will notify you, tell you which line caused the problem, and then continue processing your csv file. This includes blank lines in your csv file. However, the script will NOT validate you input proper values into the csv that will make syntactically correct event_filter statements. So if you include a header in your csv file, unlimited will parse it, but will NOT syntactically check that it produced a valid event_filter statement. Put simply: No headers, and no Blank lines! I've included a sample file, test.csv that includes two valid entries so you can see an example of the format the script expects.

Bugs? Problems?

contact info:
twitter: <at>da_667
e-mail: deusexmachina<at>gmail<dot>com