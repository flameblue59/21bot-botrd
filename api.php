<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

if(empty($_GET['f'])){
	die('harap isikan fungsi');
}

$botFacebook = new botFacebook();
$botInstagram = new botInstagram();
$botTwitter = new botTwitter();
$f = $_GET['f'];
if($f=="setIntervalFacebook"){
	$status = $botFacebook->setInterval();
}
else if($f=="setIntervalTwitter"){
	$status = $botTwitter->setInterval();
}
else if($f=="resetAccountFacebook"){
	$status = $botFacebook->resetAccount();
}
else if($f=="resetAccountInstagram"){
	$status = $botInstagram->resetAccount();
}
else if($f=="resetAccountTwitter"){
	$status = $botTwitter->resetAccount();
}
print_r($status);
?>