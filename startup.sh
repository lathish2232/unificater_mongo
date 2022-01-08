#!/bin/sh

# ************************************************
# Author: sundar <sundarcse1216@gmail.com>
# Description: Unificater REST Service Startup Script
# ProcessName: Unificater REST Service
# Version : 1.0
# Relased Date : 09-01-2021
# ***********************************************

#ln -s <src_directory_path> <filename>

#git push -d origin $(git tag -l "v1.*")
#set +x # -x Enable debug mode; +x disable debug mode

APP_NAME="Unificater REST Service"
UNIQUE_NAME="python3 manage.py runserver"
ENV="$2"

if [ "$ENV" = "qa" ]; then
  HOST_PORT='0.0.0.0:7198'
  export UNIFY_REGION='qa'
#  export DEBUG=False
elif [ "$ENV" = "prod" ]; then
  HOST_PORT='0.0.0.0:7197'
  export UNIFY_REGION='prod'
#  export DEBUG=False
else
  HOST_PORT='0.0.0.0:8000'
  export UNIFY_REGION='dev'
#  export DEBUG=False
fi
export DEBUG=False
export UNIFY_LISTERN=$HOST_PORT
cp .env.example .env

echo "\n\tWelcome to "$APP_NAME"\n*****************************************************\n"

start() {

  PID=$(ps -ef | grep "python3 manage.py runserver $HOST_PORT" | grep -v grep | awk '{print $2}' | wc -l)
  if [ $PID -eq 0 ]; then
    $UNIQUE_NAME $HOST_PORT &
    echo $APP_NAME" started successfully\n"
  else
    echo $APP_NAME" is already running\n"
  fi

}

stop() {

  #PID=$(ps -aux | grep "python3 manage.py runserver $HOST_PORT" | awk '{print $2}' | wc -l)
  PID=$(ps -ef | grep "python3 manage.py runserver $HOST_PORT" | grep -v grep | awk '{print $2}' | wc -l)
  if [ $PID -eq 1 ]; then
    echo $APP_NAME" is already stopped\n"
  else
    PID=$(ps -ef | grep "python3 manage.py runserver $HOST_PORT" | grep -v grep | awk '{print $2}')
    for i in ${PID}; do
      kill -9 $i
    done
    sleep 5
    echo $APP_NAME" stopped successfully\n"
  fi

}

restart() {

  stop
  sleep 10
  start

}

status() {

  PID=$(ps -ef | grep "python3 manage.py runserver $HOST_PORT" | grep -v grep | awk '{print $2}' | wc -l)
  if [ $PID -eq 0 ]; then
    echo $APP_NAME" is stopped\n"
  else
    echo $APP_NAME" is running\n"
  fi

}

case $1 in

start)

  start
  exit 0
  ;;

stop)

  stop
  exit 0
  ;;

restart)

  restart
  exit 0
  ;;

status)

  status
  exit 0
  ;;

--help)

  echo $0 "start [ENV] = to start "$APP_NAME"\n"
  echo $0 "stop [ENV] = to stop "$APP_NAME"\n"
  echo $0 "restart [ENV] = to restart "$APP_NAME"\n"
  echo $0 "status [ENV] = to see the status of "$APP_NAME"\n"
  echo "\t ENV = dev, qa, prod; default is dev\n"
  echo "\n*****************************************************\n"
  ;;

*)

  echo "Parameter should be [start | stop | restart | status]"
  echo $0 "--help = to see the help\n"
  exit 1
  ;;

esac
