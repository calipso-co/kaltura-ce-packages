<?php

if (count($argv)<4){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <minus_2_secret> <profile name> <delivery url> <storage host> <storage basedir> <remote storage username> <remote storage passwd> <playback proto>'."\n";
    exit (1);
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');

$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
$profile_name=$argv[4];
$delivery_url=$argv[5];
$storage_host=$argv[6];
$storage_basedir=$argv[6];
$storage_user=$argv[7];
$storage_passwd=$argv[8];
$basedir=dirname(__FILE__);
$playback_protocol=$argv[9];
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $service_url;  
$client = new KalturaClient($config);
$config->partnerId=$partnerId;
$client->setConfig($config);
$ks = $client->session->start($secret, null, KalturaSessionType::ADMIN, -2, null,null);
$client->setKs($ks);
$delivery = new KalturaDeliveryProfile();
$delivery->name = $profile_name;
$delivery->type = KalturaDeliveryProfileType::HTTP;
$delivery->systemName = $profile_name;
$delivery->url = $delivery_url;
$delivery->isDefault = KalturaNullableBoolean::TRUE_VALUE;
var_dump($client->deliveryProfile->add($delivery));

$storageProfile = new KalturaStorageProfile();
$storageProfile->name = $profile_name;
$storageProfile->systemName = $profile_name;
$storageProfile->status = KalturaStorageProfileStatus::AUTOMATIC;
$storageProfile->protocol = KalturaStorageProfileProtocol::SFTP;
$storageProfile->storageUrl = $storage_host;
$storageProfile->storageBaseDir = $storage_basedir;
$storageProfile->storageUsername = $storage_user;
$storageProfile->storagePassword = $storage_passwd;
$storageProfile->deliveryProfileIds = array();
$storageProfile->deliveryProfileIds[0] = new KalturaKeyValue();
$storageProfile->deliveryProfileIds[0]->key = $playback_protocol;
$storageProfile->deliveryProfileIds[0]->value = $delivery_obj->id;
$result = $client->storageProfile->add($storageProfile);
var_dump($result);
