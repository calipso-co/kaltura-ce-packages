#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-batch-config.sh
#         USAGE: ./kaltura-batch-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo -e $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-batch;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-batch is not installed.${NORMAL}"
	exit 0 
fi
PHP_MINOR_VER=`php -r 'echo PHP_MINOR_VERSION;'`
if [ "$PHP_MINOR_VER" -gt 3 ];then
        if ! rpm -q php-pecl-zendopcache >/dev/null;then
                yum -y install php-pecl-zendopcache
        fi
fi

if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$ANSFILE"
else
	echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi
trap 'my_trap_handler "${LINENO}" $?' ERR
CONFIG_DIR=/opt/kaltura/app/configurations
if [ -r $CONFIG_DIR/system.ini ];then
	. $CONFIG_DIR/system.ini
else
	echo -e "${BRIGHT_RED}ERROR: Missing $CONFIG_DIR/system.ini. Exiting..${NORMAL}"
	exit 1
fi

BATCH_SCHED_CONF=$APP_DIR/configurations/batch/scheduler.conf
BATCH_MAIN_CONFS="$APP_DIR/configurations/batch/batch.ini $APP_DIR/configurations/batchBase.ini"

# if we couldn't access the DB to retrieve the secret, assume the post install has not finished yet.
BATCH_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-1"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME -P$DB1_PORT`
if [ -z "$BATCH_PARTNER_ADMIN_SECRET" ];then
	echo -e "${BRIGHT_RED}ERROR: could not retrieve partner.admin_secret for id -1. It probably means you did not yet run $APP_DIR/kaltura-base-config.sh yet. Please do.${NORMAL}" 
	exit 2
fi

BATCH_HOSTNAME=`hostname`
sed -i "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#" -i $BATCH_MAIN_CONFS
sed -i "s#@INSTALLED_HOSNAME@#$BATCH_HOSTNAME#" -i $BATCH_MAIN_CONFS
# if this host already has a configured_id ID, in the scheduler table, use that:
BATCH_SCHEDULER_ID=`echo "select configured_id from scheduler where host='$BATCH_HOSTNAME' order by updated_at desc limit 1"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME -P$DB1_PORT`
# otherwise, let's generate a random one:
if [ -z "$BATCH_SCHEDULER_ID" ];then
    BATCH_SCHEDULER_ID=`< /dev/urandom tr -dc 0-9 | head -c5`
fi
sed "s#@BATCH_SCHEDULER_ID@#$BATCH_SCHEDULER_ID#"  -i $BATCH_MAIN_CONFS


# logrotate:
ln -sf $APP_DIR/configurations/logrotate/kaltura_batch /etc/logrotate.d/ 
ln -sf $APP_DIR/configurations/logrotate/kaltura_apache /etc/logrotate.d/
ln -sf $APP_DIR/configurations/logrotate/kaltura_apps /etc/logrotate.d/

# setting KALTURA_BATCH_SKIP_WEBSERVER to anything but false||0 will configure Apache on the batch node
# KALTURA_BATCH_SKIP_WEBSERVER=true can be used in the event you want the batch daemon to use a remote Kaltura endpoint/service URL
# and thus do not wish for a local Apache instance to run on the node
if [ -z "$KALTURA_BATCH_SKIP_WEBSERVER" -o "$KALTURA_BATCH_SKIP_WEBSERVER" = "false" -o "$KALTURA_BATCH_SKIP_WEBSERVER" = 0 ];then
	if [ "$PROTOCOL" = "https" -o "$IS_SSL" = 'Y' -o "$IS_SSL" = 1 -o "$IS_SSL" = 'y' -o "$IS_SSL" = 'true' ]; then
                ln -sf $APP_DIR/configurations/apache/kaltura.ssl.conf /etc/httpd/conf.d/zzzkaltura.ssl.conf
        else
                ln -sf $APP_DIR/configurations/apache/kaltura.conf /etc/httpd/conf.d/zzzkaltura.conf
        fi
        chkconfig httpd on
        if service httpd status >/dev/null 2>&1;then
                service httpd reload
        else
                service httpd start
        fi
        ln -sf $BASE_DIR/app/configurations/monit/monit.avail/httpd.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.httpd.rc
fi


mkdir -p $LOG_DIR/batch
find $APP_DIR/cache/ -type f -exec rm {} \;
find $BASE_DIR/log -type d -exec chmod 775 {} \;
find $BASE_DIR/log -type f -exec chmod 664 {} \;
chown -R kaltura.apache $BASE_DIR/app/cache/ $BASE_DIR/log

chkconfig memcached on
service memcached restart

/etc/init.d/kaltura-batch restart >/dev/null 2>&1
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/batch.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.batch.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/memcached.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.memcached.rc
service kaltura-monit stop >> /dev/null 2>&1
service kaltura-monit start
