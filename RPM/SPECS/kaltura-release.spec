%define baseurl installrepo.kaltura.org
%define testpath releases/nightly/RPMS
%define prefix /opt/kaltura 
Summary: Kaltura Server release file and package configuration
Name: kaltura-release
Version: 19.4.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch


%description
Kaltura Server release file. This package contains yum 
configuration for the Kaltura RPM Repository, as well as the public
GPG keys used to sign them.




%build
%{__cat} <<EOF >kaltura.repo
# URL: http://kaltura.org/
[Kaltura]
name = Kaltura Server
baseurl = http://%{baseurl}/releases/latest/\$releasever/RPMS/\$basearch/
gpgkey = http://%{baseurl}/releases/RPM-GPG-KEY-kaltura-curr
gpgcheck = 1 
enabled = 1

[Kaltura-noarch]
name = Kaltura Server arch independent
baseurl = http://%{baseurl}/releases/latest/\$releasever/RPMS/noarch
gpgkey = http://%{baseurl}/releases/RPM-GPG-KEY-kaltura-curr
gpgcheck = 1
enabled = 1
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 kaltura.repo %{buildroot}%{_sysconfdir}/yum.repos.d/kaltura.repo

%clean
%{__rm} -rf %{buildroot}

%post
if [ "$1" = 2 ];then
	if [ -r  %{prefix}/bin/kaltura-functions.rc ];then
		. %{prefix}/bin/kaltura-functions.rc
		if [ -r /etc/sysconfig/clock ];then
			. /etc/sysconfig/clock
		else 
			ZONE='unknown'
	  	fi
		send_install_becon %{name}-%{version}-%{release} $ZONE install_upgrade
	fi
fi
exit 0

%files
%dir %{_sysconfdir}/yum.repos.d/
%config %{_sysconfdir}/yum.repos.d/kaltura.repo

%changelog
* Thu Mar 9 2023 jess.portnoy@kaltura.com <Jess Portnoy> - 19.4.0-1
- Ver Bounce to 19.4.0

* Mon Feb 27 2023 jess.portnoy@kaltura.com <Jess Portnoy> - 19.3.0-1
- Ver Bounce to 19.3.0

* Mon Jan 30 2023 jess.portnoy@kaltura.com <Jess Portnoy> - 19.2.0-1
- Ver Bounce to 19.2.0

* Mon Jan 30 2023 jess.portnoy@kaltura.com <Jess Portnoy> - 19.1.0-1
- Ver Bounce to 19.1.0

* Fri Jan 13 2023 jess.portnoy@kaltura.com <Jess Portnoy> - 19.0.0-1
- Ver Bounce to 19.0.0

* Wed Dec 28 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.20.0-1
- Ver Bounce to 18.20.0

* Mon Nov 28 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.19.0-1
- Ver Bounce to 18.19.0

* Thu Nov 10 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.18.0-1
- Ver Bounce to 18.18.0

* Mon Oct 24 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.17.0-1
- Ver Bounce to 18.17.0

* Mon Oct 3 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.16.0-1
- Ver Bounce to 18.16.0

* Tue Sep 20 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.15.0-1
- Ver Bounce to 18.15.0

* Wed Sep 7 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.14.0-1
- Ver Bounce to 18.14.0

* Mon Aug 22 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.13.0-1
- Ver Bounce to 18.13.0

* Mon Aug 8 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.12.0-1
- Ver Bounce to 18.12.0

* Wed Jul 27 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.11.0-1
- Ver Bounce to 18.11.0

* Mon Jul 18 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.10.0-1
- Ver Bounce to 18.10.0

* Thu Jun 30 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.9.0-1
- Ver Bounce to 18.9.0

* Mon Jun 27 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.8.0-1
- Ver Bounce to 18.8.0

* Fri Jun 10 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.7.0-1
- Ver Bounce to 18.7.0

* Mon May 30 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.6.0-1
- Ver Bounce to 18.6.0

* Wed May 4 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.4.0-1
- Ver Bounce to 18.4.0

* Mon Apr 25 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.3.0-1
- Ver Bounce to 18.3.0

* Tue Mar 22 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.2.0-1
- Ver Bounce to 18.2.0

* Sat Mar 12 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.1.0-1
- Ver Bounce to 18.1.0

* Wed Feb 9 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 18.0.0-1
- Ver Bounce to 18.0.0

* Thu Feb 3 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 17.20.0-1
- Ver Bounce to 17.20.0

* Mon Jan 24 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 17.19.0-1
- Ver Bounce to 17.19.0

* Fri Jan 7 2022 jess.portnoy@kaltura.com <Jess Portnoy> - 17.18.0-1
- Ver Bounce to 17.18.0

* Mon Dec 20 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.17.0-1
- Ver Bounce to 17.17.0

* Sat Dec 11 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.16.0-1
- Ver Bounce to 17.16.0

* Thu Dec 2 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.16.0-1
- Ver Bounce to 17.16.0

* Mon Nov 22 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.14.0-1
- Ver Bounce to 17.14.0

* Tue Oct 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.13.0-1
- Ver Bounce to 17.13.0

* Mon Oct 18 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.12.0-1
- Ver Bounce to 17.12.0

* Wed Oct 6 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.11.0-1
- Ver Bounce to 17.11.0

* Fri Sep 17 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.10.0-1
- Ver Bounce to 17.10.0

* Thu Jul 8 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.5.0-1
- Ver Bounce to 17.5.0

* Tue Jun 22 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.4.0-1
- Ver Bounce to 17.4.0

* Mon Jun 14 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.3.0-1
- Ver Bounce to 17.3.0

* Wed May 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.2.0-1
- Ver Bounce to 17.2.0

* Wed May 5 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.1.0-1
- Ver Bounce to 17.1.0

* Mon Apr 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 17.0.0-1
- Ver Bounce to 17.0.0

* Mon Mar 15 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.19.0-1
- Ver Bounce to 16.19.0

* Fri Feb 26 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.18.0-1
- Ver Bounce to 16.18.0

* Mon Feb 15 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.17.0-1
- Ver Bounce to 16.17.0

* Fri Jan 29 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.16.0-1
- Ver Bounce to 16.16.0

* Tue Jan 12 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.15.0-1
- Ver Bounce to 16.15.0

* Mon Jan 4 2021 jess.portnoy@kaltura.com <Jess Portnoy> - 16.14.0-1
- Ver Bounce to 16.14.0

* Mon Dec 14 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.13.0-1
- Ver Bounce to 16.13.0

* Tue Nov 24 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.12.0-1
- Ver Bounce to 16.12.0

* Mon Nov 2 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.11.0-1
- Ver Bounce to 16.11.0

* Wed Oct 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.10.0-1
- Ver Bounce to 16.10.0

* Wed Oct 14 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.9.0-1
- Ver Bounce to 16.9.0

* Sun Aug 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.8.0-1
- Ver Bounce to 16.8.0

* Tue Jul 14 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.7.0-1
- Ver Bounce to 16.7.0

* Wed Jul 8 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.6.0-1
- Ver Bounce to 16.6.0

* Wed Jun 17 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.5.0-1
- Ver Bounce to 16.5.0

* Tue Jun 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.4.0-1
- Ver Bounce to 16.4.0

* Mon May 25 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.3.0-1
- Ver Bounce to 16.3.0

* Tue May 12 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.2.0-1
- Ver Bounce to 16.2.0

* Fri Apr 3 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 16.0.0-1
- Ver Bounce to 16.0.0

* Fri Mar 27 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.20.0-1
- Ver Bounce to 15.20.0

* Wed Mar 4 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.19.0-1
- Ver Bounce to 15.19.0

* Mon Feb 24 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.18.0-1
- Ver Bounce to 15.18.0

* Tue Feb 4 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.17.0-1
- Ver Bounce to 15.17.0

* Tue Jan 28 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.16.0-1
- Ver Bounce to 15.16.0

* Tue Jan 7 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 15.15.0-1
- Ver Bounce to 15.15.0

* Mon Dec 23 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.14.0-1
- Ver Bounce to 15.14.0

* Wed Nov 27 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.12.0-1
- Ver Bounce to 15.12.0

* Tue Nov 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.11.0-1
- Ver Bounce to 15.11.0

* Thu Oct 31 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.10.0-1
- Ver Bounce to 15.10.0

* Thu Oct 10 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.9.0-1
- Ver Bounce to 15.9.0

* Tue Sep 17 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.8.0-1
- Ver Bounce to 15.8.0

* Mon Sep 9 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.7.0-1
- Ver Bounce to 15.7.0 - New GPG key

* Thu Aug 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.6.0-1
- Ver Bounce to 15.6.0

* Thu Aug 8 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.5.0-1
- Ver Bounce to 15.5.0

* Mon Jul 22 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.4.0-1
- Ver Bounce to 15.4.0

* Tue Jul 9 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.3.0-1
- Ver Bounce to 15.3.0

* Mon Jun 24 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.2.0-1
- Ver Bounce to 15.2.0

* Wed May 29 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.1.0-1
- Ver Bounce to 15.1.0

* Tue May 14 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 15.0.0-1
- Ver Bounce to 15.0.0

* Tue Apr 30 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.20.0-1
- Ver Bounce to 14.20.0

* Tue Apr 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.19.0-1
- Ver Bounce to 14.19.0

* Mon Apr 8 2019 Jess Portnoy <jess.portnoy@kaltura.com> - 14.18.0-1
- Ver Bounce to 14.18.0

* Tue Mar 19 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.17.0-1
- Ver Bounce to 14.17.0

* Tue Mar 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.16.0-1
- Ver Bounce to 14.16.0

* Thu Feb 21 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.15.0-1
- Ver Bounce to 14.15.0

* Thu Feb 7 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.14.0-1
- Ver Bounce to 14.14.0

* Mon Jan 21 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.13.0-1
- Ver Bounce to 14.13.0

* Sun Jan 13 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 14.12.0-1
- Ver Bounce to 14.12.0

* Tue Dec 18 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.11.0-1
- Ver Bounce to 14.11.0

* Wed Dec 5 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.10.0-1
- Ver Bounce to 14.10.0

* Wed Nov 21 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.9.0-1
- Ver Bounce to 14.9.0

* Tue Oct 30 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.8.0-1
- Ver Bounce to 14.8.0

* Tue Oct 16 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.7.0-1
- Ver Bounce to 14.7.0

* Tue Aug 28 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.6.0-1
- Ver Bounce to 14.6.0

* Mon Aug 13 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.5.0-1
- Ver Bounce to 14.5.0

* Tue Jul 31 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.4.0-1
- Ver Bounce to 14.4.0

* Tue Jul 24 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.3.0-1
- Ver Bounce to 14.3.0

* Wed Jul 4 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.2.0-1
- Ver Bounce to 14.2.0

* Mon Jun 18 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.1.0-1
- Ver Bounce to 14.1.0

* Tue Jun 5 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 14.0.0-1
- Ver Bounce to 14.0.0

* Tue May 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.20.0-1
- Ver Bounce to 13.20.0

* Mon Apr 23 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.19.0-1
- Ver Bounce to 13.19.0

* Mon Apr 9 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.18.0-1
- Ver Bounce to 13.18.0

* Mon Mar 26 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.17.0-1
- Ver Bounce to 13.17.0

* Mon Mar 12 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.16.0-1
- Ver Bounce to 13.16.0

* Mon Feb 26 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.15.0-1
- Ver Bounce to 13.15.0

* Mon Feb 12 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.14.0-1
- Ver Bounce to 13.14.0

* Mon Jan 29 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.13.0-1
- Ver Bounce to 13.13.0

* Mon Jan 15 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.12.0-1
- Ver Bounce to 13.12.0

* Wed Jan 3 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 13.11.0-1
- Ver Bounce to 13.11.0

* Tue Dec 19 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.10.0-1
- Ver Bounce to 13.10.0

* Mon Dec 4 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.9.0-1
- Ver Bounce to 13.9.0

* Tue Nov 21 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.8.0-1
- Ver Bounce to 13.8.0

* Fri Nov 10 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.7.0-1
- Ver Bounce to 13.7.0

* Mon Oct 23 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.6.0-1
- Ver Bounce to 13.6.0

* Wed Oct 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.5.0-1
- Ver Bounce to 13.5.0

* Mon Oct 8 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.4.0-2
- New repo FS layout

* Mon Sep 25 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.4.0-1
- Ver Bounce to 13.4.0

* Mon Sep 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.3.0-1
- Ver Bounce to 13.3.0

* Tue Aug 15 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.2.0-1
- Ver Bounce to 13.2.0

* Mon Jul 31 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.1.0-1
- Ver Bounce to 13.1.0

* Tue Jul 18 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 13.0.0-1
- Ver Bounce to 13.0.0

* Tue Jul 4 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.20.0-1
- Ver Bounce to 12.20.0

* Tue Jun 20 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.19.0-1
- Ver Bounce to 12.19.0

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.0-1
- Ver Bounce to 12.18.0

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.0-1
- Ver Bounce to 12.18.0

* Mon Jun 5 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.18.00-1
- Ver Bounce to 12.18.00

* Mon May 22 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.17.0-1
- Ver Bounce to 12.17.0

* Tue May 9 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.16.0-1
- Ver Bounce to 12.16.0

* Mon Apr 24 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.15.0-1
- Ver Bounce to 12.15.0

* Mon Mar 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.14.0-1
- Ver Bounce to 12.14.0

* Tue Mar 14 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.13.0-1
- Ver Bounce to 12.13.0

* Tue Feb 28 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.12.0-1
- Ver Bounce to 12.12.0

* Mon Feb 13 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.11.0-1
- Ver Bounce to 12.11.0

* Tue Jan 31 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.10.0-1
- Ver Bounce to 12.10.0

* Mon Jan 9 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 12.9.0-1
- Ver Bounce to 12.9.0

* Thu Dec 22 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.8.0-1
- Ver Bounce to 12.8.0

* Thu Dec 22 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.8.0-1
- Ver Bounce to 12.8.0

* Tue Dec 6 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.7.0-1
- Ver Bounce to 12.7.0

* Thu Nov 24 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.6.0-1
- Ver Bounce to 12.6.0

* Wed Nov 9 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.5.0-1
- Ver Bounce to 12.5.0

* Mon Oct 10 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.4.0-1
- Ver Bounce to 12.4.0

* Tue Sep 27 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.3.0-1
- Ver Bounce to 12.3.0

* Tue Sep 13 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.2.0-1
- Ver Bounce to 12.2.0

* Mon Aug 29 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.1.0-1
- Ver Bounce to 12.1.0

* Mon Aug 15 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.0.0-1
- Ver Bounce to 12.0.0

* Thu Aug 4 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.21.0-1
- Ver Bounce to 11.21.0

* Tue Jul 19 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.20.0-1
- Ver Bounce to 11.20.0

* Tue Jul 12 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.19.0-1
- Ver Bounce to 11.19.0

* Sat Jun 25 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.18.0-1
- Ver Bounce to 11.18.0

* Tue Jun 7 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.17.0-1
- Ver Bounce to 11.17.0

* Tue May 24 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.16.0-1
- Ver Bounce to 11.16.0

* Mon May 9 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.15.0-1
- Ver Bounce to 11.15.0

* Mon Apr 25 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.14.0-1
- Ver Bounce to 11.14.0

* Tue Apr 12 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.13.0-1
- Ver Bounce to 11.13.0

* Mon Mar 28 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.12.0-1
- Ver Bounce to 11.12.0

* Tue Mar 15 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.11.0-1
- Ver Bounce to 11.11.0

* Tue Mar 1 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.10.0-1
- Ver Bounce to 11.10.0

* Mon Feb 15 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.9.0-1
- Ver Bounce to 11.9.0

* Mon Feb 1 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.8.0-1
- Ver Bounce to 11.8.0

* Mon Jan 18 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.7.0-1
- Ver Bounce to 11.7.0

* Mon Jan 4 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 11.6.0-1
- Ver Bounce to 11.6.0

* Mon Dec 21 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.5.0-1
- Ver Bounce to 11.5.0

* Mon Dec 7 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.4.0-1
- Ver Bounce to 11.4.0

* Mon Nov 23 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.3.0-1
- Ver Bounce to 11.3.0

* Mon Nov 9 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.2.0-1
- Ver Bounce to 11.2.0

* Mon Oct 26 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.1.0-1
- Ver Bounce to 11.1.0

* Mon Oct 12 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 11.0.0-1
- Ver Bounce to 11.0.0

* Mon Sep 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.21.0-1
- Ver Bounce to 10.21.0

* Mon Sep 7 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.20.0-1
- Ver Bounce to 10.20.0

* Mon Aug 24 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.19.0-1
- Ver Bounce to 10.19.0

* Mon Aug 10 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.18.0-1
- Ver Bounce to 10.18.0

* Mon Jul 27 2015 jess.portnoy@kaltura.com <Jess Portnoy> - 10.17.0-1
- Ver Bounce to 10.17.0

* Mon Jul 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.16.0-1
- Ver Bounce to 10.16.0

* Mon Jun 29 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.15.0-1
- Ver Bounce to 10.15.0

* Tue Jun 16 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.14.0-1
- Ver Bounce to 10.14.0

* Mon Jun 1 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.13.0-1
- Ver Bounce to 10.13.0

* Tue May 19 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.12.0-1
- Ver Bounce to 10.12.0

* Tue May 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.11.0-1
- Ver Bounce to 10.11.0

* Sun Apr 26 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.10.0-1
- Ver Bounce to 10.10.0

* Mon Apr 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.9.0-1
- Ver Bounce to 10.9.0

* Mon Mar 23 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.8.0-1
- Ver Bounce to 10.8.0

* Sun Mar 15 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.7.0-1
- Ver Bounce to 10.7.0

* Fri Mar 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.6.0-1
- Ver Bounce to 10.6.0

* Wed Feb 11 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.5.0-1
- Ver Bounce to 10.5.0

* Wed Feb 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.4.0-1
- Ver Bounce to 10.4.0

* Tue Jan 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.3.0-1
- Ver Bounce to 10.3.0

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.1.0-1
- Ver Bounce to 10.1.0

* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 10.0.0-1
- Ver Bounce to 10.0.0

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.8-1
- Ver Bounce to 9.19.8

* Mon Nov 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.7-1
- Ver Bounce to 9.19.7

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.6-1
- Ver Bounce to 9.19.6

* Sat Oct 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.5-1
- Ver Bounce to 9.19.5

* Sun Oct 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.4-1
- Ver Bounce to 9.19.4

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.3-1
- Ver Bounce to 9.19.3

* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.19.0-1
- Ver Bounce to 9.19.0

* Sun Jun 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.18.0-1
- Ver Bounce to 9.18.0

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.17.0-1
- Ver Bounce to 9.17.0

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.16.0-1
- Ver Bounce to 9.16.0

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.15.0-1
- Ver Bounce to 9.15.0

* Thu Apr 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.14.0-4
- Changed repo name from stable to latest as requested by Zohar.

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.14.0-1
- Ver Bounce to 9.14.0

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.13.0-1
- Ver Bounce to 9.13.0

* Tue Mar 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-2
- We will be signing our RPMs from now on.

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-1
- Ver Bounce to 9.12.0

* Thu Feb 27 2014 David Bezemer <info@davidbezemer.nl> - 9.11.0-6
- Add testing to base package

* Wed Feb 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-5
- Added update becon.

* Tue Feb 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-3
- URL to repo modified to include 'releases' in path.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-2
- dont need i686

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-1
- 9.11.0

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-1
- 9.9.0

* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- Added 32bit repos.

* Wed Jan 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- initial release.

