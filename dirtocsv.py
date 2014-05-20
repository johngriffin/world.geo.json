#!/usr/bin/python

"""
Converts a directory of geojson files to a single csv ready to be imported into Dataseed.
"""

import os
import json
import csv, codecs, cStringIO
from pprint import pprint
        
INPATH = './countries'
OUTFILE = 'output.csv'

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# open csv writer on output.csv
ofile  = open(OUTFILE, "wb")
writer = UnicodeWriter(ofile)
# write header
writer.writerow(['id', 'short_label', 'label', 'area'])

# traverse countries subdirectory, and write a row in csv for each country
for root, dirs, files in os.walk(INPATH):    
    for file in files:
        filename = root + '/' + file
        print "processing " + filename
        with open(filename) as data_file:    
           data = json.load(data_file)
           
           # get variables from country file
           cid = data['features'][0]['id']
           feature = data['features'][0]
           cname = data['features'][0]['properties']['name']
           # write a row to output csv
           writer.writerow([cid, cname, cname, json.dumps(feature)])
        