#!/usr/bin/bash -e
#===============================================================================
#          FILE: kaltura-dwh-config.sh
#         USAGE: ./kaltura-dwh-config.sh 
#   DESCRIPTION: configure the server as a DWH node. 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:25:54 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-dwh;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-dwh is not installed.${NORMAL}"
	exit 0 
fi
if [ ! -r $BASE_DIR/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$1"
else
	echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm $BASE_DIR/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "${BRIGHT_RED}Could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi
. $RC_FILE
trap - ERR
TABLES=`echo "show tables" | mysql -h$DWH_HOST -u$SUPER_USER -p$SUPER_USER_PASSWD -P$DWH_PORT kalturadw 2> /dev/null`
if [ -z "$TABLES" ];then 
	echo -e "${CYAN}Deploying analytics warehouse DB, please be patient as this may take a while...
Output is logged to $BASE_DIR/dwh/logs/dwh_setup.log.${NORMAL}
"
	trap 'my_trap_handler "${LINENO}" $?' ERR
	# Define required dates
	FDAYCM=$(date '+%Y%m%d' -d "-$((10#`date +%d`-1)) days")
	SDAYCM=$(date '+%Y%m%d' -d "-$((10#$(date +%d)-2)) days")
	LDAYLM=$(date '+%Y%m%d' -d "-$(date +%d) days")
	LASTMO=$(date '+%Y%m' -d "-$(date +%d) days")
	
	# Replace various old dates to avoid issues with partitions
	olddates=(20130831 201308 20130901 20130902 20131231 201312 20140101 201406 20140701 201510 20151101)

        newdates=($LDAYLM $LASTMO $FDAYCM $SDAYCM $LDAYLM $LASTMO $FDAYCM $LASTMO $FDAYCM $LASTMO $FDAYCM)
	
	for ((i=0;i<${#olddates[@]};++i)); do
		FILES=`grep -rl "${olddates[i]}" $BASE_DIR/dwh/ddl/` || true
		if [ -n "$FILES" ]; then
            		sed -i  "s/${olddates[i]}/${newdates[i]}/g" $FILES
		fi
	done

	$BASE_DIR/dwh/setup/dwh_setup.sh -u$SUPER_USER -k $BASE_DIR/pentaho/pdi/ -d$BASE_DIR/dwh -h$DWH_HOST -P$DWH_PORT -p$SUPER_USER_PASSWD | tee $BASE_DIR/dwh/logs/dwh_setup.log
else
cat << EOF
The Kaltura DWH DB seems to already be installed.
DB creation will be skipped.
EOF
fi
chown -R $OS_KALTURA_USER $BASE_DIR/pentaho/pdi $BASE_DIR/dwh/logs
#sed  "s#\(@DWH_DIR@\)#\1 -k $BASE_DIR/pentaho/pdi/kitchen.sh#g" $APP_DIR/configurations/cron/dwh.template >$APP_DIR/configurations/cron/dwh
sed -i -e "s#@DWH_DIR@#$BASE_DIR/dwh#g" -e "s#@APP_DIR@#$APP_DIR#g" -e "s#@EVENTS_FETCH_METHOD@#local#g" -e "s#@LOG_DIR@#$LOG_DIR#g" $APP_DIR/configurations/cron/dwh
ln -sf $APP_DIR/configurations/cron/dwh /etc/cron.d/kaltura-dwh
# Alas, we only work well with Sun's Java so, first lets find the latest version we have for it [this package is included in Kaltura's repo, as taken from Oracle's site
LATEST_JAVA=`ls -d /usr/java/jre* 2>/dev/null|tail -1` 
if [ -n "$LATEST_JAVA" ];then
	alternatives --install /usr/bin/java java $LATEST_JAVA/bin/java  20000
fi
echo -e "${CYAN}DWH configured.${NORMAL}"
