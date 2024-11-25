%define prefix /opt/kaltura
%define kaltura_user kaltura
%define codename Orion 
Summary: Kaltura Open Source Video Platform - Analytics 
Name: kaltura-dwh
Version: 15.1.0
Release: 4
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/dwh/archive/%{name}-%{codename}-%{version}.zip
Source1: dwh_fact_active_users.sql
URL: https://github.com/kaltura/dwh/tree/master 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base,kaltura-pentaho,jre, kaltura-postinst 
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

This package configures the Data Warehouse [DWH] analytics component. 

%prep
%setup -qn dwh-%{codename}-%{version} 

%build

%install
# for Apache access logs.
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/logs
cp -r %{_builddir}/dwh-%{codename}-%{version} $RPM_BUILD_ROOT%{prefix}/dwh

# See https://github.com/kaltura/dwh/blob/Orion-15.1.0/ddl/dw/facts/dwh_fact_active_users.sql#L3
# This drops the critical dwh_fact_plays table, instead of dwh_fact_active_users
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/dwh/ddl/dw/facts/dwh_fact_active_users.sql
find  $RPM_BUILD_ROOT%{prefix}/dwh/ -name "*.sh" -type f -exec chmod +x {} \;

%clean
rm -rf %{buildroot}

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

%post
if [ "$1" = 0 ];then
	%{prefix}/bin/kaltura-dwh-config.sh
fi

%preun
if [ "$1" = 0 ] ; then
	rm -f %{_sysconfdir}/cron.d/kaltura-dwh
fi

%files
%dir %{prefix}/web/logs
%defattr(-, %{kaltura_user},root 0755)
%{prefix}/dwh


%changelog
* Mon Nov 25 2024 jesse@packman.io <Jesse Portnoy> - 15.1.0-4
- Override typo in https://github.com/kaltura/dwh/blob/Orion-15.1.0/ddl/dw/facts/dwh_fact_active_users.sql#L3

* Tue Jan 5 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 15.1.0-2
- 2021 bug (https://github.com/kaltura/dwh/commit/b0b0288063c06216ef0a2fecb68cffcfe6950c36)

* Thu Apr 4 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.18.0-1
- Since RAPT is implemented as a playlist, we need to include the value 3 when querying `entry_media_type_id`.

* Tue Jan 15 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.12.0-1
- New UserAgent.jar, used for browser detection.

* Thu Jan 7 2016 Jess Portnoy <jess.portnoy@kaltura.com> - 11.3.0-1
- Add Hercules to Iris/Jupiter migration
- Add Nginx log parsing
- Add Totals Aggregration
- Add Live Analytics

* Thu Oct 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 9.5.0-2
- Live entry aggregation ddl changes 

* Mon Aug 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 9.5.0-1
- Don't use preserved word MAX as query alias.
- Make sure that file_size is int value like in DB

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.2.0-2
%%{prefix}/bin/kaltura-dwh-config.sh does not require user interaction, if this is an upgrade just run it at %%post.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.2.0-1
- Fixes Unknown column 'invalid_login_count' in 'field list' - this field was dropped from the kaltura operational DB.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-3
- Define 'kaltura_user' in the spec.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-2
- Make kaltura owner of logs dir.
- Set exec bit on all shell scripts.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-1
- Moving to IX-9.9.0

* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-8
- Sources moved to GIT.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-6
- Plus .kettle config.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-5
- Install actual %%{prefix}/dwh dir

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.1.0-3
- Added creation of %%{prefix}/web/logs

* Mon Dec 23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package
