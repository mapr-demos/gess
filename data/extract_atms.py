#!/usr/bin/python

""" 
  Extracts ATM locations from OSM files and writes it out as CSV file like so:
  
    -8.8051236,42.4003502,"Atm"
    1.2985738,38.9833171,"Atm"
    4.0733016,39.9029528,"Atm"
    -1.7720182,43.3408758,"Atm"
  
  Example usage: python extract_atms.py sf-bay-area.osm
  
  Note: the output file will have the same name as the input file but with a 
        .csv file extension. In the above usage example this would mean the 
        resulting output file is: sf-bay-area.csv

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2014-01-27
@status: init
"""
import sys
import logging
import csv
from imposm.parser import OSMParser

DEBUG = False

if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT)
  

# Handles ATM location extraction via nodes-callback
class ATMLocExtractor(object):
  NODE_PROGRESS_CHECKMARK = 1000
  atm_list = []
  node_num = 0

  # writes out the list of extracted ATMs in a CSV file the generator understands
  def dump_result(self, result_file_name):
    result_file  = open(result_file_name, 'wb')
    result_file_writer = csv.writer(
        result_file,
        quoting=csv.QUOTE_NONNUMERIC,
        delimiter=','
    )
    for atm in self.atm_list:
      logging.debug('%s' %(atm))
      row = [atm['lon'], atm['lat'], atm['name'].replace('\n', ' ')]
      result_file_writer.writerow(row)


  # callback method for extracting ATM position from nodes
  # for callback params doc see: https://github.com/omniscale/imposm-parser/blob/master/doc/source/concepts.rst 
  def atm_loc(self, nodes):
        
        lon = lat = 0
        name = ''
        for osmid, desc, loc in nodes:
            # status marker
            self.node_num += 1
            if self.node_num % self.NODE_PROGRESS_CHECKMARK == 0:
              logging.debug('... at node %d' %self.node_num)

            # there are two types of nodes, either 1. tagged with 'amenity': 'bank'/'atm': 'yes' where we get the label from 'name' or 2. 'amenity': 'atm', then we get the label from 'operator'
            # 'amenity': 'bank' and 'atm': 'yes' -> use 'name'              
            if ('atm' in desc):
              lon = loc[0]
              lat = loc[1]
              try:
                name = desc['name']
              except:
                name = 'ID_%s' %osmid                
              logging.debug('Found ATM called %s with ID %d at lon %s, lat %s' %(name, osmid, lon, lat))
              self.atm_list.append({'lon' : lon, 'lat' : lat, 'name' : name })

            # 'amenity': 'atm' -> use 'operator'
            if ('amenity' in desc and desc['amenity'] == 'atm'):
              lon = loc[0]
              lat = loc[1]
              try:
                name = desc['operator']
              except:
                name = 'ID_%s' %osmid                
              logging.debug('Found ATM called %s with ID %d at lon %s, lat %s' %(name, osmid, lon, lat)) 
              self.atm_list.append({'lon' : lon, 'lat' : lat, 'name' : name })
            

################################################################################
## Main script

if __name__ == '__main__':
  try:
    input_osm = sys.argv[1]
    output_csv = input_osm.replace('.osm', '.csv')
    logging.info('Trying to extract ATM locations from %s:' %input_osm)
    ale = ATMLocExtractor()
    p = OSMParser(concurrency=1, nodes_callback=ale.atm_loc)
    p.parse(input_osm)
    ale.dump_result(output_csv)
    logging.info('Extracted %d ATMs and stored it in %s' %(len(ale.atm_list), output_csv))
  except:
    print 'No OSM input file specified! Usage, for example as follows: python extract_atms.py sf-bay-area.osm'