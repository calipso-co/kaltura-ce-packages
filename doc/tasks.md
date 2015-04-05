# Simple Tasks That Make A Difference!
This document outlines general "smaller" or "easier" tasks that new Kaltura platform developers can take on as learning challenges, but at the same time also be proud of making a valueable contribution to the platform evolution!    
If you decide to take on a challenge, please open a bug with the details of the task, and mark it as yours on the issue queue. We promise to do our best at mentoring you to greatness!

Thanks!

## Port Kaltura's Core to PHP 5_5

## Fix Core's SQL init scripts to support MySQL 5.5

## Admin Console

- Mask passwds in admin console
- Mark mandatory field with '*', red, whatever. For example - the 'Add publisher' form.
- Testme fixes
- format output of testme console in tree-like XML structure
- allow configuration of package and publisher types from admin console
- provide an option to validate a KS, and display what capabilities it provides (especially handy for resolving a missing sview capability)
- when inputting an invalid KS in admin console's sys helper:
```PHP
2014-04-20 05:27:46 [0.000542] [10.0.80.24] [2024683882] [API] [ks->logError] ERR: Hash [>M��!���b�ZHD���] doesn't match sha1 on partner [174].
2014-04-20 05:27:46 [0.000378] [10.0.80.24] [2024683882] [API] [KalturaFrontController->getExceptionObject] CRIT: exception 'Exception' with message 'INVALID_STR' in /opt/kaltura/app/alpha/apps/kaltura/lib/webservices/kSessionUtils.class.php:272
Stack trace: 
#0 /opt/kaltura/app/plugins/admin_console/kaltura_internal_tools/services/KalturaInternalToolsSystemHelperService.php(22): ks::fromSecureString('djJ8MTc0fHK3sNK...')
```

But this is not displayed, instead only: 'Internal server error occurred'
Need to catch the exception and display.

## KMC
- Storage: force 'http' in http delivery URL
- Disallow login to KMC if partner is -2
- Change KMC login to be JS instead of FLASH

## Packages
- Add our packages to ClearOS' repo
- (optionally) add package to EPEL

## Backend Plugins
- Create a plugin for the Monit monitoring tab in admin console

## Client libs
- Add more client libs [http://knowledge.kaltura.com/adding-new-kaltura-api-client-library-generator]
- Write tests for the new NodeJS client libs [http://www.kaltura.com/api_v3/testme/client-libs.php]
- Fix Python units for version 2.6.n and >= 3.0.n
