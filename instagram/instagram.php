<?php
use JonnyW\PhantomJs\Client;
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');
$botInstagram = new botInstagram();
$status = $botInstagram->instagram();
if(!ISSET($status['callback'])){
    echo $status['status'].'=>'.$status['notification'];
    return;
}
echo $status['status'].'=>'.$status['callback']['data'];
?>