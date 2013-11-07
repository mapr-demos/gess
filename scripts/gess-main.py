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
  FORMAT = '%(asctime)-0s %(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')


# creates a single financial transaction
def create_fintran():
  fintran = {
    'timestamp' : str(datetime.datetime.now()),
    'transaction_id' : random.randint(1, 100000),
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
  overall_fintransize = 0
  while True:
    (fintran, fintransize) = create_fintran()
    send_fintran(out_socket, fintran)
    num_fintrans += 1
    overall_fintransize += fintransize
  
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time
    
    if diff_time.seconds > (SAMPLE_INTERVAL - 1):
      fintransps = (num_fintrans/1000) / diff_time.seconds
      fintranssizeps = (overall_fintransize/1024) / diff_time.seconds
      logging.info('Sample interval: %ssec' %diff_time.seconds)
      logging.info('Transactions emitted in sample interval: %sk' %(num_fintrans/1000))
      logging.info('Transaction-throughput in sample interval: %sk/sec' %fintransps)
      logging.info('Bytes emitted in sample interval: %sMB' %(overall_fintransize/1024/1024))
      logging.info('Bytes-throughput in sample interval: %skB/sec' %fintranssizeps)
      
      start_time = datetime.datetime.now()
      num_fintrans = 0
      overall_fintransize = 0
      


################################################################################
## Main script

if __name__ == '__main__':
  run_gess()
