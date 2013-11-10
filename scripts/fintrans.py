#!/usr/bin/python

""" 
  The implementation of the synthetic financial transaction stream,
  used in the main script of gess.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2013-11-08
@status: init
"""
import sys
import os
import socket
import logging
import string
import datetime
import random
import uuid
import csv

DEBUG = False

GESS_IP = "127.0.0.1"
GESS_UDP_PORT = 6900  # defines default port for a single gess running
SAMPLE_INTERVAL = 10  # defines the sampling interval (in seconds) for 
                      # reporting runtime statistics 

# ATM withdrawal data config
OSM_ATM_DATA = 'data/osm-atm-garmin.csv'
AMOUNTS = [20, 50, 100, 200, 300, 400]

if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT)


class FinTransSource(object):

  def __init__(self, send_port=GESS_UDP_PORT):
         #threading.Thread.__init__(self)
         self.send_port = send_port
         self.atm_loc = {}
         self._load_data()
  
  # loads the ATM location data from the OSM dump
  def _load_data(self):
    osm_atm_file = open(OSM_ATM_DATA, 'rb')
    atm_counter = 0
    try:
      reader = csv.reader(osm_atm_file, delimiter=',')
      for row in reader:
        lat, lon = row[1], row[0]
        atm_counter += 1
        self.atm_loc[str(atm_counter)] = lat, lon
        logging.debug('Loaded ATM location %s, %s' %(lat, lon))
    finally:
      osm_atm_file.close()
      logging.debug('Loaded %d ATM locations in total.' %(atm_counter))
  
  # creates a single financial transaction (ATM withdrawal) using
  # the following format:
  # {
  #   'timestamp': '2013-11-08T10:58:19.668225', 
  #   'lat': '37,3896661',
  #   'lon': '-5.9742199',
  #   'amount': 100, 
  #   'account_id': 'a335', 
  #   'transaction_id': '636adacc-49d2-11e3-a3d1-a820664821e3'
  # }
  def _create_fintran(self):
    rloc = random.choice(self.atm_loc.keys()) # obtain a random ATM location
    lat, lon = self.atm_loc[rloc]
    fintran = {
      'timestamp' : str(datetime.datetime.now().isoformat()),
      'lat' : str(lat),
      'lon' :  str(lon),
      'amount' : random.choice(AMOUNTS),
      'account_id' : 'a' + str(random.randint(1, 1000)),
      'transaction_id' : str(uuid.uuid1())
    }    
    logging.debug('Created financial transaction: %s' %fintran)
    return (fintran, sys.getsizeof(str(fintran)))

  # sends a single financial transaction via UDP
  def _send_fintran(self, out_socket, fintran):
    out_socket.sendto(str(fintran) + '\n', (GESS_IP, self.send_port))
    logging.debug('Sent financial transaction: %s' %fintran)
    
  ############# API ############################################################

  # dumps the OSM ATM data
  def dump_data(self):
    for k, v in self.atm_loc.iteritems():
      logging.info('ATM %s location: %s %s' %(k, v[0], v[1])) 
  
  # generates financial transactions (ATM withdrawals) and sends them
  # via UDP on port GESS_UDP_PORT as well as logs runtime statistics.
  def run(self):
    out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
    start_time = datetime.datetime.now()
    num_fintrans = 0
    tp_fintrans = 0
    num_bytes = 0
    tp_bytes = 0
  
    # the header of the TSV-formatted log statistics file
    # (all values are relative to the sample interval)
    #  sample_interval ... the sample interval (in seconds)
    #  num_fintrans ... financial transactions emitted
    #  tp_fintrans ... throughput of financial transactions (in thousands/second)
    #  num_bytes ... number of bytes emitted (in MB)
    #  tp_bytes ... throughput of bytes (in kB/sec)
    logging.info('sample_interval\tnum_fintrans\ttp_fintrans\tnum_bytes\ttp_bytes')
    while True:
      (fintran, fintransize) = self._create_fintran()
      self._send_fintran(out_socket, fintran)
      num_fintrans += 1
      num_bytes += fintransize
  
      end_time = datetime.datetime.now()
      diff_time = end_time - start_time
    
      if diff_time.seconds > (SAMPLE_INTERVAL - 1):
        tp_fintrans = (num_fintrans/1000) / diff_time.seconds
        tp_bytes = (num_bytes/1024) / diff_time.seconds
        logging.info('%s\t%d\t%d\t%d\t%d'
          %(
            diff_time.seconds,
            num_fintrans, 
            tp_fintrans,
            (num_bytes/1024/1024),
            tp_bytes
          )
        )
        start_time = datetime.datetime.now()
        num_fintrans = 0
        num_bytes = 0


################################################################################
## Main script

if __name__ == '__main__':
  fns = FinTransSource()
  # fns.dump_data()
  fns.run()