#!/bin/bash - 
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
if [ "$#" -lt 4 ];then
	echo -e "${BRIGHT_RED}Usage: $0 <mysql-hostname> <mysql-super-user> <mysql-super-user-passwd> <mysql-port> [upgrade]${NORMAL}"
	exit 1
fi


MYSQL_HOST=$1
MYSQL_SUPER_USER=$2
MYSQL_SUPER_USER_PASSWD=$3
MYSQL_PORT=$4
IS_UPGRADE=$5

#Notice for a non installation
NO_REMOVAL_NOTICE="This installation has been stopped. In order to try again please tend to stop reason and run '${CYAN}kaltura-config-all.sh${NORMAL}' or '${CYAN}kaltura-db-config.sh${NORMAL}' depending on the initial command which has been used.";

#USed for both connection check, and record check
EMPTY_HOSTS_RECORDS=`mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -N -e "use mysql; select host,user from mysql.user where user=''"`
if [ $? -ne 0 ]; then
    echo -e "${BRIGH_RED}Problem connecting to DB. Please verify that the super user password is correct.${NORMAL}";
    exit 1;
else
    echo "Initial DB access check passed.";
fi

# DB emnpty user fix
EMPTY_HOSTS_COUNT=`echo $EMPTY_HOSTS_RECORDS | wc -w;` # counting how many words were returned.
if [ $EMPTY_HOSTS_COUNT -ne 0 ]; then 
    echo -e "
    \rRecords found in ${CYAN}mysql.user${NORMAL} table contain 'host' values with no 'user' value. These records may interfere with the planned installation process.
    \rWe would like to remove these records in order to allow proper user authentication.\e[31m\e[1m"; 
    
    #Run for showing well formatted results for the user
    mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -e "use mysql; select host,user from mysql.user where user=''"
    echo -e "${NORMAL}
    \r* 'YES' - If you are certain that you wish to proeed with the record removal and installation
    \r* 'NO' - Stop the installation, with no DB changes made. If you wish to tend to the matter manually this installation can be performed again later.
    \r* 'TRY' - Attempt to proceed with the installation without user removal\n";
    read -p ">" USER_CHOICE;

    # Input verification
    while [ $USER_CHOICE != 'YES' ] && [ $USER_CHOICE != 'NO' ] && [ $USER_CHOICE != 'TRY' ]
    do
        echo -e "Please choose either: \n'YES' - remove users and proeed with the installation, \n'NO' - Stop the installation or \n'GO' in order to try without user removal:\n";
        read -p ">" USER_CHOICE;
    done
    
    #1st menu choice
    case "$USER_CHOICE" in 
        YES)
            echo -e "Are you sure you want to delete the mentioned records?. This action cannot be undone.";
            read -p "Please choose either 'YES' or 'NO':" USER_CHOICE;
            
            # Input verification
            while [ $USER_CHOICE != 'YES' ] && [ $USER_CHOICE != 'NO' ]
            do
                echo -e "Please choose either 'YES' or 'NO':"
                read -p ">" USER_CHOICE;
            done

            #2nd level menu choice
            case "$USER_CHOICE" in
                YES)
                    echo -n "Deleting records from the DB...";
                    echo "delete from mysql.user where user=''" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT;
                    echo "Done"
                    ;;
                NO)
                    echo -e "Exiting with no changes made.\n$NO_REMOVAL_NOTICE";
                    exit 0;
                    ;;              
            esac
            ;;
        NO)
            echo -e "Exiting with no changes made.\n$NO_REMOVAL_NOTICE";
            ;;
        TRY)
            echo "proceeding without user removal.";
            ;;  
    esac    
fi
#DB fix change end 

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
trap 'my_trap_handler "${LINENO}" ${$?}' ERR
send_install_becon `basename $0` $ZONE install_start 0 



if [ "$IS_UPGRADE" = 'upgrade' ];then
	echo "calling upgrade script instead."
	# the upgrade script is more complex naturally.. will include a check for schema
	# decide how far back to run alter scripts, etc.
fi
KALTURA_DB=$DB1_NAME

# check DB connectivity:
echo -e "${CYAN}Checking MySQL version..${NORMAL}"
MYVER=`echo "select version();" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -N`
MYMAJVER=`echo $MYVER| awk -F "." '{print $1}'`
MYMINORVER=`echo $MYVER| awk -F "." '{print $2}'`

if [ "$MYMAJVER" -ne 5 ];then
	echo -e "${BRIGHT_RED}Your version of MySQL is not compatible with Kaltura at the moment. 
Please install and configure MySQL 5.1 according to the instructions on the Kaltura install manual before proceeding with the Kaltura installation.${NORMAL}"
	exit 1
else
	echo -e "${CYAN}Ver $MYVER found compatible${NORMAL}"
fi

if [ $? -ne 0 ];then
cat << EOF
Failed to run:
# mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT."
Check your settings."
EOF
	exit 4
fi
if ! check_mysql_settings $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_HOST $MYSQL_PORT ;then
	if [ $MYSQL_HOST = 'localhost' -o $MYSQL_HOST = '127.0.0.1' ];then
		echo "Your MySQL settings are incorrect, do you wish to run $BASE_DIR/bin/kaltura-mysql-settings.sh in order to correct them? [Y/n]"
		read ANS
		if [ "$ANS" = "Y" ];then
			$BASE_DIR/bin/kaltura-mysql-settings.sh
		else
			echo "Please adjust your settings manually and re-run." 
			exit 8
		fi
	else
		exit 7
	fi
fi
trap - ERR
if [ -z "$POPULATE_ONLY" ];then
	# check whether the 'kaltura' already exists:
	echo "use kaltura" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $KALTURA_DB 2> /dev/null
	if [ $? -eq 0 ];then
cat << EOF
The $KALTURA_DB DB seems to already be installed.

if you meant to perform an upgrade? run with:
# $0 $MYSQL_HOST $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_PORT upgrade

Otherwise, do you wish to remove the existing DB [n/Y]?

EOF
		read REMOVE
		if [ $REMOVE = "Y" ];then
			`dirname $0`/kaltura-drop-db.sh
		else
			exit 5
		fi
	fi 
trap 'my_trap_handler "${LINENO}" ${$?}' ERR

	# this is the DB creation part, we want to exit if something fails here:
	set -e

	# create users:
	#for DB_USER in $DB_USERS;do
		echo "CREATE USER kaltura;"
		echo "CREATE USER kaltura IDENTIFIED BY '$DB1_PASS' ;"  | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
		echo "CREATE USER etl;"
		echo "CREATE USER etl IDENTIFIED BY '$DWH_PASS' ;"  | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	#done
	# create the DBs:
	for DB in $DBS;do 
		echo "CREATE DATABASE $DB;"
		echo "CREATE DATABASE $DB;" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
		PRIVS=${DB}_PRIVILEGES
		DB_USER=${DB}_USER
		# apply privileges:
		echo "GRANT ${!PRIVS} ON $DB.* TO '${!DB_USER}'@'%';FLUSH PRIVILEGES;" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
		DB_SQL_FILES=${DB}_SQL_FILES
		# run table creation scripts:
		for SQL in ${!DB_SQL_FILES};do 
			mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $DB < $SQL
		done
	done
	echo "GRANT SELECT ON kaltura.* TO 'etl'@'%';FLUSH PRIVILEGES;" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT

	# DB schema created. Before we move onto populating, lets check MySQL and Sphinx connectivity.
fi
set +e

echo "Checking connectivity to needed daemons..."
if ! check_connectivity $DB1_USER $DB1_PASS $DB1_HOST $DB1_PORT $SPHINX_HOST $SERVICE_URL;then
	echo -e "${BRIGHT_RED}Please check your setup and then run $0 again.${NORMAL}"
cat << EOF

Do you wish to remove the existing DB or keep for debugging puropses [n/Y]?

EOF
	read REMOVE
	if [ $REMOVE = "Y" ];then
		`dirname $0`/kaltura-drop-db.sh
	fi
	exit 6
fi

echo "Cleaning cache.."
rm -rf $APP_DIR/cache/*
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

if [ -n "$IS_SSL" ];then
# force KMC login via HTTPs.
	php $APP_DIR/deployment/base/scripts/insertPermissions.php -d $APP_DIR/deployment/permissions/ssl/ > /dev/null 2>&1
fi

KMC_VERSION=`grep "^kmc_version" /opt/kaltura/app/configurations/local.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
echo -e "${BRIGHT_BLUE}Generating UI confs..${NORMAL}"
php $APP_DIR/deployment/uiconf/deploy_v2.php --ini=$WEB_DIR/flash/kmc/$KMC_VERSION/config.ini >> $LOG_DIR/deploy_v2.log  2>&1
for i in $APP_DIR/deployment/updates/scripts/patches/*.sh;do
	$i
done
find  $WEB_DIR/content/generatedUiConf -type d -exec chmod 775 {} \;

set +e
rm -rf $BASE_DIR/cache/*
rm -f $APP_DIR/log/kaltura-*.log



if [ "$DB1_HOST" = `hostname` -o "$DB1_HOST" = '127.0.0.1' -o "$DB1_HOST" = 'localhost' ];then
	ln -sf $BASE_DIR/app/configurations/monit/monit.avail/mysqld.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.mysqld.rc
	/etc/init.d/kaltura-monit stop >> /dev/null 2>&1
	/etc/init.d/kaltura-monit restart
fi
send_install_becon `basename $0` $ZONE install_success 0 
