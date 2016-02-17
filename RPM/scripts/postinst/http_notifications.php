<?php
if($argc<4){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url>'."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = KalturaSessionType::ADMIN;
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

// list available HTTP templates:
$filter = new KalturaEventNotificationTemplateFilter();
$filter->systemNameEqual = 'HTTP_ENTRY_STATUS_CHANGED';
$pager = null;
$eventNotificationTemplate = new KalturaHttpNotificationTemplate();
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$notification_templates = $eventnotificationPlugin->eventNotificationTemplate->listTemplates($filter, $pager);
// id for entry change:
if (isset($notification_templates->objects[0]->id)){
	$template_id=$notification_templates->objects[0]->id;
}else{
	die("\nNo HTTP templates exist.\n Try running:\nphp /opt/kaltura/app/tests/standAloneClient/exec.php /opt/kaltura/app/tests/standAloneClient/httpNotificationsTemplate.xml /tmp/out.xml\nPassing -2 as partner ID");
}

// clone the template to partner:
$result = $eventnotificationPlugin->eventNotificationTemplate->cloneAction($template_id, $eventNotificationTemplate);
$notification_id = $result->id;

// activate template
$status = KalturaEventNotificationTemplateStatus::ACTIVE;
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->updateStatus($notification_id, $status);

// update url:
$eventNotificationTemplate->type = KalturaEventNotificationTemplateType::HTTP;
$eventNotificationTemplate->eventType = KalturaEventNotificationEventType::BATCH_JOB_STATUS;
$eventNotificationTemplate->eventObjectType = KalturaEventNotificationEventObjectType::ENTRY;
$eventNotificationTemplate->contentParameters = array();
$eventNotificationTemplate->contentParameters[0] = new KalturaEventNotificationParameter();
$eventNotificationTemplate->contentParameters[1] = new KalturaEventNotificationParameter();
$eventNotificationTemplate->contentParameters[2] = null;
$eventNotificationTemplate->contentParameters[3] = null;
$eventNotificationTemplate->url = 'http://localhost/1.php';
$KalturaHttpNotificationDataFields=new KalturaHttpNotificationDataFields();
$eventNotificationTemplate->data = $KalturaHttpNotificationDataFields;
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->update($notification_id, $eventNotificationTemplate);
$eventnotificationPlugin->eventNotificationTemplate->delete($notification_id);
echo('ID: '. $result->id. ', URL: '.$result->url);
?>
