<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$arrError = array();
$getValue = new getValue();
$tool = new tool();
$version = $getValue->settings('version');
if($version=="1.0.0"){
	$sql = "CREATE TABLE data_url(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		source VARCHAR(50) NOT NULL,
		url VARCHAR(255) NOT NULL,
		status VARCHAR(25) NOT NULL,
		waktu DATETIME NOT NULL	
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database data_url';
	}
	$version = "1.0.1";
}
if($version=="1.0.1"){
	$sql = "CREATE TABLE banned_account(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		email VARCHAR(255) UNIQUE NOT NULL DEFAULT '',
		tries INT(11) NOT NULL DEFAULT 0,
		password VARCHAR(100) NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database data_url';
	}
	$sql = "CREATE TABLE account_data(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		email VARCHAR(255) UNIQUE NOT NULL DEFAULT '',
		password VARCHAR(255) NOT NULL DEFAULT '',
		lastSync DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database account_data';
	}	
	$version = "1.0.2";
}
if($version=="1.0.2"){
	$sql = "ALTER TABLE banned_account ADD COLUMN banned TINYINT(1) NOT NULL DEFAULT 0 after password";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal alter table banned_account';
	}	
	$sql = "ALTER TABLE banned_account ADD COLUMN bannedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() after banned";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal alter table banned_account';
	}
	$sql = "CREATE TABLE number_vault(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		category VARCHAR(25) NOT NULL DEFAULT '',
		subCategory VARCHAR(25) NOT NULL DEFAULT '',
		source VARCHAR(20) NOT NULL DEFAULT '',
		uid VARCHAR(25) NOT NULL DEFAULT '',
		name VARCHAR(100) NOT NULL DEFAULT '',
		number VARCHAR(25) UNIQUE NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal create table number_vault';
	}
	$sql = "CREATE TABLE olx_pool(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		start VARCHAR(20) NOT NULL DEFAULT 0,
		end VARCHAR(11) NOT NULL DEFAULT 0,
		done TINYINT(1) NOT NULL DEFAULT 0,
		rendered DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal create table olx_pool';
	}
	//inserting pool data
	$start = 100010000;
	$end = 125000000;
	$increment = 1000;
	$batch = 1;
	$bind = '';
	$params = array();
	$query = array();
	while($start < $end){
		$bind .= 'ss';
		$params[] = $start;
		$params[] = $start+$increment;
		$query[] = '(?,?)';
		$start += $increment;
		if($batch % 2000==false){
			echo $batch;
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = implode(',',$query);
			//inserting pool
			$sql = "INSERT INTO olx_pool(start,end) VALUES $query";
			$process = $conn->prepare($sql);
			call_user_func_array(array($process,'bind_param'),$params);
			$process->execute();
			$process->close();	
			//reseting bind & params
			$bind = '';
			$params = array();
			$query = array();		
		}
		$batch++;
	}
	//inserting olxUID
	$sql = "INSERT INTO settings(type,value) VALUES('olxUID','100000000')";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();
	//create low account data
	$sql = "CREATE TABLE account_data_low(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		email VARCHAR(255) UNIQUE NOT NULL DEFAULT '',
		password VARCHAR(255) NOT NULL DEFAULT '',
		lastSync DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		logout TINYINT(1) NOT NULL DEFAULT 0,
		banned TINYINT(1) NOT NULL DEFAULT 0,
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database account_data';
	}
	//create grabber_account to run [grabber url]
	$sql = "CREATE TABLE grabber_account(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		account VARCHAR(100) UNIQUE NOT NULL DEFAULT '',
		lastSync DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database grabber_account';
	}	
	//creating account to grabber_account
	$bind = '';
	$params = array();
	$query = array();
	for($i=1; $i<=20; $i++){
		$account = "account".$i;
		$bind .= 's';
		$params[] = $account;
		$query[] = "(?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO grabber_account(account) VALUES $query ON DUPLICATE KEY UPDATE account=account";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();
	//add profile UID data
	$sql = "CREATE TABLE olx_rendered_uid(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(50) NOT NULL DEFAULT '',
		profileUid VARCHAR(50) UNIQUE NOT NULL DEFAULT '',
		nomor VARCHAR(50) NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database olx_rendered_uid';
	}
	$version = "1.0.3";
}
if($version=="1.0.3"){
	//create pyCommand in settings
	$pyCommand = 'py';	
	$sql = "INSERT INTO settings(type,value) VALUES('pyCommand',?)";
	$process = $conn->prepare($sql);
	$process->bind_param('s',$pyCommand);
	$process->execute();
	$process->close();	
	//create localhostPath in settings
	$pyCommand = 'C:/XAMPP/htdocs/botrd/';	
	$sql = "INSERT INTO settings(type,value) VALUES('localhostPath',?)";
	$process = $conn->prepare($sql);
	$process->bind_param('s',$pyCommand);
	$process->execute();
	$process->close();
	//create filePath in settings
	$path = 'c:\\';	
	$sql = "INSERT INTO settings(type,value) VALUES('filePath',?)";
	$process = $conn->prepare($sql);
	$process->bind_param('s',$path);
	$process->execute();
	$process->close();
	//create filePath in settings
	$slashDir = '\\';	
	$sql = "INSERT INTO settings(type,value) VALUES('slashDir',?)";
	$process = $conn->prepare($sql);
	$process->bind_param('s',$slashDir);
	$process->execute();
	$process->close();	
	//creating proxy_data table
	$sql = "CREATE TABLE proxy_data(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		proxy VARCHAR(255) NOT NULL DEFAULT '',
		lastSync DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database proxy_data';
	}
	//inserting proxies
	$arrProxy = array(
		"155.94.232.5:8800",
		"188.119.89.219:8800",
		"188.119.91.222:8800",
		"188.119.89.129:8800",
		"188.119.89.230:8800",
		"188.119.91.212:8800",
		"155.94.232.179:8800",
		"192.126.220.56:8800",
		"155.94.232.192:8800",
		"188.119.89.234:8800",
		"188.119.89.238:8800",
		"188.119.91.10:8800",
		"192.126.219.66:8800",
		"104.223.48.42:8800",
		"104.223.48.102:8800",
		"155.94.232.10:8800",
		"192.126.219.191:8800",
		"192.126.220.111:8800",
		"188.119.89.187:8800",
		"188.119.89.26:8800",
		"188.119.91.141:8800",
		"192.126.219.104:8800",
		"188.119.89.223:8800",
		"188.119.91.94:8800",
		"188.119.89.195:8800",
		"192.126.220.38:8800",
		"192.126.219.192:8800",
		"188.119.89.94:8800",
		"188.119.91.31:8800",
		"192.126.220.153:8800",
		"188.119.91.196:8800",
		"188.119.89.149:8800",
		"188.119.91.252:8800",
		"192.126.219.9:8800",
		"104.223.48.101:8800",
		"188.119.91.159:8800",
		"192.126.219.15:8800",
		"104.223.48.25:8800",
		"188.119.91.217:8800",
		"188.119.91.195:8800",
		"104.223.48.116:8800",
		"188.119.89.215:8800",
		"104.223.48.47:8800",
		"192.126.220.239:8800",
		"192.126.220.69:8800",
		"155.94.232.240:8800",
		"155.94.232.53:8800",
		"188.119.91.103:8800",
		"188.119.89.66:8800",
		"188.119.89.103:8800",
	);
	$bind = '';
	$params = array();
	$query = array();
	foreach($arrProxy as $proxy){
		$bind .= 's';
		$params[] = $proxy;
		$query[] = "(?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO proxy_data(proxy) VALUES $query";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();	
	$version = "1.0.4";
}
if($version=="1.0.4"){
	$sql = "CREATE TABLE facebook_account(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		password VARCHAR(100) NOT NULL DEFAULT '',
		proxy VARCHAR(50) NOT NULL DEFAULT '',
		likes INT(11) NOT NULL DEFAULT 0,		
		maxLikes INT(11) NOT NULL DEFAULT 20,
		comment INT(11) NOT NULL DEFAULT 0,
		maxComment INT(11) NOT NULL DEFAULT 5,
		addFriend INT(11) NOT NULL DEFAULT 0,
		maxAddFriend INT(11) NOT NULL DEFAULT 20,
		confirmFriend INT(11) NOT NULL DEFAULT 0,
		maxConfirmFriend INT(11) NOT NULL DEFAULT 50,
		unFriend INT(11) NOT NULL DEFAULT 0,
		maxUnFriend INT(11) NOT NULL DEFAULT 20,
		profileWalk INT(11) NOT NULL DEFAULT 0,
		maxProfileWalk INT(11) NOT NULL DEFAULT 20,
		profilePostStatus INT(11) NOT NULL DEFAULT 0,
		maxProfilePostStatus INT(11) NOT NULL DEFAULT 2,
		profilePostPhoto INT(11) NOT NULL DEFAULT 0,
		maxProfilePostPhoto INT(11) NOT NULL DEFAULT 1,
		groupInvite INT(11) NOT NULL DEFAULT 0,
		maxGroupInvite INT(11) NOT NULL DEFAULT 50,
		groupPostStatus INT(11) NOT NULL DEFAULT 0,
		maxGroupPostStatus INT(11) NOT NULL DEFAULT 1,
		groupPostPhoto INT(11) NOT NULL DEFAULT 0,
		maxGroupPostPhoto INT(11) NOT NULL DEFAULT 2,
		likeInterval INT(11) NOT NULL DEFAULT 5,
		commentInterval INT(11) NOT NULL DEFAULT 10,
		addFriendInterval INT(11) NOT NULL DEFAULT 5,		
		confirmFriendInterval INT(11) NOT NULL DEFAULT 5,
		unFriendInterval INT(11) NOT NULL DEFAULT 5,
		groupInviteInterval INT(11) NOT NULL DEFAULT 5,
		profileWalkInterval INT(11) NOT NULL DEFAULT 2,
		profilePostInterval INT(11) NOT NULL DEFAULT 120,
		groupPostInterval INT(11) NOT NULL DEFAULT 120,
		restInterval INT(11) NOT NULL DEFAULT 30,
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database facebook_account';
	}
	$sql = "CREATE TABLE facebook_activity(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		activity VARCHAR(50) NOT NULL DEFAULT '',
		done TINYINT(1) NOT NULL DEFAULT 0,
		runAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database facebook_activity';
	}
	$sql = "CREATE TABLE facebook_activity_log(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		activity VARCHAR(50) NOT NULL DEFAULT '',
		done TINYINT(1) NOT NULL DEFAULT 0,
		runAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database facebook_activity';
	}	
	$sql = "CREATE TABLE posted_group_image(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		filename VARCHAR(255) NOT NULL DEFAULT '',
		posted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database posted_group_image';
	}
	$sql = "CREATE TABLE posted_profile_image(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		filename VARCHAR(255) NOT NULL DEFAULT '',
		posted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database posted_profile_image';
	}
	$version = "1.0.5";
}
if($version=="1.0.5"){
	$sql = "CREATE TABLE facebook_status(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		category VARCHAR(255) NOT NULL DEFAULT '',
		language VARCHAR(25) NOT NULL DEFAULT '',
		text TEXT UNIQUE NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database facebook_status';
	}	
	$arrLanguage = array(
		array('category'=>'jodoh','language'=>'id','text'=>'Salam kenal ya.. yg kesepian boleh add aku'),
		array('category'=>'jodoh','language'=>'id','text'=>'Barangkali ada yang mau kenalan..'),
		array('category'=>'jodoh','language'=>'id','text'=>'Yuk berteman sama aku..'),
		array('category'=>'jodoh','language'=>'id','text'=>'Cari temen chat..'),
		array('category'=>'jodoh','language'=>'id','text'=>'Temanan yuk kakak..'),
		array('category'=>'jodoh','language'=>'id','text'=>'Pengen cari yang terbaik!'),
		array('category'=>'jodoh','language'=>'id','text'=>'Siapa tau ada yang mau kenalan sama aku'),
		array('category'=>'jodoh','language'=>'id','text'=>'Ingin rasanya mencintai tapi apalah daya saat hati sudah tersakiti'),
		array('category'=>'jodoh','language'=>'id','text'=>'Pacaran yuk kak, tukeran pap sama aku'),
		array('category'=>'jodoh','language'=>'id','text'=>'Biar ga bosen chat sama aku yuk'),
		array('category'=>'jodoh','language'=>'id','text'=>'Pengen punya pacar yang serius ^_^'),
		array('category'=>'jodoh','language'=>'id','text'=>'Andai mereka tau yang aku rasakan..'),
		array('category'=>'jodoh','language'=>'id','text'=>'Kadang iri liat orang lain pacaran tapi susah banget cari yang baik'),
		array('category'=>'jodoh','language'=>'id','text'=>'cari temen buat iseng curhat aja..'),
		array('category'=>'jodoh','language'=>'id','text'=>'Semoga aja hari ini akan lebih baik, dipertemukan dengan yang baik2 #melupakanmantan'),		
	);
	//inserting data
	$bind = '';
	$params = array();
	$query = array();
	foreach($arrLanguage as $arr){
		$bind .= 'sss';
		$params[] = $arr['category'];
		$params[] = $arr['language'];
		$params[] = $arr['text'];
		$query[] = "(?,?,?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO facebook_status(category,language,text) VALUES $query";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();
	//inserting facebook comment
	$sql = "CREATE TABLE facebook_comment(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		category VARCHAR(255) NOT NULL DEFAULT '',
		language VARCHAR(25) NOT NULL DEFAULT '',
		text TEXT UNIQUE NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database facebook_comment';
	}		
	$arrLanguage = array(
		array('category'=>'general','language'=>'id','text'=>'ok kak..'),
		array('category'=>'general','language'=>'id','text'=>'aku merasakanmu'),
		array('category'=>'general','language'=>'id','text'=>'pengen kenalan'),
		array('category'=>'general','language'=>'id','text'=>'sip..'),
		array('category'=>'general','language'=>'id','text'=>'sip deh'),
		array('category'=>'general','language'=>'id','text'=>'okein aja'),
		array('category'=>'general','language'=>'id','text'=>'ya kali'),
		array('category'=>'general','language'=>'id','text'=>'coba aja hihi'),
		array('category'=>'general','language'=>'id','text'=>'haha'),
		array('category'=>'general','language'=>'id','text'=>'hehe'),
		array('category'=>'general','language'=>'id','text'=>'pasti bisa'),
		array('category'=>'general','language'=>'id','text'=>'cobain ah'),
		array('category'=>'general','language'=>'id','text'=>'pengen nyoba ah'),
		array('category'=>'general','language'=>'id','text'=>'pengen nyoba'),
		array('category'=>'general','language'=>'id','text'=>'kadang-kadang ah'),
		array('category'=>'general','language'=>'id','text'=>'sabarin aja'),
		array('category'=>'general','language'=>'id','text'=>'mencoba sabar'),
		array('category'=>'general','language'=>'id','text'=>'memang sulit sih..'),
		array('category'=>'general','language'=>'id','text'=>'aku pun gitu'),
		array('category'=>'general','language'=>'id','text'=>'harus bisa'),
		array('category'=>'general','language'=>'id','text'=>'harusin aja..'),
	);
	//inserting data
	$bind = '';
	$params = array();
	$query = array();
	foreach($arrLanguage as $arr){
		$bind .= 'sss';
		$params[] = $arr['category'];
		$params[] = $arr['language'];
		$params[] = $arr['text'];
		$query[] = "(?,?,?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO facebook_comment(category,language,text) VALUES $query";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();	
	$sql = "CREATE TABLE facebook_profile(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		profileId VARCHAR(25) UNIQUE NOT NULL DEFAULT '',
		profileLink VARCHAR(255) NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database facebook_profile';
	}
	$sql = "INSERT INTO settings(type,value) VALUES('facebookReset',CURRENT_TIMESTAMP())";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();
	$version = "1.0.6";
}
if($version=="1.0.6"){
	$sql = "CREATE TABLE tiktok_account(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		email VARCHAR(255) NOT NULL DEFAULT '',
		password VARCHAR(100) NOT NULL DEFAULT '',
		proxy VARCHAR(255) NOT NULL DEFAULT '',
		follow INT(11) NOT NULL DEFAULT 0,
		maxFollow INT(11) NOT NULL DEFAULT 100,
		comment INT(11) NOT NULL DEFAULT 0,
		maxComment INT(11) NOT NULL DEFAULT 20,
		followInterval INT(11) NOT NULL DEFAULT 3,
		commentInterval INT(11) NOT NULL DEFAULT 10,
		restInterval INT(11) NOT NULL DEFAULT 30,		
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database tiktok_account';
	}	
	$sql = "CREATE TABLE tiktok_activity(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		activity VARCHAR(50) NOT NULL DEFAULT '',
		done TINYINT(1) NOT NULL DEFAULT 0,
		runAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database tiktok_activity';
	}
	$sql = "CREATE TABLE tiktok_activity_log(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		activity VARCHAR(50) NOT NULL DEFAULT '',
		done TINYINT(1) NOT NULL DEFAULT 0,
		runAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database tiktok_activity_log';
	}
	//inserting tiktok comment
	$sql = "CREATE TABLE tiktok_comment(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		category VARCHAR(255) NOT NULL DEFAULT '',
		language VARCHAR(25) NOT NULL DEFAULT '',
		text TEXT UNIQUE NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database tiktok_comment';
	}		
	$arrLanguage = array(
		array('category'=>'general','language'=>'id','text'=>'ok kak..'),
		array('category'=>'general','language'=>'id','text'=>'aku merasakanmu'),
		array('category'=>'general','language'=>'id','text'=>'pengen kenalan'),
		array('category'=>'general','language'=>'id','text'=>'sip..'),
		array('category'=>'general','language'=>'id','text'=>'sip deh'),
		array('category'=>'general','language'=>'id','text'=>'okein aja'),
		array('category'=>'general','language'=>'id','text'=>'ya kali'),
		array('category'=>'general','language'=>'id','text'=>'coba aja hihi'),
		array('category'=>'general','language'=>'id','text'=>'haha'),
		array('category'=>'general','language'=>'id','text'=>'hehe'),
		array('category'=>'general','language'=>'id','text'=>'pasti bisa'),
		array('category'=>'general','language'=>'id','text'=>'cobain ah'),
		array('category'=>'general','language'=>'id','text'=>'pengen nyoba ah'),
		array('category'=>'general','language'=>'id','text'=>'pengen nyoba'),
		array('category'=>'general','language'=>'id','text'=>'kadang-kadang ah'),
		array('category'=>'general','language'=>'id','text'=>'sabarin aja'),
		array('category'=>'general','language'=>'id','text'=>'memang sulit sih..'),
		array('category'=>'general','language'=>'id','text'=>'aku pun gitu'),
		array('category'=>'general','language'=>'id','text'=>'harus bisa'),
		array('category'=>'general','language'=>'id','text'=>'harusin aja..'),
		array('category'=>'general','language'=>'id','text'=>'lucu..'),		
	);
	//inserting data
	$bind = '';
	$params = array();
	$query = array();
	foreach($arrLanguage as $arr){
		$bind .= 'sss';
		$params[] = $arr['category'];
		$params[] = $arr['language'];
		$params[] = $arr['text'];
		$query[] = "(?,?,?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO tiktok_comment(category,language,text) VALUES $query";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();
	$version = "1.0.7";
}
else if($version=="1.0.7"){
	$sql = "CREATE TABLE instagram_account(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		password VARCHAR(100) NOT NULL DEFAULT '',
		proxy VARCHAR(50) NOT NULL DEFAULT '',
		post INT(11) NOT NULL DEFAULT 0,		
		maxPost INT(11) NOT NULL DEFAULT 2,		
		likes INT(11) NOT NULL DEFAULT 0,		
		maxLikes INT(11) NOT NULL DEFAULT 20,
		comment INT(11) NOT NULL DEFAULT 0,
		maxComment INT(11) NOT NULL DEFAULT 5,
		follow INT(11) NOT NULL DEFAULT 0,
		maxFollow INT(11) NOT NULL DEFAULT 10,
		unfollow INT(11) NOT NULL DEFAULT 0,
		maxUnfollow INT(11) NOT NULL DEFAULT 10,
		postInterval INT(11) NOT NULL DEFAULT 120,		
		likeInterval INT(11) NOT NULL DEFAULT 5,
		commentInterval INT(11) NOT NULL DEFAULT 10,
		followInterval INT(11) NOT NULL DEFAULT 5,		
		unfollowInterval INT(11) NOT NULL DEFAULT 5,
		restInterval INT(11) NOT NULL DEFAULT 30,
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database instagram_account';
	}
	$sql = "CREATE TABLE instagram_activity(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		activity VARCHAR(50) NOT NULL DEFAULT '',
		done TINYINT(1) NOT NULL DEFAULT 0,
		runAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database instagram_activity';
	}
	$sql = "CREATE TABLE instagram_activity_log(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		activity VARCHAR(50) NOT NULL DEFAULT '',
		done TINYINT(1) NOT NULL DEFAULT 0,
		runAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
		nextRun DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database instagram_activity_log';
	}	
	$sql = "INSERT INTO settings(type,value) VALUES('instagramReset',CURRENT_TIMESTAMP())";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();	
	$sql = "CREATE TABLE instagram_status(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		category VARCHAR(255) NOT NULL DEFAULT '',
		language VARCHAR(25) NOT NULL DEFAULT '',
		text TEXT UNIQUE NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database instagram_status';
	}	
	$arrLanguage = array(
		array('category'=>'thesimlife','language'=>'id','text'=>'Dapatkan penghasilan sampingan dari aplikasi, cek link dibio untuk download'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Mau cari dimana lagi program yang membayar?, download aplikasinya dilink bio'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Buat usaha virtual tanpa modal, cuan ngalir! langsung aja cek bio kita kak'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Buka usaha virtual bisa dapat cuan lebih? yuk cek aja aplikasinya di bio kita'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Cari penghasilan tambahan dari aplikasi? Rapatkan barisan ke link di bio kita'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Kapan lagi bisa belajar bisnis sambil dibayar? Link ada di bio'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Sudah saatnya mencari tambahan passive income dengan membuka usaha virtual di TheSimlife! Gratisss.. Cek BIO!'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Mau tau gimana cara dapat penghasilan tambahan? bisa coba cek bio kita kak, aplikasinya gratis!'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Cek bio kita untuk kalian yang lagi cari tambahan cuan dengan cara gratis!'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Usaha virtual bisa modal gratisan?? Bisa cuan juga? Gas download aja di bio link kita'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Mau tau cara cepat cuan? Biar dikit-dikit yang penting terus bayar lho.. Link ada di bio'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Bingung usaha yang ga pake modal? Kita ada aplikasinya nih, biar diawal dapet dikit. Tapi seiring waktu berjalan bakal nambah terus guys! Coba aja deh cek link bio kita'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Jangan liat hasilnya sekarang, pohon aja dari kecil dulu. Ya begitulah dengan pendapatan kita! Yuk cek bio kita guys'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Rebahan bisa sambil cuan cari dimana lagi! Gas aja cek bio kita'),
		array('category'=>'thesimlife','language'=>'id','text'=>'Puluhan ribu orang udah mencoba, yakin mau lewatin kesempatan ini? Cek aja bio kita'),		
	);
	//inserting data
	$bind = '';
	$params = array();
	$query = array();
	foreach($arrLanguage as $arr){
		$bind .= 'sss';
		$params[] = $arr['category'];
		$params[] = $arr['language'];
		$params[] = $arr['text'];
		$query[] = "(?,?,?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO instagram_status(category,language,text) VALUES $query";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();
	//inserting instagram comment
	$sql = "CREATE TABLE instagram_comment(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		category VARCHAR(255) NOT NULL DEFAULT '',
		language VARCHAR(25) NOT NULL DEFAULT '',
		text TEXT UNIQUE NOT NULL DEFAULT '',
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database instagram_comment';
	}		
	$arrLanguage = array(
		array('category'=>'general','language'=>'id','text'=>'ok kak..'),
		array('category'=>'general','language'=>'id','text'=>'aku merasakanmu'),
		array('category'=>'general','language'=>'id','text'=>'pengen kenalan'),
		array('category'=>'general','language'=>'id','text'=>'sip..'),
		array('category'=>'general','language'=>'id','text'=>'sip deh'),
		array('category'=>'general','language'=>'id','text'=>'okein aja'),
		array('category'=>'general','language'=>'id','text'=>'ya kali'),
		array('category'=>'general','language'=>'id','text'=>'coba aja hihi'),
		array('category'=>'general','language'=>'id','text'=>'haha'),
		array('category'=>'general','language'=>'id','text'=>'hehe'),
		array('category'=>'general','language'=>'id','text'=>'pasti bisa'),
		array('category'=>'general','language'=>'id','text'=>'cobain ah'),
		array('category'=>'general','language'=>'id','text'=>'pengen nyoba ah'),
		array('category'=>'general','language'=>'id','text'=>'pengen nyoba'),
		array('category'=>'general','language'=>'id','text'=>'kadang-kadang ah'),
		array('category'=>'general','language'=>'id','text'=>'sabarin aja'),
		array('category'=>'general','language'=>'id','text'=>'mencoba sabar'),
		array('category'=>'general','language'=>'id','text'=>'memang sulit sih..'),
		array('category'=>'general','language'=>'id','text'=>'aku pun gitu'),
		array('category'=>'general','language'=>'id','text'=>'harus bisa'),
		array('category'=>'general','language'=>'id','text'=>'harusin aja..'),
	);
	//inserting data
	$bind = '';
	$params = array();
	$query = array();
	foreach($arrLanguage as $arr){
		$bind .= 'sss';
		$params[] = $arr['category'];
		$params[] = $arr['language'];
		$params[] = $arr['text'];
		$query[] = "(?,?,?)";
	}
	array_unshift($params,$bind);
	$params = $tool->refValues($params);
	$query = implode(',',$query);
	$sql = "INSERT INTO instagram_comment(category,language,text) VALUES $query";
	$process = $conn->prepare($sql);
	call_user_func_array(array($process,'bind_param'),$params);
	$process->execute();
	$process->close();		
	$sql = "CREATE TABLE posted_instagram_image(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) NOT NULL DEFAULT '',
		filename VARCHAR(255) NOT NULL DEFAULT '',
		posted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'gagal membuat database posted_instagram_image';
	}	
	//add server
	$sql = "ALTER TABLE facebook_account ADD COLUMN server INT(11) NOT NULL DEFAULT 1 after password";
	if(!$process=$conn->query($sql)){
		$arrError[] = 'alter table facebook_account';
	}	
	//reset account
	$botFacebook = new botFacebook();
	$botFacebook->resetAccount();
	//add rest table
	$sql = "CREATE TABLE instagram_temp_banned(
		id INT(11) PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100) UNIQUE NOT NULL DEFAULT '',
		tries INT(11) NOT NULL DEFAULT 0,
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = "create table instagram_temp_banned";
	}
	$version = "1.0.8";
}
else if($version=="1.0.8"){
	$sql = "CREATE TABLE rumahku_profile(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		url VARCHAR(255) UNIQUE NOT NULL DEFAULT '',
		rendered TINYINT(1) NOT NULL DEFAULT 0,
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = "create table rumahku_profile";
	}
	//inserting max page to go
	$sql = "INSERT INTO settings(type,value) VALUES('rumahkuMax',100)";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();
	//inserting current page
	$sql = "INSERT INTO settings(type,value) VALUES('rumahkuCurrent',0)";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();
	//inserting rumah.com
	$sql = "INSERT INTO settings(type,value) VALUES('rumahcomCurrent',0)";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();
	//to create dotproperty url
	$sql = "CREATE TABLE dotproperty_url(
		id INT(11) AUTO_INCREMENT PRIMARY KEY,
		url VARCHAR(255) UNIQUE NOT NULL DEFAULT '',
		rendered TINYINT(1) NOT NULL DEFAULT 0,
		waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP()
	)";
	if(!$process=$conn->query($sql)){
		$arrError[] = "create table dotproperty_url";
	}	
	//inserting dotproperty.id
	$sql = "INSERT INTO settings(type,value) VALUES('dotpropertyCurrent',0)";
	$process = $conn->prepare($sql);
	$process->execute();
	$process->close();
	$version = "1.0.9";
}

if(count($arrError) > 0){
	foreach($arrError as $value){
		echo '<p>'.$value.'</p>';
	}
}
else{
	$sql = "UPDATE settings SET value=? WHERE type='version'";
	$process = $conn->prepare($sql);
	$process->bind_param('s',$version);
	$process->execute();
	$process->close();
	echo 'berhasil melakukan update '.$version;
}
?>