<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

if(empty($_GET['f'])){
	die('harap isikan fungsi');
}

$botFacebook = new botFacebook();
$botInstagram = new botInstagram();
$f = $_GET['f'];
if($f=="setInterval"){
	$status = $botFacebook->setInterval();
}
else if($f=="resetAccountFacebook"){
	$status = $botFacebook->resetAccount();
}
else if($f=="resetAccountInstagram"){
	$status = $botInstagram->resetAccount();
}
print_r($status);
?>