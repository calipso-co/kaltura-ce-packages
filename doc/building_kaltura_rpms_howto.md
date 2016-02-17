Required RPMS for build
=======================
rpm-build gcc gcc-c++ git redhat-rpm-config svn wget dos2unix

Extra repos
===========
Extra repos are not needed for installing Kaltura but MUST be configured in order to build some Kaltura dependencies:
EPEL (https://fedoraproject.org/wiki/EPEL), rpmforge (http://repoforge.org/use) and ATRPMS (http://dl.atrpms.net)
Alternatively, you can look up needed additional packages at http://pkgs.org

GIT repo
========
\# git clone https://github.com/kaltura/platform-install-packages

~/rpmbuild dir structure
========================
To setup your build ENV please see here:
http://wiki.centos.org/HowTos/SetupRpmBuildEnvironment

```
$ ll ~/rpmbuild/
total 72
drwxrwxr-x 88 jess jess  4096 Apr  7 03:06 BUILD
drwxr-xr-x 45 jess jess  4096 Apr  7 03:06 BUILDROOT
drwxrwxr-x  6 jess jess  4096 Jan 26 08:03 RPMS
drwxr-xr-x  8 jess jess 12288 Apr  6 11:00 SOURCES -> /sym/link/to/platform-install-packages/RPM/SOURCES
lrwxrwxrwx  1 jess jess    91 Mar 25 10:48 SPECS -> /sym/link/to/platform-install-packages/RPM/SPECS
drwxrwxr-x  2 jess jess 36864 Apr  7 03:06 SRPMS
```

platform-install-packages/RPM/.rpmmacros
========================================
This file specifies vars used in the RPM spec files, currently holds versions of supporting components, for instance, kaltura-kmc needs to know what kmc-login ver to take, etc.
When components are upgraded, this file needs to be edited.
In the build ENV, it should reside at ~/.rpmmacros

platform-install-packages/build dir
================================================
* sources.rc - this file has the ENV vars needed for building from sources. When versions of components are upgraded, they should be modified there.

* packager.rc - should have the following vars:
```
PACKAGER_NAME="First Last"
PACKAGER_MAIL="packager@example.com"
```

* package_*.sh - each component has a wrapper script that fetches the sources from the needed version and packages them so that the RPM can be built.

You will need to edit sources.rc and change:
```
PACKAGER_NAME=""
PACKAGER_MAIL=""
SVN_USER=""
```
You may also change these two although defaults should be fine:
TMP_DIR=/tmp
SOURCE_PACKAGING_DIR=~/sources

And of course:
```
$ mkdir $SOURCE_PACKAGING_DIR
```
Utility scripts
===============
under build/rpm-specific:

* push_rpm.sh - scp the RPM to repo origin and sign it over SSH, then, generate meta data with create repo
* bounce_core_ver.sh

Deployment instructions
================================
Each deployment has instructions here:
https://kaltura.atlassian.net/wiki/display/QAC/QA.Core+Production+Deployments
That includes the new versions for updated components as well as PHP/SQL scripts to run.
The versions should be updated in platform-install-packages/build/sources.rc

Step by step release process
============================
0. run build/rpm-specific/setrep.sh on the repo server

1. read instructions at: https://kaltura.atlassian.net/wiki/display/QAC/QA.Core+Production+Deployments

2. update versions in platform-install-packages/build/sources.rc and ~/.rpmmacros if applicable.

3. if ~/.rpmmacros was updated, also commit under platform-install-packages/RPM/.rpmmacros

4. run platform-install-packages/build/rpm-specifc/bounce_core_ver.sh $NEW_VER
This will update the Core version in the various relevant spec files

5. update specs for additional components according to versions in the deployment doc, i.e:
if KMC is of a new version then update 'Version' in kaltura-kmc.spec, for kdp3, update kaltura-kdp3.spec, etc

6. Add changelog entries according to what is stated in the deployment doc to each component, for instance this is one for kaltura-base - the Core package:
- Ver Bounce to 9.13.0
- PLAT-307 - FFMpeg 2.1.3 integration 
- PLAT-914 - FileSyncImport - re-use curl 
- PLAT-558 - Live streaming should support multiple stream ingest 
- PLAT-932 - Production admin_console: "View History" doesn't work 
- PLAT-1003 - E-mail for notification ,configurable fields override default values 
- SUP-1567 - Problem to duplicate KSR from admin console. 
- SUP-1625 - Avoid creating notification jobs when no notification email is configured

7. for the modified components, run the respective package_*.sh script, for instance, if KMC was updated run:
platform-install-packages/build/package_kaltura_kmc.sh
for KDP3 run:
platform-install-packages/build/package_kaltura_kdp3.sh
and so on.
If a new package is introduces, make sure to create a wrapper script for it as well, in addition to the RPM spec file. 

8. The package_*.sh scripts will retrieve the source archive from GIT/SVN/else and place it in the ~/rpmbuild/SOURCES dir.
Then the script triggers:
```
$ rpmbuild -ba $SPEC
```
if the source retrieval succeeded but build failed, you can simply correct what needs correction and then run:
```
$ rpmbuild -ba $SPEC 
```
one more, no need to repackage for that.

9. once all RPMs are built, use: 
$ platform-install-packages/build/push_rpm.sh /path/to/rpm
this will push the RPMs to the origin server using SCP, sign it and generate new metadata with createrepo.

10. run sanity on the test machine using kaltura-sanity.sh and make sure all passes successfully.

11. run build/set_stable_rep.sh on the repo machine.
