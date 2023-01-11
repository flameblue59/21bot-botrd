<?php
use JonnyW\PhantomJs\Client;
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');
$botInstagram = new botInstagram();
$botInstagram->instagram();
?>