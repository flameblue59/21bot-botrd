<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$bot = new bot();

echo $bot->work('processUrl');
?>