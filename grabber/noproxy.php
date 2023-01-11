<?php
use JonnyW\PhantomJs\Client;
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$getValue = new getValue();
$bot = new bot();
$tool = new tool();
$securityKey = $getValue->settings('securityKey');
$renderSite = 'dotproperty.id';
$renderUrl = 'https://www.dotproperty.id/properties-for-sale';
$job = 'process';
$type = 'olx'; //change between 'olx' and 'others'
if($type=="olx"){
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
	if($job=='url'){
		echo $bot->grabUrl(array(
			'debug'=>true,
			'type'=>'property',
			'category'=>'property',
			'subCategory'=>'rumah'
		));		
	}
	else{
		$status = $bot->processUrl(array(
			'debug'=>true,
			'urlList'=>$urlList,
			'renderSite'=>'olx.co.id',
			'category'=>'property',
			'subCategory'=>'rumah',
			'noproxy'=>true
		));
		if(is_array($status)){
			print_r($status);
		}
		else{
			echo $status;
		}
	}
}
else{
	if($job=='url'){
		echo $bot->grabUrl(array(
			'debug'=>true,
			'renderSite'=>$renderSite,
			'renderUrl'=>$renderUrl,
			'type'=>'property',
			'category'=>'rumah',
			'id'=>0
		));
	}
	else{
		echo $bot->processUrl(array(
			'debug'=>true,
			'renderSite'=>$renderSite,
			'renderUrl'=>$renderUrl
		));
	}
}
/*
//echo $bot->grabUrl();
		$url = 'https://www.rumah.com/properti-dijual';	
		$chrome_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36';
		$firefox_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0';
		$ie_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko';
		$edge_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063';
		$agents = array($chrome_agent, $firefox_agent, $edge_agent, $ie_agent);
		$userAgent = array_rand(array_flip($agents));
    	$userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36';
		$client = Client::getInstance();
		$client->getProcedureCompiler()->enableCache();
		$client->isLazy();
		$client->getEngine()->setPath($_SERVER["DOCUMENT_ROOT"].'/bin/phantomjs');
		$request = $client->getMessageFactory()->createRequest($url, 'POST');
		$request->addSetting('userAgent', $userAgent);
		$request->addSetting('viewPortSize','{ width: 1440, height: 900 }');
		$response = $client->getMessageFactory()->createResponse();
		// Send the request
		$client->send($request, $response);
		if($response->getStatus() === 200) {
			echo $response->getContent();
		}
		print_r($response->getHeaders());
		echo $response->getContent();
*/
?>
