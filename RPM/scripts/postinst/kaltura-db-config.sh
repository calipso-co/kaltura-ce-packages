#!/usr/bin/bash -
#===============================================================================
#          FILE: kaltura-db-config.sh
#         USAGE: ./kaltura-db-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/09/14 04:57:40 EST
#      REVISION:  ---
#===============================================================================
#set -o nounset                              # Treat unset variables as an error

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if [ "$#" -lt 5 ];then
	echo -e "${BRIGHT_RED}Usage: $0 <mysql-operational-hostname> <mysql-analytics-hostname> <mysql-super-user> <mysql-super-user-passwd> <mysql-port> [upgrade]${NORMAL}"
	exit 1
fi

RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi
. $RC_FILE
DB_ACTIONS_RC=`dirname $0`/db_actions.rc
if [ ! -r "$DB_ACTIONS_RC" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $DB_ACTIONS_RC so, exiting..${NORMAL}"
	exit 3
fi
. $DB_ACTIONS_RC
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $KALTURA_FUNCTIONS_RC so, exiting..${NORMAL}"
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
trap 'my_trap_handler "${LINENO}" $?' ERR

MYSQL_OP_HOST=$1
MYSQL_DWH_HOST=$2
MYSQL_SUPER_USER=$3
MYSQL_SUPER_USER_PASSWD=$4
MYSQL_PORT=$5
IS_UPGRADE=$6

if [ "$IS_UPGRADE" = 'upgrade' ];then
	echo "calling upgrade script instead."
	# the upgrade script is more complex naturally.. will include a check for schema
	# decide how far back to run alter scripts, etc.
fi
KALTURA_DB=$DB1_NAME

function setup_db
{
	DB_NAME=$1
	DB_HOST=$2

	echo "CREATE DATABASE $DB_NAME;"
	echo "CREATE DATABASE $DB_NAME;" | mysql -h$DB_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	PRIVS=${DB_NAME}_PRIVILEGES
	DB_USER=${DB_NAME}_USER
	# apply privileges:
	echo "GRANT ${!PRIVS} ON $DB_NAME.* TO '${!DB_USER}'@'%';FLUSH PRIVILEGES;" | mysql -h$DB_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	DB_SQL_FILES=${DB_NAME}_SQL_FILES
	# run table creation scripts:
	for SQL in ${!DB_SQL_FILES};do 
		mysql -h$DB_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $DB_NAME < $SQL
	done
}
# check DB connectivity:
check_mysql_strict_mode $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_OP_HOST $MYSQL_PORT
if ! check_mysql_settings $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_OP_HOST $MYSQL_PORT ;then
	if [ $MYSQL_OP_HOST = 'localhost' -o $MYSQL_OP_HOST = '127.0.0.1' ];then
		echo "Your MySQL settings are incorrect, do you wish to run $BASE_DIR/bin/kaltura-mysql-settings.sh in order to correct them? [Y/n]"
		read ANS
		if [ "$ANS" = "Y" ];then
			$BASE_DIR/bin/kaltura-mysql-settings.sh
		else
			echo -e "${BRIGHT_RED}Please adjust your MySQL configuration manually and re-run.${NORMAL}" 
			exit 8
		fi
	else
		echo "Your MySQL settings are incorrect, please set the following in your MySQL conf file [my.cnf]:
lower_case_table_names = 1
innodb_file_per_table
innodb_log_file_size=32M
open_files_limit = 20000
max_allowed_packet = 16M

Restart the MySQL daemon and re-run the config script.
"
		exit 7
	fi
fi
trap - ERR
if [ -z "$POPULATE_ONLY" ];then
	# check whether the 'kaltura' already exists:
	echo "use kaltura" | mysql -h$MYSQL_OP_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $KALTURA_DB 2> /dev/null
	if [ $? -eq 0 ];then
cat << EOF
The $KALTURA_DB DB seems to already be installed.

if you meant to perform an upgrade? run with:
# $0 $MYSQL_OP_HOST $MYSQL_DWH_HOST $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_PORT upgrade

Otherwise, do you wish to remove the existing DB [n/Y]?

EOF
		read REMOVE
		if [ $REMOVE = "Y" ];then
			`dirname $0`/kaltura-drop-db.sh
		else
			exit 5
		fi
	fi 
trap 'my_trap_handler "${LINENO}" $?' ERR

	# this is the DB creation part, we want to exit if something fails here:
	set -e

	# create users:
	USER_EXISTS=`echo "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'kaltura');" | mysql -h$MYSQL_OP_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -N`
	if [ "$USER_EXISTS" != "1" ];then
		echo "CREATE USER kaltura;"
		echo "CREATE USER kaltura@'%' IDENTIFIED BY '$DB1_PASS' ;"  | mysql -h$MYSQL_OP_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	fi
	for DB_HOST in $MYSQL_OP_HOST $MYSQL_DWH_HOST; do
		USER_EXISTS=`echo "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'etl');" | mysql -h$DB_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -N`
		if [ "$USER_EXISTS" != "1" ];then
			echo "CREATE USER etl;"
			echo "CREATE USER etl@'%' IDENTIFIED BY '$DWH_PASS' ;FLUSH PRIVILEGES;"  | mysql -h$DB_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
		fi
	done
	# create the operational DBs:
	for DB in $OP_DBS;do 
		setup_db $DB $MYSQL_OP_HOST
	done
	echo "GRANT SELECT ON kaltura.* TO 'etl'@'%';FLUSH PRIVILEGES;" | mysql -h$MYSQL_OP_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT

	for DB in $DWH_DBS;do 
		setup_db $DB $MYSQL_DWH_HOST
	done
fi
set +e

# DB schema created. Before we move onto populating, lets check MySQL and Sphinx connectivity.
echo "Checking connectivity to needed daemons..."
if ! check_connectivity $DB1_USER $DB1_PASS $DB1_HOST $DB1_PORT $SPHINX_HOST $SERVICE_URL;then
	echo -e "${BRIGHT_RED}Please check your setup and then run $0 again.${NORMAL}"
cat << EOF

Do you wish to remove the Kaltura DBs? [n/Y]
Hit 'n' to keep it for debugging purposes.

EOF
	read REMOVE
	if [ "$REMOVE" = "Y" ];then
		`dirname $0`/kaltura-drop-db.sh
	fi
	exit 6
fi

echo "Cleaning cache.."
find $APP_DIR/cache/ -type f -exec rm {} \;
rm -f $LOG_DIR/installPlugins.log $LOG_DIR/insertDefaults.log $LOG_DIR/insertPermissions.log $LOG_DIR/insertContent.log
service httpd restart
service php-fpm restart


echo -e "${CYAN}Populating DB with data.. please wait..${NORMAL}"
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/installPlugins.php being logged into $LOG_DIR/installPlugins.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/installPlugins.php >> $LOG_DIR/installPlugins.log  2>&1
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/insertDefaults.php being logged into $LOG_DIR/insertDefaults.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/insertDefaults.php $APP_DIR/deployment/base/scripts/init_data >> $LOG_DIR/insertDefaults.log  2>&1
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/insertPermissions.php being logged into $LOG_DIR/insertPermissions.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/insertPermissions.php  >> $LOG_DIR/insertPermissions.log 2>&1
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/insertContent.php being logged into $LOG_DIR/insertContent.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/insertContent.php >> $LOG_DIR/insertContent.log  2>&1
if [ $? -ne 0 ];then
cat << EOF
Failed to run:
php $APP_DIR/deployment/base/scripts/insertContent.php >> $LOG_DIR/insertContent.log  2>&1
EOF
	echo -e "${BRIGHT_RED}Please check your setup and then run $0 again.${NORMAL}"
	exit 8
fi

KMC_VERSION=`grep "^kmc_version" $BASE_DIR/app/configurations/local.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
KMCNG_VERSION=`grep "^kmcng_version" $BASE_DIR/app/configurations/local.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
if [ "$IS_SSL" = 'Y' -o "$IS_SSL" = 1 -o "$IS_SSL" = 'y' -o "$IS_SSL" = 'true' ];then
# force KMC login via HTTPs.
	php $APP_DIR/deployment/base/scripts/insertPermissions.php -d $APP_DIR/deployment/permissions/ssl/ > /dev/null 2>&1
fi

echo -e "${BRIGHT_BLUE}Generating UI confs..${NORMAL}"
php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$BASE_DIR/apps/kmcng/$KMCNG_VERSION/deploy/config.ini >> $LOG_DIR/deploy_v2.log  2>&1

#for i in $APP_DIR/deployment/updates/scripts/patches/*.sh;do
#	$i
#done
HTML5_STUDIO_VERSION=`rpm -q kaltura-html5-studio --queryformat %{version}`
if [ -r $BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini ];then
	php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini >> /dev/null
	sed -i "s@^\(studio_version\s*=\)\(.*\)@\1 $HTML5_STUDIO_VERSION@g" -i $BASE_DIR/app/configurations/local.ini
fi
HTML5LIB3_VERSION=`rpm -q kaltura-html5lib3 --queryformat %{version}`
HTML5LIB3_BASEDIR=$BASE_DIR/html5/html5lib/playkitSources/kaltura-ovp-player
PARTNER_ZERO_SECRET=`echo "select admin_secret from partner where id=0" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER  -P$DB1_PORT`
if [ -r $HTML5LIB3_BASEDIR/create_playkit_uiconf.php ];then
	php $HTML5LIB3_BASEDIR/create_playkit_uiconf.php 0 $PARTNER_ZERO_SECRET $SERVICE_URL $HTML5LIB3_VERSION
fi
BUNDLER_CONF_FILE=$BASE_DIR/playkit-js-bundle-builder/config/default.json
if [ -r $APP_DIR/configurations/local.ini -a -r $BUNDLER_CONF_FILE ];then
        SALT=`grep remote_addr_header_salt $APP_DIR/configurations/local.ini|sed 's@^remote_addr_header_salt\s*=\s*\(.*\)$@\1@g'| sed 's@"@@g'`
        sed -i "s#@APP_REMOTE_ADDR_HEADER_SALT@#$SALT#g" $BUNDLER_CONF_FILE
fi
service kaltura-playkit-bundler restart || true

find  $WEB_DIR/content/generatedUiConf -type d -exec chmod 775 {} \;

set +e


#if [ "$DB1_HOST" = `hostname` -o "$DB1_HOST" = '127.0.0.1' -o "$DB1_HOST" = 'localhost' ];then
#	if [ `rpm -qa "Percona-Server-server*"` ]; then 
#		ln -sf $BASE_DIR/app/configurations/monit/monit.avail/percona.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.mysqld.rc
#	else
#		ln -sf $BASE_DIR/app/configurations/monit/monit.avail/mysqld.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.mysqld.rc
#	fi
#	service kaltura-monit stop >> /dev/null 2>&1
#	service kaltura-monit restart
#fi
