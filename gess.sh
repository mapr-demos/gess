#!/bin/bash -

################################################################################
# 
# This is the script that allows you to start or stop gess.
#
# Usage: ./gess.sh start | stop | status
#
#

GESS_LOG=gess.tsv
GESS_PID=gess.pid

function usage() {
	printf "Usage: %s start | stop | status\n" $0
}

function start_gess() {
	nohup python scripts/gess-main.py &> $1 &
	echo $! > $GESS_PID
}

function stop_gess() {
	
	# try to find the PID of gess process and kill it
	if [ -f $GESS_PID ]; then
		if kill -0 `cat $GESS_PID` > /dev/null 2>&1; then
			echo 'Shutting down gess ...'
			kill `cat $GESS_PID`
			rm $GESS_PID
		fi
	fi
	
	# ... as well as clean up the nohup stuff
	if [ -f nohup.out ]; then
		rm nohup.out
	fi
}

function is_gess_running() {
  case `uname` in
          Linux|AIX) PS_ARGS='-ewwo pid,args'   ;;
          SunOS)     PS_ARGS='-eo pid,args'     ;;
          *BSD)      PS_ARGS='axwwo pid,args'   ;;
          Darwin)    PS_ARGS='Awwo pid,command' ;;
  esac

  if ps $PS_ARGS | grep -q '[p]ython scripts/gess-main.py' ; then
          echo 'gess is running, see also log file:' $GESS_LOG
  else
          echo 'gess is currently not running.'
  fi
}

# main script
case $1 in
 start )  start_gess $GESS_LOG ;;
 stop )   stop_gess ;;
 status ) is_gess_running ;;
 * )      usage ; exit 1 ; ;;
esac