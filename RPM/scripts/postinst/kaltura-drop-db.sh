#!/bin/bash -e 
#===============================================================================
#          FILE: kaltura-drop-db.sh
#         USAGE: ./kaltura-drop-db.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/24/14 12:50:13 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ ! -r /opt/kaltura/bin/db_actions.rc ];then
	echo "I can't drop without /opt/kaltura/bin/db_actions.rc"
	exit 1
fi
. /opt/kaltura/bin/db_actions.rc
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 1 
fi
. $RC_FILE
echo "This will drop the following DBs: 
$DBS 
and remove users:
$DB_USERS
on $DB1_HOST

Are you absolutely certain you want this? Type yes
"
read AN
if [ "$AN" != 'yes' ];then
	echo "Exiting. You must type the word 'yes'."
	exit 1
fi
echo "root DB passwd:"
read -s DBPASSWD
for i in $DBS;do
	echo "Removing $i" 
	echo "drop database $i" | mysql -h$DB1_HOST -p$DBPASSWD ;
done
for i in $DB_USERS;do echo "drop user $i" | mysql -h$DB1_HOST -p$DBPASSWD ;done


