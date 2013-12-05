#!/bin/bash -

################################################################################
# 
# This is the script that allows you to test gess. Through utilising netcat
# (see also 'man nc'), this script listens on the gess test port 6900 for
# incoming UDP packages and echos them. In order to work, you first need to
# execute gess.sh
# 
#
# Usage: ./dummy_gess_sink.sh
#
#
nc -v -u -l 6900 | tee dummy_gess_sink.log