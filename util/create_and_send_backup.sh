#!/usr/bin/env bash
set -e
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
source ${SCRIPTPATH}/create_db_backup.sh
source ${SCRIPTPATH}/send_db_backup.sh
