%define prefix /opt/kaltura
%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define apache_user	apache
%define apache_group	apache
Summary: Kaltura Open Source Video Platform - frontend server 
Name: kaltura-front
Version: 9.14.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
#Source0: kaltura.ssl.conf.template 
#Source1: kaltura-kmc.conf
#Source2: kaltura-admin-console.conf
Source3: zz-%{name}.ini 

URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: mediainfo, httpd, php, curl, kaltura-base, kaltura-ffmpeg, ImageMagick, memcached, php-pecl-memcached, php-mysql, php-pecl-apc, php-mcrypt, kaltura-segmenter, mod_ssl
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
BuildArch: noarch

%description
Kaltura is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Kaltura platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Kaltura improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Kaltura offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.kaltura.com, http://www.kaltura.org and http://www.html5video.org.


The Kaltura platform enables video management, publishing, syndication and monetization, 
as well as providing a robust framework for managing rich-media applications, 
and developing a variety of online workflows for video. 

This package sets up a server as a front node.

#%prep
#%setup -q

%pre
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce >> /dev/null 2>&1; then
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi
%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/app/configurations/apache
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/php.d
cp %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/php.d
sed 's#@WEB_DIR@#%{prefix}/web#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/zz-%{name}.ini

%post
#sed 's#@WEB_DIR@#%{prefix}/web#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/*.conf 
#sed 's#@LOG_DIR@#%{prefix}/log#'  -i $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/*.conf
#sed 's#@APP_DIR@#%{prefix}/app#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/*.conf

chown -R %{kaltura_user}:%{apache_group} %{prefix}/log 
chown -R %{kaltura_user}:%{apache_group} %{prefix}/tmp 
chown -R %{kaltura_user}:%{apache_group} %{prefix}/app/cache 
chmod -R 775 %{prefix}/log %{prefix}/tmp %{prefix}/app/cache %{prefix}/web
if [ "$1" = 1 ];then
	/sbin/chkconfig --add httpd
	/sbin/chkconfig httpd on
	/sbin/chkconfig --add memcached 
	/sbin/chkconfig memcached on
fi
service httpd restart

if [ "$1" = 1 ];then
echo "#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi
%preun
if [ "$1" = 0 ] ; then
#	rm %{prefix}/app/configurations/monit.d/httpd.rc || true#
	rm -f %{_sysconfdir}/cron.d/kaltura-api
	rm -f %{_sysconfdir}/cron.d/kaltura-cleanup
	rm -f %{_sysconfdir}/logrotate.d/kaltura_api
	rm -f %{_sysconfdir}/logrotate.d/kaltura_apache
fi

%clean
rm -rf %{buildroot}

%files
%config %{_sysconfdir}/php.d/zz-%{name}.ini

%changelog
* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-1
- Ver Bounce to 9.13.0

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-1
- Ver Bounce to 9.12.0

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-1
- New tag.

* Tue Feb 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-3
- monit is handled in postinst scripts now.

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-2
- Start httpd and memcached at init.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-1
- Moving to IX-9.9.0

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-9
- Corrected permissions.

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-8
- Add dep on mod_ssl.

* Thu Jan 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-7
- We will not bring a done config for front Apache. 
  Instead, during post we will generate from template and then SYMLINK to /etc/httpd/conf.d.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-6
- Use the monit scandir mechanism.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> 9.7.0-5
- Output post message only on first install.
- sed corrected.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-4
- Added define for apache_group.
- Monit conf path corrected.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- Added dep on kaltura-segmenter.

* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-2
- Added chown and chmod on log dir.

* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package

