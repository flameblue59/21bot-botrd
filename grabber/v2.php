<?php
use JonnyW\PhantomJs\Client;
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$getValue = new getValue();
$bot = new bot();
$tool = new tool();
$securityKey = $getValue->settings('securityKey');

$field = array('securityKey'=>$securityKey,'category'=>'property');
$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=402f60o58g&rand='.rand(0,999),'post'=>true,'field'=>$field));
if(!ISSET($curl['object'])){
	die('<script>
			setTimeout(function(){
				window.location.reload();
				setTimeout(function(){
					window.location.reload();
				},600000);
			},10000);
		</script>kesalahan load curl getTarget '.$tool->safeJsonEncode($curl));
}
$urlList = $curl['object']['data'];

$status = $bot->processOlx('v2',array(
	'debug'=>true,
	'urlList'=>$urlList,
	'renderSite'=>'olx.co.id',
	'category'=>'property',
	'subCategory'=>'rumah',
	'noproxy'=>true
));

if(is_array($status)){
	print_r($status);
	$status = implode(',',$status);
}

$body = "<script>
setTimeout(function(){
	window.location.reload();
	setTimeout(function(){
		window.location.reload();
	},300000);
},3000);
</script>".$status;
echo $body;
?>
