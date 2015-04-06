#!/bin/bash - 
#===============================================================================
#          FILE: drop-analytics-data.sh
#         USAGE: ./drop-analytics-data.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 11/19/2014 05:51:34 PM IST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ $# -lt 1 ];then
	echo "Usage: $0 <mysql_root_passwd>"
	exit 1
fi

echo "This will remove all data from the DWH [analytics] DBs and cannot be reverted.
Are you sure you want to continue? [N/y]"
read ANS
if [ "$ANS" !='y' ];then
	echo "Exiting. Rerun and select lower case 'y' to continue"
	exit 2
fi
PASSWD=$1
for i in `mysql -N -p$PASSWD kalturadw_bisources -e "show tables"`;do mysql -p$PASSWD kalturadw_bisources -e "drop table $i";done
for i in `mysql -N -p$PASSWD kalturadw -e "show tables"`;do mysql -p$PASSWD kalturadw -e "drop table $i";done
for i in `mysql -N -p$PASSWD kalturadw_ds -e "show tables"`;do mysql -p$PASSWD kalturadw_ds -e "drop table $i";done
for i in `mysql -N -p$PASSWD kalturalog -e "show tables"`;do mysql -p$PASSWD kalturalog -e "drop table $i";done
for i in `mysql -p$PASSWD -e "Show procedure status" |grep kalturadw|awk -F " " '{print $2}'`;do mysql kalturadw -p$PASSWD -e "drop procedure $i;";done
for i in `mysql -p$PASSWD -e "Show procedure status" |grep kalturadw_ds|awk -F " " '{print $2}'`;do mysql kalturadw_ds -p$PASSWD -e "drop procedure $i;";done

