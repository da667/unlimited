#Version 1.0
##Imports##
#Import sys to ensure soft spaces are NOT inserted into written files
#Import csv to take csv-delimited data
#Argparse for fancy cli args
#textwrap for a fancy help/description output

import sys, csv, argparse, textwrap

#Initialize argparse and print the big ass description and help usage block if -h or --help is used

parser = argparse.ArgumentParser(
formatter_class=argparse.RawDescriptionHelpFormatter,
description = textwrap.dedent('''
                    unlimited.py
                Brought to you by ...
                    @da_667
                ---------------------
Generates event_filter files from a comma delimited data file
Usage: unlimited.py -i <infile> -o <outfile>
Infile format:
gen_id,sig_id,type_of_filter,track_by,count,seconds

gen_id: the snort generator id for the rule you want to set limits for

sig_id: the snort signature ID (sid) for the rule in question

type_of_filter: the type of event_filter to generate -- threshold, limit, or both

track_by: src -- track by source IP dst -- track by destination IP

count: number of events be fore triggering event_limit type

seconds: amount of time, in seconds to recieve count number of limits before triggering.

Example: 1,2801,limit,src,1,3600

results in....

event_filter gen_id 1, sig_id 2801, type limit, track by_src, count 1, seconds 3600
'''))

#add infile and outfile arguments, make them mandatory and provide more detailed output as to what they are for when -h or --help is used.

parser.add_argument('-i', dest="infile", required=True, help="The name of the file containing the space-delimited data for generating event_filters.")
parser.add_argument('-o', dest="outfile", required=True, help="The name of the file to output your complete event_filter statements")
args = parser.parse_args()
print "\033[92m[*]\033[0m Using %s as input file.." %args.infile
print "\033[92m[*]\033[0m And %s as output file..." %args.outfile

#This serves as a fail-safe to ensure spaces are NOT inserted into the text file we write to.

sys.stdout.softspace = False

#This is to ensure row numbers (read: line numbers) are tracked by a human-understandable index e.g. line 1 instead of line 0, so users know what line my script thinks is mal-formed.

row_num = 1

#A with statement within a with statement. 
#This is the only way I could find to ensure that both files were open for reading and writing at the same time.
#Do you know a cleaner way? tell me.

#Opens our output file for writing, and our input file for reading. The csv.reader is explicitly configured to NOT put quotes around any row values. Just in case.
#Then we iterate over every row/line. If the number of columns is greater than OR less than 6, we inform the user what line caused the error, skip that line, and continue processing.
#Just to be clear: this WILL barf on blank lines, but it will skip them and keep parsing.

with open(args.outfile, 'w+') as o:
        with open(args.infile, 'rb') as f:
                reader=csv.reader(f, quoting = csv.QUOTE_NONE)
                for row in reader:
                        if len(row) < 6:
                                print "\033[93m[*]\033[0m Line", row_num, "is malformed, it's missing values. It contains", str(len(row)), "values, this number is less than 6. Skipping."
                                row_num+=1
                                continue
                        elif len(row) > 6:
                                print "\033[93m[*]\033[0m Line", row_num, "is malformed, it has too many values. It contains", str(len(row)), "values, this number is greater than 6. Skipping."
                                row_num+=1
                                continue
                        else:
                                o.write ("event_filter gen_id %s, sig_id %s, type %s, track by_%s, count %s, seconds %s\n" % (row[0], row[1], row[2], row[3], row[4], row[5]))
                                row_num+=1
print "\033[92m[*]\033[0m Done!"
exit()
