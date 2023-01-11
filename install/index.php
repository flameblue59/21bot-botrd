<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$arrError = array();
$getValue = new getValue();
$tool = new tool();

//create settings
$sql = "CREATE TABLE settings(
	id INT(11) AUTO_INCREMENT PRIMARY KEY,
	type VARCHAR(50) NOT NULL,
	value VARCHAR(255) NOT NULL
)";
if(!$process = $conn->query($sql)){
	$arrError[] = 'table settings error';
}
//insert settings
$arrSettings = array(
	'version'=>'1.0.0',
	'timeDelay'=>'-7',
	'affiliateDelay'=>'12',
	'domain'=>'https://stidac.id',
	'securityKey'=>'MKPJHX62C44MMJZYAC7B906Y',
	'websiteName'=>'BOT NUMBER GRABBER',
	'title_homepage'=>'Selamat Datang di [websiteName]',
	'meta_homepage'=>'Kami berusaha untuk memberikan solusi bisnis terbaik, bergabunglah bersama kami untuk membangung mega bisnis bersama-sama',
);
//bind params
$bind = '';
$params = array();
$query = array();
foreach($arrSettings as $type=>$value){
	$bind .= 'ss';
	$params[] = $type;
	$params[] = $value;
	$query[] = '(?,?)';
}
$query = implode(',',$query);
array_unshift($params,$bind);
$params = $tool->refValues($params);
$sql = "INSERT INTO settings(type,value) VALUES $query";
$process = $conn->prepare($sql);
call_user_func_array(array($process,'bind_param'),$params);
$process->execute();
$process->close();

if(count($arrError) > 0 ){
	foreach($arrError as $value){
		echo '<p>'.$value.'</p>';
	}
}
else{
	echo 'berhasil melakukan proses instalasi';
}
?>