#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5lib.sh
#         USAGE: ./package_kaltura_html5lib.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/14/14 11:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
for i in wget ;do
	EX_PATH=`which $i 2>/dev/null`
	if [ -z "$EX_PATH" -o ! -x "$EX_PATH" ];then
		echo "Need to install $i."
		exit 2
	fi
done
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 

cd $SOURCE_PACKAGING_DIR
wget $HTML5LIB_URI -O $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz
tar zxf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz 
rm -rf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
mv `ls -rtd kaltura-mwEmbed-* | tail -1` $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
tar zcf $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz"
rpmbuild -ba $RPM_SPECS_DIR/$HTML5LIB_RPM_NAME.spec
