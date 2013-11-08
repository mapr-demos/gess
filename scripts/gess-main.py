#!/usr/bin/python

""" 
  The main script of gess, the generator for synthetic streams 
  of financial transactions.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2013-11-07
@status: init
"""
import logging

from fintrans import FinTransSource

DEBUG = False
SAMPLE_INTERVAL = 5   # defines the sampling interval (in seconds) for 
                      # reporting runtime statistics 


if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT)


################################################################################
## Main script

if __name__ == '__main__':
  fns = FinTransSource()
  fns.run()
