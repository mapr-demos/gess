#!/usr/bin/python

""" 
  The main script of gess, the generator for synthetic streams 
  of financial transactions.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2013-11-07
@status: init
"""
import sys
import os
import socket
import logging
import string
import datetime
import json
import random
import uuid

from os import curdir, pardir, sep

DEBUG = False
GESS_IP = "127.0.0.1"
GESS_UDP_PORT = 6900  # defines default port for a single gess running
SAMPLE_INTERVAL = 5   # defines the sampling interval (in seconds) for 
                      # reporting runtime statistics 


if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT)


# creates a single financial transaction
def create_fintran():
  fintran = {
    'timestamp' : str(datetime.datetime.now().isoformat()),
    'transaction_id' : str(uuid.uuid4()),
    'account_from' : random.randint(1, 1000),
    'account_to' : random.randint(1, 1000),
    'amount' : random.randint(1, 10000000)
  }    
  logging.debug('Created financial transaction: %s' %fintran)
  return (fintran, sys.getsizeof(str(fintran)))

# sends a single financial transaction via UDP
def send_fintran(out_socket, fintran):
  out_socket.sendto(str(fintran) + '\n', (GESS_IP, GESS_UDP_PORT))
  logging.debug('Sent financial transaction: %s' %fintran)
    
def run_gess():
  out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
  start_time = datetime.datetime.now()
  num_fintrans = 0
  tp_fintrans = 0
  num_bytes = 0
  tp_bytes = 0
  
  # the header of the TSV formatted log statistics file
  # (all values are relative to the sample interval)
  #  sample_interval ... the sample interval (in seconds)
  #  num_fintrans ... financial transactions emitted
  #  tp_fintrans ... throughput of financial transactions (in thousands/second)
  #  num_bytes ... number of bytes emitted (in MB)
  #  tp_bytes ... throughput of bytes (in kB/sec)
  logging.info('sample_interval\tnum_fintrans\ttp_fintrans\tnum_bytes\ttp_bytes')
  while True:
    (fintran, fintransize) = create_fintran()
    send_fintran(out_socket, fintran)
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
  run_gess()
