<?php
use JonnyW\PhantomJs\Client;
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');
$botTwitter = new botTwitter();
$botTwitter->twitter();
?>