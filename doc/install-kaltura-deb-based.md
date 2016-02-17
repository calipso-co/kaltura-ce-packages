﻿# Installing Kaltura on a Single Server (deb)
This guide describes deb installation of an all-in-one Kaltura server and applies to deb based Linux distros.

The processes was tested on Debian 8 and Ubuntu 14.04 but is expected to work on other versions. If you tried a deb based distro and failed, please report it.


[Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). Please note that this service in only offered for RHEL based distros. 

#### Table of Contents
[Prerequites](https://github.com/kaltura/platform-install-packages/blob/master/doc/pre-requisites.md)

[Step-by-step Installation](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-deb-based.md#step-by-step-installation)

[Unattended Installation](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-deb-based.md#unattended-installation)

[Upgrade Kaltura](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-deb-based.md#upgrade-kaltura)

[Remove Kaltura](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-deb-based.md#remove-kaltura)

[Troubleshooting](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-deb-based.md#troubleshooting)

[Additional Information](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#additional-information)

[How to contribute](https://github.com/kaltura/platform-install-packages/blob/master/doc/CONTRIBUTERS.md)

## Step-by-step Installation

### Pre-Install notes
* This install guides assumes that you did a clean, basic install of one of the deb based OSes in 64bit architecture.
* When installing, you will be prompted for each server's resolvable hostname. Note that it is crucial that all host names will be resolvable by other servers in the cluster (and outside the cluster for front machines). Before installing, verify that your /etc/hosts file is properly configured and that all Kaltura server hostnames are resolvable in your network.
* Before you begin, make sure you're logged in as the system root. Root access is required to install Kaltura, and you should execute ```sudo -i``` or ```su -```to make sure that you are indeed root.

#### Firewall requirements
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-required-ports.md).
If you're just testing and don't mind an open system, you can use the below to disbale iptables altogether:
```bash
iptables -F
service iptables stop
chkconfig iptables off
```
#### Disable SELinux - REQUIRED
**Currently Kaltura doesn't properly support running with SELinux, things will break if you don't set it to permissive**.

```bash
setenforce permissive
```

To verify SELinux will not revert to enabled next restart:

1. Edit the file `/etc/selinux/config`
1. Verify or change the value of SELINUX to permissive: `SELINUX=permissive`
1. Save the file `/etc/selinux/config`

### Start of Kaltura installation
This section is a step-by-step guide of a Kaltura installation.

#### Setup the Kaltura deb repository

```bash
wget -O - http://installrepo.kaltura.org/repo/apt/debian/kaltura-deb.gpg.key|apt-key add -
echo "deb [arch=amd64] http://installrepo.kaltura.org/repo/apt/debian kajam main" > /etc/apt/sources.list.d/kaltura.list
```

*NOTE: for Debian, the non-free repo must also be enabled*

*Ubuntu NOTE: You must also make sure the multiverse repo is enabled in /etc/apt/sources.list*

*Debian Jessie [8] NOTE: You must also make sure the following Wheezy repos are enabled in /etc/apt/sources.list*
```
deb http://ftp.debian.org/debian/ wheezy main
deb http://security.debian.org/ wheezy/updates main
```

IMPORTANT NOTE: 

depending on your current Apache configuration, you may need to disable your default site configuration.

Use:
```
# apachectl -t -DDUMP_VHOSTS
```
to check your current configuration and:
```
a2dissite $SITENAME
```
to disable any site that might be set in a way by which $YOUR_SERVICE_URL/api_v3 will reach it instead of the Kaltura vhost config.

In such case, the postinst script for kaltrua-db will fail, if so, adjust it and run:
```
# dpkg-reconfigure kaltura-db
```



#### MySQL Install and Configuration
Please note that for MySQL version 5.5 and above, you must first disable strict mode enforcement.
See:
https://support.realtyna.com/index.php?/Knowledgebase/Article/View/535/0/how-can-i-turn-off-mysql-strict-mode

#### Install Kaltura Server with PHP 7
By default, the installation is done against the PHP stack available from the official repo.
Kaltura now offers beta deb packages of PHP 7 which can be installed from our repo.
In order to install the server using these packages, simply run:
```bash
# wget -O - http://installrepo.kaltura.org/repo/apt/debian/kaltura-deb.gpg.key|apt-key add -
# echo "deb [arch=amd64] http://installrepo.kaltura.org/repo/apt/debian kajam main" > /etc/apt/sources.list.d/kaltura.list
# aptitude update
# aptitude install kaltura-php7
```
And the follow the instructions for installing the Kaltura server as normal.

#### Install Kaltura Server
You can use this process to auto install an all in 1 server.
In order to perform a manual step by step install, simply copy the commands and run them one by one.

*NOTE: the script calls aptitude with -y which means you will not be prompted to confirm the packages about to be installed.*

```bash
# wget http://installrepo.kaltura.org/repo/apt/debian/install_kaltura_all_in_1.sh 
# chmod +x install_kaltura_all_in_1.sh
# ./install_kaltura_all_in_1.sh
```

#### Configure Red5 server
1. install the kaltura-red5 package:
```
# aptitude install kaltura-red5
```
1. Request http://hostname:5080
1. Click 'Install a ready-made application'
1. Mark 'OFLA Demo' and click 'Install'
1. Edit /usr/lib/red5/webapps/oflaDemo/index.html and replace 'localhost' with your actual Red5 hostname or IP
1. Test OflaDemo by making a request to http://hostname:5080/oflaDemo/ and playing the sample videos
1. Run:

```bash
/opt/kaltura/bin/kaltura-red5-config.sh
```



**Your Kaltura installation is now complete.**

## SSL Step-by-step Installation
### Pre-Install notes
* Currently, the Nginx VOD module does not support integration with Kaltura over HTTPs, only HTTP is supported. 
### SSL Certificate Configuration


**Your Kaltura installation is now complete.**

## Unattended Installation
Edit the debconf [response file template](https://github.com/kaltura/platform-install-packages/blob/Jupiter-10.16.0/deb/kaltura_debconf_response.sh) by replacing all tokens with relevant values.
and run it as root:
```
./kaltura_debconf_response.sh
```
the set the DEBIAN_FRONTEND ENV var:
```
export DEBIAN_FRONTEND=noninteractive
```

And install as described above. 

## Upgrade Kaltura
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
# aptitude update
# aptitude install ~Nkaltura
# dpkg-reconfigure kaltura-base
# dpkg-reconfigure kaltura-front
# dpkg-reconfigure kaltura-batch
```

## Remove Kaltura
Use this in cases where you want to clear the database and start from fresh.
```bash
# /opt/kaltura/bin/kaltura-drop-db.sh
# aptitude purge ~Nkaltura
# rm -rf /opt/kaltura
```

## Troubleshooting
Once the configuration phase is done, you may wish to run the sanity tests, for that, run:
```base
/opt/kaltura/bin/kaltura-sanity.sh
```

If you experience unknown, unwanted or erroneous behaviour, the logs are a greta place to start, to get a quick view into errors and warning run:
```bash
kaltlog
```

If this does not give enough information, increase logging verbosity:
```bash
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' /opt/kaltura/app/configurations/logger.ini
```

To revert this logging verbosity run:
```bash
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*4@writers.\1.filters.priority.priority=7@g' /opt/kaltura/app/configurations/logger.ini
```

Or output all logged information to a file for analysis:
```bash
allkaltlog > /path/to/mylogfile.log
```

For posting questions, please go to:
(http://forum.kaltura.org)

## Additional Information
* Please review the [frequently answered questions](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-packages-faq.md) document for general help before posting to the forums or issue queue.
* This guide describes the installation and upgrade of an all-in-one machine where all the Kaltura components are installed on the same server. For cluster deployments, please refer to [cluster deployment document](http://bit.ly/kipp-cluster-yum), or [Deploying Kaltura using Opscode Chef](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-chef-cluster-deployment.md).
* To learn about monitoring, please refer to [configuring platform monitors](http://bit.ly/kipp-monitoring).
* Testers using virtualization: [@DBezemer](https://github.com/kaltura) created a basic CentOS 6.4 template virtual server vailable here in OVF format: https://www.dropbox.com/s/luai7sk8nmihrkx/20140306_CentOS-base.zip
* Alternatively you can find VMWare images at - http://www.thoughtpolice.co.uk/vmware/ --> Make sure to only use compatible OS images; either RedHat or CentOS 5.n, 6.n or FedoraCore 18+.
* Two working solutions to the AWS EC2 email limitations are:
  * Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
  * Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/).
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing deb based users, Kaltura offers commercial upgrade options.
