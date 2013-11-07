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
GESS_UDP_PORT = 6900

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
  return fintran

# sends a single financial transaction via UDP
def send_fintran(out_socket, fintran):
  out_socket.sendto(str(fintran) + '\n', (GESS_IP, GESS_UDP_PORT))
  logging.debug('Sent financial transaction: %s' %fintran)
    
def run_gess():
  out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
  while True:
    fintran = create_fintran()
    send_fintran(out_socket, fintran)


################################################################################
## Main script

if __name__ == '__main__':
  run_gess()
