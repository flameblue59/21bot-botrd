<?php
use JonnyW\PhantomJs\Client;
class getValue{
	public $arrPhone = array('0811','0812','0813','0814','0815','0816','0817','0818','0819','0820','0821','0822','0823','0828','0831','0832','0833','0838','0851','0852','0853','0855','0856','0857','0858','0859','0877','0878','0881','0882','0883','0884','0885','0886','0887','0888','0899','0895','0896','0897','0898','0899');
	function settings($type){
		global $conn;
		$value = '';
		$sql = "SELECT value FROM settings WHERE type=?";
		$process = $conn->prepare($sql);
		$process->bind_param('s',$type);
		$process->bind_result($value);
		$process->execute();
		$process->store_result();
		if($process->num_rows > 0){
			$process->fetch();
		}
		$process->close();
		return $value;
	}
	function account(
		Array $arrData = [],
		$arrField = array(
			'id'=>'id',
			'email'=>'email',
			'tries'=>'tries',
			'password'=>'password',
			'waktu'=>'waktu'
		)
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$waktu = $tool->getTime("Y-m-d H:i:s",'');
		$status = 'active';
		$order = "ORDER BY waktu ASC";
		$identifier = 'id';
		$group = '';
		$arrResult = array();
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		//bind param
		$bind = 's';
		$params = array();
		$query = array();
		$arrJson = array();
		$field = $arrField;
		$arrFilter = array('email','password');
		foreach($arrFilter as $value){
			if(ISSET(${$value})){
				$bind .= 's';
				$params[] = ${$value};
				$query[] = "$value=?";
			}
		}
		if(count($params) > 0){
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = "WHERE ".implode(' and ',$query);
		}
		else{
			$query = '';
		}
		//get pinterest list
		$queryResult = implode(',',$field);
		$sql = "SELECT $queryResult FROM banned_account $query $group $order";
		$process = $conn->prepare($sql);
		if(count($params) > 0){
			call_user_func_array(array($process,'bind_param'),$params);
		}
		$process->execute();
		$process->store_result();
		if($process->num_rows > 0){
			$result = array();
			$meta = $process->result_metadata();
			while($field = $meta->fetch_field()){
				$result[] = &$row[$field->name];
			}
			call_user_func_array(array($process,'bind_result'),$result);
			while($process->fetch()){
				$arr = array();
				foreach($arrField as $type=>$value){
					$arr[$type] = $row[$type];
					if(in_array($type,$arrJson)){
						$arr[$type] = json_decode($row[$type],true);
					}
				}
				$arrResult[$row[$identifier]] = $arr;
			}
		}
		$process->close();
		return $arrResult;
	}
	function facebookAccount(
		Array $arrData = [],
		$arrField = array(
			'id'=>'id',
			'email'=>'email',
			'password'=>'password',
			'server'=>'server',
			'proxy'=>'proxy',
			'likes'=>'likes',
			'maxLikes'=>'maxLikes',
			'comment'=>'comment',
			'maxComment'=>'maxComment',
			'addFriend'=>'addFriend',
			'maxAddFriend'=>'maxAddFriend',
			'confirmFriend'=>'confirmFriend',
			'unFriend'=>'unFriend',
			'maxUnFriend'=>'maxUnFriend',
			'maxConfirmFriend'=>'maxConfirmFriend',
			'profileWalk'=>'profileWalk',
			'maxProfileWalk'=>'maxProfileWalk',
			'profilePostStatus'=>'profilePostStatus',
			'maxProfilePostStatus'=>'maxProfilePostStatus',
			'profilePostPhoto'=>'profilePostPhoto',
			'maxProfilePostPhoto'=>'maxProfilePostPhoto',
			'groupInvite'=>'groupInvite',
			'maxGroupInvite'=>'maxGroupInvite',
			'groupPostStatus'=>'groupPostStatus',
			'maxGroupPostStatus'=>'maxGroupPostStatus',
			'groupPostPhoto'=>'groupPostPhoto',
			'maxGroupPostPhoto'=>'maxGroupPostPhoto',
			'likeInterval'=>'likeInterval',
			'commentInterval'=>'commentInterval',
			'addFriendInterval'=>'addFriendInterval',
			'confirmFriendInterval'=>'confirmFriendInterval',
			'unFriendInterval'=>'unFriendInterval',
			'profileWalkInterval'=>'profileWalkInterval',
			'groupInviteInterval'=>'groupInviteInterval',
			'profilePostInterval'=>'profilePostInterval',
			'groupPostInterval'=>'groupPostInterval',
			'restInterval'=>'restInterval',
			'nextRun'=>'nextRun',
			'waktu'=>'waktu'
		)
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$waktu = $tool->getTime("Y-m-d H:i:s",'');
		$order = "ORDER BY waktu ASC";
		$identifier = 'id';
		$group = '';
		$arrResult = array();
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		//bind param
		$bind = '';
		$params = array();
		$query = array();
		$arrJson = array();
		$field = $arrField;
		$arrFilter = array('email','password','server','proxy');
		foreach($arrFilter as $value){
			if(ISSET(${$value})){
				$bind .= 's';
				$params[] = ${$value};
				$query[] = "$value=?";
			}
		}
		if(count($params) > 0){
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = "WHERE ".implode(' and ',$query);
		}
		else{
			$query = '';
		}
		//get pinterest list
		$queryResult = implode(',',$field);
		$sql = "SELECT $queryResult FROM facebook_account $query $group $order";
		$process = $conn->prepare($sql);
		if(count($params) > 0){
			call_user_func_array(array($process,'bind_param'),$params);
		}
		$process->execute();
		$process->store_result();
		if($process->num_rows > 0){
			$result = array();
			$meta = $process->result_metadata();
			while($field = $meta->fetch_field()){
				$result[] = &$row[$field->name];
			}
			call_user_func_array(array($process,'bind_result'),$result);
			while($process->fetch()){
				$arr = array();
				foreach($arrField as $type=>$value){
					$arr[$type] = $row[$type];
					if(in_array($type,$arrJson)){
						$arr[$type] = json_decode($row[$type],true);
					}
				}
				$arrResult[$row[$identifier]] = $arr;
			}
		}
		$process->close();
		return $arrResult;
	}	
	function instagramAccount(
		Array $arrData = [],
		$arrField = array(
			'id'=>'id',
			'email'=>'email',
			'password'=>'password',
			'proxy'=>'proxy',
			'post'=>'post',
			'maxPost'=>'maxPost',
			'likes'=>'likes',
			'maxLikes'=>'maxLikes',
			'comment'=>'comment',
			'maxComment'=>'maxComment',
			'follow'=>'follow',
			'maxFollow'=>'maxFollow',
			'unfollow'=>'unfollow',
			'maxUnfollow'=>'maxUnfollow',
			'postInterval'=>'postInterval',
			'likeInterval'=>'likeInterval',
			'commentInterval'=>'commentInterval',
			'followInterval'=>'followInterval',
			'unfollowInterval'=>'unfollowInterval',
			'restInterval'=>'restInterval',
			'nextRun'=>'nextRun',
			'waktu'=>'waktu'
		)
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$waktu = $tool->getTime("Y-m-d H:i:s",'');
		$order = "ORDER BY waktu ASC";
		$identifier = 'id';
		$group = '';
		$arrResult = array();
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		//bind param
		$bind = 's';
		$params = array();
		$query = array();
		$arrJson = array();
		$field = $arrField;
		$arrFilter = array('email','password','proxy');
		foreach($arrFilter as $value){
			if(ISSET(${$value})){
				$bind .= 's';
				$params[] = ${$value};
				$query[] = "$value=?";
			}
		}
		if(count($params) > 0){
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = "WHERE ".implode(' and ',$query);
		}
		else{
			$query = '';
		}
		//get pinterest list
		$queryResult = implode(',',$field);
		$sql = "SELECT $queryResult FROM instagram_account $query $group $order";
		$process = $conn->prepare($sql);
		if(count($params) > 0){
			call_user_func_array(array($process,'bind_param'),$params);
		}
		$process->execute();
		$process->store_result();
		if($process->num_rows > 0){
			$result = array();
			$meta = $process->result_metadata();
			while($field = $meta->fetch_field()){
				$result[] = &$row[$field->name];
			}
			call_user_func_array(array($process,'bind_result'),$result);
			while($process->fetch()){
				$arr = array();
				foreach($arrField as $type=>$value){
					$arr[$type] = $row[$type];
					if(in_array($type,$arrJson)){
						$arr[$type] = json_decode($row[$type],true);
					}
				}
				$arrResult[$row[$identifier]] = $arr;
			}
		}
		$process->close();
		return $arrResult;
	}		
}

class bot{
	/* unsed
		'163.198.89.93:3128',
	*/
	public $listProxy = array(
		"155.94.232.163:3128",
		"192.126.215.216:3128",
		"104.223.48.26:3128",
		"192.126.214.82:3128",
		"192.126.215.34:3128",
		"192.126.214.23:3128",
		"155.94.232.25:3128",
		"155.94.232.190:3128",
		"155.94.232.242:3128",
		"104.223.48.23:3128",
		"166.88.110.155:3128",
		"198.55.110.230:3128",
		"198.55.110.245:3128",
		"166.88.110.196:3128",
		"166.88.110.159:3128",
		"166.88.110.5:3128",
		"107.150.0.226:3128",
		"107.150.0.24:3128",
		"50.118.222.70:3128",
		"50.118.222.217:3128",
		"192.126.153.221:3128",
		"104.140.209.154:3128",
		"81.16.128.114:3128",
		"81.16.128.73:3128",
		"81.16.128.84:3128",
		"104.140.209.35:3128",
		"192.126.153.73:3128",
		"81.16.128.123:3128",
		"173.232.7.3:3128",
		"173.232.7.235:3128",
		"192.126.199.50:3128",
		"23.229.72.75:3128",
		"5.253.117.146:3128",
		"198.20.188.21:3128",
		"147.78.52.188:3128",
		"147.78.52.62:3128",
		"5.253.117.9:3128",
		"23.229.72.22:3128",
		"192.126.197.234:3128",
		"91.132.248.172:3128",
		"86.62.56.13:3128",
		"147.78.52.21:3128",
		"198.20.188.218:3128",
		"91.132.248.141:3128",
		"50.31.106.89:3128",
		"91.132.248.143:3128",
		"91.132.248.175:3128",
		"86.62.56.184:3128",
		"23.229.72.74:3128",
		"5.253.117.237:3128",
		"192.126.197.102:3128",
		"192.126.197.32:3128",
		"192.126.199.26:3128",
		"91.132.248.98:3128",
		"192.126.199.107:3128",
		"5.253.117.194:3128",
		"147.78.52.9:3128",
		"50.31.106.103:3128",
		"50.31.106.28:3128",
		"23.19.97.19:3128",
		"23.19.97.255:3128",
		"198.20.188.161:3128",
		"23.229.72.25:3128",
		"5.253.117.211:3128",
		"23.19.97.140:3128",
		"86.62.56.180:3128",
		"86.62.56.78:3128",
		"23.229.72.205:3128",
		"86.62.56.243:3128",
		"192.126.197.174:3128",
		"147.78.52.83:3128",
		"192.126.197.254:3128",
		"50.31.106.1:3128",
		"198.20.188.216:3128",
		"50.31.106.64:3128",
		"23.19.97.1:3128",
		"192.126.199.106:3128",
		"192.126.199.30:3128",
		"23.19.97.205:3128",
		"198.20.188.54:3128"
	);
	public $listAgent = array(
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
		'Mozilla/5.0 Windows/537.36 Gecko/20100101 Firefox/75.0',
		'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'
	);
	function work($job){
		global $conn;
		//get job
		if(empty($job)){
			$rand = rand(0,100);
			if($rand <= 100){
				$job = "grabUrl";
			}
			else{
				$job = "idle";
			}
		}
		//set grab url for this time
		if($job=="grabUrl"){
			$activity = $this->grabUrl('');
		}
		else if($job=="processUrl"){
			$activity = $this->processUrl('');
		}
		else if($job=="idle"){
			$activity = "Sedang istirahat.. ".$rand;
		}
		funcstatus('success','berhasil memproses',array('activity'=>$activity));
	}
	function runGeneral(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');
		$command = "$pyCommand $localhostPath"."general/getGeneralNumber.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		$body = 'Selesai: '.$output;
		$script = "<script>
		setTimeout(function(){
			window.location.reload();
			setTimeout(function(){
				window.location.reload();
			},300000);
		},3000);
		</script>";
		echo $body.$script;
	}
	function grabUrl($arrData){
		global $conn;
		$tool = new tool();
		$arrUrl = array();
		$waktu = $this->getTime("Y-m-d H:i:s",'');
		$msg = "";
		$arrPhone = array();
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		/*
		//check get target
		$count = 0;
		if(ISSET($_COOKIE['grabError'])){
			$count = $_COOKIE['grabError'];
		}
		$count++;
		setCookie('grabError',$count,time()+3600*24*365,'/');
		//check grab target
		if($count > 2){
			$field = array('securityKey'=>$securityKey,'grabId'=>$id);
			$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=setTarget','post'=>true,'field'=>$field));		
		}
		*/
		//get target
		$getValue = new getValue();
		$securityKey = $getValue->settings('securityKey');
		$cookie = dirname(__FILE__).'/cookie.txt';
		$field = array('securityKey'=>$securityKey,'category'=>'property');
		if(!ISSET($debug)){
			$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=getTarget&rand='.rand(0,999),'post'=>true,'field'=>$field));
			if(!ISSET($curl['object'])){
				return '<script>
				setTimeout(function(){
					window.location.reload();
					setTimeout(function(){
						window.location.reload();
					},600000);
				},10000);
			</script>
				kesalahan load curl getTarget #1 ('.$tool->safeJsonEncode($curl).')';
			}
			$object = $curl['object'];
			if($curl['status']=="reset"){
				$field = array('securityKey'=>$securityKey);
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=resetGrab&rand='.rand(0,999),'post'=>true,'field'=>$field));
				return $curl['notification'];
			}
			else if($curl['status']=="failed"){
				//get rumahku (prop: 1000001);
				if(!ISSET($_COOKIE['rumahku'])){
					setCookie('rumahku',0,time()+3600*24*365*10,'/');
					return 'set cookie rumahku';
				}
				$url = 'https://www.rumahku.com/backprocess/properties/contact/';
				$default = 1000000;
				$state = $_COOKIE['rumahku'];
				$state++;
				$default += $state;
				setCookie('rumahku',$state,time()+3600*24*365*10,'/');
				//default gvalue
				$id = 0;
				$mainUrl = $url.$default.'/';
				$page = 0;
				$site = 'rumahku.com';
				$type = 'rumah';
				$category = 'property';
			}
			else if($curl['status']=="success"){
				//set variable
				$id = $object['data']['id'];
				$mainUrl = $object['data']['url'];
				$page = $object['data']['page'];
				$site = $object['data']['site'];
				$type = $object['data']['type'];
				$category = $object['data']['category'];
			}
			//if page more than 1
			$rootUrl = $mainUrl;
			if($page > 1){
				if($site=="rumahdijual.com"){
					$rootUrl = $mainUrl.'index'.$page.'.html';
				}
				else if($site=="rumah.com"){
					$rootUrl = $mainUrl.'/'.$page.'?order=desc&sort=date';
				}
				else if($site=="rumahhokie.com"){
					$rootUrl = $mainUrl.'/'.$page;
				}
				else if($site=="99.co"){
					$rootUrl = $mainUrl.'&hlmn='.$page;
				}
				else if($site=="brighton.co.id" || $site=="dotproperty.id"){
					$rootUrl = $mainUrl.'&page='.$page;
				}
				else{
					$rootUrl = $mainUrl.'?page='.$page;
				}
			}
		}
		//get proxy
		$listProxy = $this->listProxy;
		$proxy = $listProxy[rand(0,count($listProxy)-1)];
		$arrAgent = $this->listAgent;
		if(ISSET($debug)){
			$rootUrl = $renderUrl;
			$site = $renderSite;
		}
		$opt = array('url'=>$rootUrl,'plain'=>true,'timeout'=>60,'userAgent'=>$arrAgent[array_rand($arrAgent)]);
		//for debug purpose
		if(!ISSET($debug)){
			$opt['proxy'] = $proxy;
		}
		//to read cookie
		if($site=='rumah.com'){
			$curl = $tool->phantomJs($opt);
		}
		else if($site=='rumahku.com'){
			$opt['proxy'] = $proxy;
			$opt['referrer'] = 'https://www.rumahku.com';
			$opt['origin'] = 'rumahku.com';
			$opt['cookie'] = $_SERVER["DOCUMENT_ROOT"].'/botrd/rumahku.txt';
			$curl = $tool->curl($opt);
		}
		else if($site=='dotproperty.id'){
			$opt['referrer'] = 'https://dotproperty.id';
			$opt['origin'] = 'dotproperty.id';
			$opt['cookie'] = $_SERVER["DOCUMENT_ROOT"].'/botrd/dotproperty.txt';
			//$opt['proxy'] = '23.19.97.19:3128';
			$curl = $tool->curl($opt);
		}
		else{
			$curl = $tool->curl($opt);
		}
		if($curl['status']=='failed'){
			return 'Terjadi kesalahan dalam render ('.$rootUrl.')';
		}
		//load curl
		$html = new simple_html_dom();
		$html->load($curl['data']);
		$data = $curl['data'];
		//function for rumahdijual
		if($site=="rumahdijual.com"){
			foreach($html->find('b[class=title_usable] a') as $element){
				$url = $element->href;
				if(stripos($url,'http')===false){
					$url = 'https://'.$site.$url;
				}
				$arrUrl[$url] = '';
			}
			foreach($html->find('span[class=title_usable] a') as $element){
				$url = $element->href;
				if(stripos($url,'http')===false){
					$url = 'https://'.$site.$url;
				}
				$arrUrl[$url] = '';
			}
			$arrUrl = array_keys($arrUrl);
			$this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
			return 'berhasil render rumahdijual.com'.count($arrUrl).' url ('.$rootUrl.')';
		}
		//function for olx
		else if($site=="olx.co.id"){
			$arrPhone = array();
			/*
			foreach($html->find('button[class=phone]') as $element){
				$handphone = $element->attr['data-phone'];
				$handphone = str_replace('+','',$handphone);
				$handphone = $tool->compilePhone($handphone);
				if($phoneStatus = $tool->phoneValidation($handphone)){
					$arrPhone[$handphone] = $type;
				}
			}
			*/
			/* new version */
			foreach($html->find('li[data-aut-id=itemBox] a') as $value){
				$arrUrl[] = 'https://www.olx.co.id'.$value->href;
			}
			if(count($arrUrl) > 0){
				$status = $this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
				if($status['status']=='failed'){
					return $status['notification'];
				}
				return $status['notification'].' url ('.$rootUrl.')';
			}
			else{
				return 'tidak ada url dirender '.count($arrUrl).' url ('.$rootUrl.')';
			}
		}
		//function dotproperty.id
		else if($site=="dotproperty.id"){
			foreach($html->find('.search-list .left-block a') as $elements){
				$arrUrl[] = $elements->href;
			}
			if(count($arrUrl) > 0){
				$this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
			}
			return 'berhasil render '.count($arrUrl).' url ('.$rootUrl.')';
		}
		//function for raywhite
		else if($site=="raywhite.co.id"){
			foreach($html->find('div[class=card] a') as $value){
			    $url = $value->href;
			    if(stripos($url,'/properti/')!==false){
					$arrUrl[] = $value->href;
				}
			}
			if(count($arrUrl) > 0){
				$this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
			}
			return 'berhasil render '.count($arrUrl).' url ('.$rootUrl.')';
		}
		else if($site=="brighton.co.id"){
			$arrPhone = array();
			foreach($html->find('a[class=fbq_track_lead][href*=tel:]') as $elements){
				$handphone = $elements->href;
				$handphone = str_replace('tel:','',$handphone);
				$handphone = str_replace(' ','',$handphone);
				$handphone = str_replace('+','',$handphone);
				//if multiple number
				if(stripos($handphone,'/')!==false){
					$handphone = explode('/',$handphone);
					foreach($handphone as $value){
						$value = $tool->compilePhone($value);
						if($phoneStatus = $tool->phoneValidation($value)){
							$arrPhone[$value] = $type;
						}
					}
				}
				else{
					$handphone = $tool->compilePhone($handphone);
					if($phoneStatus = $tool->phoneValidation($handphone)){
						$arrPhone[$handphone] = $type;
					}
				}
			}
		}
		//function rumah.com
		else if($site=="rumah.com"){
			$arrPhone = array();
			foreach($html->find('a.phone-call-action-tracking') as $element){
				$handphone = $element->href;
				$handphone = str_replace('tel:','',$handphone);
				$handphone = str_replace(' ','',$handphone);
				$handphone = str_replace('+','',$handphone);
				$handphone = $tool->compilePhone($handphone);
				if($phoneStatus = $tool->phoneValidation($handphone)){
					$arrPhone[$handphone] = $type;
				}
			}
		}
		//function for rumah123
		else if($site=="rumah123.com"){
			$arrPhone = array();
			$scripts = $html->find('script');
			foreach($scripts as $key=>$s) {
				if(strpos($s->innertext, '"label":"handphone"') !== false) {
					if(preg_match_all('({"number":"\+[0-9]+)',$s->innertext,$match)){
						foreach($match[0] as $key=>$handphone){
							$handphone = str_replace('{"number":"','',$handphone);
							$handphone = str_replace('+6262','+62',$handphone);
							$handphone = str_replace('+','',$handphone);
							echo $handphone;
							$handphone = $tool->compilePhone($handphone);
							if($phoneStatus = $tool->phoneValidation($handphone)){
								$arrPhone[$handphone] = $type;
							}
						}
					}
				}
			}
		}
		else if($site=="99.co"){
			$arrPhone = array();
			//it will detect each button
			foreach($html->find('a[id=button-wa]') as $element){
				$url = $element->href;
				if(preg_match('(phone=[0-9]+)',$url,$match)){
					$handphone = str_replace('phone=','',$match[0]);
					$handphone = $tool->compilePhone($handphone);
					if($phoneStatus = $tool->phoneValidation($handphone)){
						$arrPhone[$handphone] = $type;
					}
				}
			}
		}
		else if($site=="rumahku.com"){
			$arrPhone = array();
			//it will detect each button
			foreach($html->find('.contact-number a') as $element){
				$handphone = $element->plaintext;
				$handphone = $tool->compilePhone($handphone);
				if($phoneStatus = $tool->phoneValidation($handphone)){
					$arrPhone[$handphone] = $type;
				}
			}
		}
		else if($site=="lamudi.co.id"){
			foreach($html->find('a[class=js-listing-link]') as $elements){
				$arrUrl[$elements->href.'/request-phone'] = '';
			}
			$arrUrl = array_keys($arrUrl);
			if(count($arrUrl) > 0){
				$this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
			}
			return 'berhasil render '.count($arrUrl).' url ('.$rootUrl.')';
		}
		else if($site=="rumahhokie.com"){
			foreach($html->find('.item-entry a') as $elements){
				$arrUrl[$elements->href] = '';
			}
			$arrUrl = array_keys($arrUrl);
			if(count($arrUrl) > 0){
				$this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
			}
			return 'berhasil render '.count($arrUrl).' url ('.$rootUrl.')';
		}
		else if($site=="jualo.com"){
			foreach($html->find('.product-item a') as $elements){
				$url = $elements->href;
				if(filter_var($url,FILTER_VALIDATE_URL)){
					$arrUrl[$url] = '';
				}
			}
			$arrUrl = array_keys($arrUrl);
			if(count($arrUrl) > 0){
				$this->submitUrl(array('grabId'=>$id,'source'=>$site,'arrUrl'=>$arrUrl,'category'=>$category,'subCategory'=>$type));
			}
			return 'berhasil render '.count($arrUrl).' url ('.$rootUrl.')';
		}
		if(ISSET($debug)){
			print_r($arrPhone);
			return;
		}
		//for checking phone number
		if(count($arrPhone) > 0){
			foreach($arrPhone as $handphone=>$type){
				if(!is_numeric($handphone) & strlen($handphone) < 9){
					unset($arrPhone[$handphone]);
				}
			}
		}
		else{
			return 'Tidak ada nomor untuk ditambahkan (Step #'.$count.')- '.$rootUrl.'-'.str_word_count($html);
		}
		//insert number
		$obj = $this->submit(array('grabId'=>$id,'username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return $obj['notification'].' (<a href="'.$rootUrl.'">'.$rootUrl.'</a>) #'.$proxy;
	}
	//When we have done getting url from olx then send data to server including its profile
	function sendUrl(
		Array $arrData = []
	){
		global $conn;
		$tool = new tool();
		$arrUrl = array();
		$waktu = $this->getTime("Y-m-d H:i:s",'');
		$arrPhone = array();
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		$getValue = new getValue();		
		$pyCommand = $getValue->settings('pyCommand');
		//get url
		$securityKey = $getValue->settings('securityKey');
		$field = array('securityKey'=>$securityKey,'category'=>'property');
		$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=getTarget','post'=>true,'field'=>$field));
		if($curl['status']=="reset"){
			$field = array('securityKey'=>$securityKey);
			$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=resetGrab&rand='.rand(0,999),'post'=>true,'field'=>$field));
			return $curl['notification'];
		}
		else if($curl['status']=='failed'){
			return $curl['notification'];
		}
		$object = $curl['object']['data'];
		//define root url
		$id = $object['id'];
		$rootUrl = $object['url'].'?page='.$object['page'];
		$rootUrl = $tool->safeJsonEncode($rootUrl);
		$site = $object['site'];
		$category = $object['category'];
		$type = $object['type'];
		//run script
		$localhostPath = $getValue->settings('localhostPath');
		$command = "$pyCommand $localhostPath"."url-grabber/run.py $rootUrl";
		$command = escapeshellcmd($command);		
		$output = shell_exec($command);
		$output = trim($output);
		//convert String json into array
		$arrUrl = json_decode($output,true);
		if(!is_array($arrUrl)){
			return $output;
		}
		//rendering output
		if(count($arrUrl) > 0){
			$status = $this->submitUrlProfile($id,$site,$arrUrl,$category,$type);
			if($status['status']=='failed'){
				return $status['notification'];
			}
			return $status['notification'].' url ('.$rootUrl.')';
		}
		else{
			return 'tidak ada url dirender '.count($arrUrl).' url ('.$rootUrl.')';
		}
	}
	function processUrl($arrData){
		global $conn;
		$tool = new tool();
		$debug = false;
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		$cookie = dirname(__FILE__).'/cookie.txt';
		$getValue = new getValue();		
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		//get target
		$securityKey = $getValue->settings('securityKey');
		$cookie = dirname(__FILE__).'/cookie.txt';
		$field = array('securityKey'=>$securityKey);
		if(!$debug){
			$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=getUrl&rand='.rand(0,999),'timeout'=>10,'post'=>true,'field'=>$field));
			if(!ISSET($curl['object'])){
				return 'terjadi kesalahan getUrl beyondlimit.co';
			}
			if(!is_array($curl['object'])){
				return 'kesalahan array getUrl beyondlimit.co';
			}
			$object = $curl['object'];
			if(!ISSET($object['data'])){
				return 'tidak ada url untuk diproses';
			}
			$object = $object['data'];
		}
		//tries
		setCookie('tries',true,time()+3600*24*360,'/');
		$tries = 1;
		if(ISSET($_COOKIE['tries'])){
			$tries = $_COOKIE['tries'];
		}
		$tries++;
		setCookie('tries',$tries,time()+3600*24*360,'/');
		//set phone array
		$arrPhone = array();
		//get proxy
		$listProxy = $this->listProxy;
		$proxy = $listProxy[rand(0,count($listProxy)-1)];
		//get platform
		$os = $tool->getOs();
		//get agent
		$arrAgent = $this->listAgent;
		if($debug){
			if(!ISSET($urlList)){
				$object['url'] = $renderUrl;
			}
			else{
				$object['url'] = 'https://google.com';
			}
			$object['source'] = $renderSite;
			$object['category'] = $category;
			$object['subCategory'] = $subCategory;
		}
		$opt = array('url'=>$object['url'],'plain'=>true,'timeout'=>60,'userAgent'=>$arrAgent[array_rand($arrAgent)]);
		//read cookie (special site!)
		if($object['source']=='lamudi.co.id'){
			$field = array('request_phone[phone_input]'=>'+6281122334455','request_phone[email_address]'=>'caca@gmail.com');
		    $opt['post'] = true;
		    $opt['field'] = $field;
			$opt['cookieRead'] = $_SERVER["DOCUMENT_ROOT"].'/botrd/lamudi.txt';
			$opt['referrer'] = 'https://www.lamudi.co.id/apartment/buy/';
		}
		else if($object['source']=='dotproperty.id'){
			$opt['referrer'] = 'https://dotproperty.id';
			$opt['origin'] = 'dotproperty.id';
			$opt['cookie'] = $_SERVER["DOCUMENT_ROOT"].'/botrd/dotproperty.txt';
			$curl = $tool->curl($opt);		
		}
		if(!$debug){
			$opt['proxy'] = $proxy;
		}
		//pick whether modern or old curl
		if($object['source']=='olx.co.id'){
			$urlList = array_slice($urlList,0,5); //for TEST PURPOSE
			$count = count($urlList);
			$dataUrl = json_encode(array_keys($urlList));
			if(!ISSET($noproxy)){
				$account = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=olx'));
			}
			else{
				//account with no proxy
				$account = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=olxNoProxy'));
				$path = "$pyCommand $localhostPath"."grabber/new.py";
			}
			echo '<script>
				setTimeout(function(){
					window.location.reload();
					setTimeout(function(){
						window.location.reload();
					},600000);
				},10000);
			</script>';
			if($account['status']=='failed'){
				return array('status'=>'failed','notification'=>'account error: '.$account['notification']);
			}
			$account = json_decode($account['object']['data'],true);
			$username = $account['email'];
			$password = $account['password'];
			if(!empty($account['proxy'])){
				$proxy = $account['proxy'];
			}

			//$password = "123";
			//$proxy = "163.198.89.93:3128"; //debugging
			$command = "$path $dataUrl $count $username $password $proxy";
			$command = escapeshellcmd($command);
			try{
				$output = shell_exec($command);
				$output = trim($output);
				if(stripos($output,'banned')!==false){
					$objStatus = explode('=>',$output);
					$status = $objStatus[0];
					$account = $objStatus[1];
					//when status 'banned' then add account
					if($status=="banned"){
						$sql = "INSERT INTO banned_account(email) VALUES(?) ON DUPLICATE KEY UPDATE tries=tries+1";
						$process = $conn->prepare($sql);
						$process->bind_param('s',$account);
						$process->execute();
						$process->close();
					}
					return array('status'=>'failed','notification'=>'banned terkirim: '.$account);
				}
				if(empty($output)){
					return array('status'=>'failed','notification'=>'tidak ada output');
				}						
			}
			catch(Exception $e){
				return array('status'=>'failed','notification'=>'python script'.$e);
			}
			$output = json_decode($output, true);
  			if(is_array($output) && count($output)==0){
  				return array('status'=>'failed','notification'=>'Tidak ada nomor ditemukan');
  			}	
  			else if(!is_array($output)){
  				return array('status'=>'failed','notification'=>'output error: '.$output);
  			}
			//to spoof only
			$curl = array();
			$curl['data'] = $tool->getTime("Y-m-d H:i:s",'').'Menggunakan render chrome (OLX)';
		}
		else{
			$curl = $tool->curl($opt);
		}
		if(empty($curl['data'])){
			if(ISSET($_COOKIE['tries']) && $_COOKIE['tries'] > 3){
				setCookie('tries',null,-1,'/');
				//remove from url
				$field = array('url'=>$object['url']);
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=deleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
				return 'url ('.$object['url'].') otomatis dihapus lantaran sudah gagal sebanyak 3x';
			}
			return 'terjadi kesalahan dom #'.$tries.' ('.$object['url'].' #'.$proxy.')';
		}
		$html = new simple_html_dom();
		$html->load($curl['data']);
		if($object['source']=="olx.co.id"){
			foreach($output as $id=>$arr){
				$handphone = str_replace('+','',$arr['telnumber']);
				$handphone = $tool->compilePhone($handphone);
				if($tool->phoneValidation($handphone)){
					$categoryVal = $urlList[$arr['website']]['subCategory'];
					$arrPhone[trim($handphone)] = $categoryVal;
				}			
			}
			if(count($arrPhone) > 0){
				$obj = $this->submit(array('grabId'=>'','username'=>'harold','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		else if($object['source']=="dotproperty.id"){
			$element = $html->find('input[name=number]',0);
			$handphone = $element->value;
			$handphone = preg_replace('/\s+/', '',$handphone);
 			$handphone = preg_replace("/[^0-9]/", "",$handphone);
			$handphone = $tool->compilePhone($handphone);
			$arrPhone[$handphone] = $object['subCategory'];
			if(count($arrPhone) > 0 && $phoneStatus = $tool->phoneValidation($handphone)){
				$obj = $this->submit(array('grabId'=>'','username'=>'harold','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		else if($object['source']=="rumahdijual.com"){
			$element = $html->find('span[class=nohp]',0);
			$handphone = $element->plaintext;
			//for sym
			$arrCheck = explode('[',$handphone);
			if(strlen($arrCheck[0]) >= 11){
				$handphone = $arrCheck[0];
			}
			//for (sym)
			$arrCheck = explode('(',$handphone);
			if(strlen($arrCheck[0]) >= 11){
				$handphone = $arrCheck[0];
			}		
			//for space
			$arrCheck = explode(' ',$handphone);
			if(strlen($arrCheck[0]) >= 11){
				$handphone = $arrCheck[0];
			}
			//for hypen
			$arrCheck = explode('-',$handphone);
			if(strlen($arrCheck[0]) >= 11){
				$handphone = $arrCheck[0];
			}
			$arrReplace = array(
				0=>'nol',
				1=>'satu',
				2=>'dua',
				3=>'tiga',
				4=>'empat',
				5=>'lima',
				6=>'enam',
				7=>'tujuh',
				8=>'delapan',
				9=>'sembilan'
			);
			foreach($arrReplace as $number=>$val){
				$handphone = str_replace($val,$number,$handphone);
			}
			$handphone = str_replace("l",'1',$handphone);
			$handphone = str_replace("I",'1',$handphone);
			$handphone = str_replace("o",'0',$handphone);
			$handphone = str_replace("O",'0',$handphone);
			$handphone = preg_replace('/\s+/', '',$handphone);
 			$handphone = preg_replace("/[^0-9]/", "",$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[$handphone] = $object['subCategory'];
			}
			//get handphone from content if empty
			$context = '';
			foreach($html->find(".alt1") as $elements){
				$context .= $elements->plaintext;
			}
			preg_match_all('/\+?(?:[ -]?\d+)+|(\d+)(?:[ -]\d+)/', $context, $matches);
			$matches = $matches[0];
			foreach($matches as $value){
				$value = str_replace("l",'1',$value);
				$value = str_replace("I",'1',$value);
				$value = str_replace("o",'0',$value);
				$value = str_replace("O",'0',$value);
				$value = preg_replace('/\s+/', '',$value);
				$value = preg_replace("/[^0-9]/", "",$value);
				$value = $tool->compilePhone($value);
				if($tool->phoneValidation($value)){
					$arrPhone[$tool->compilePhone($value)] = $object['subCategory'];
				}
			}
			if(count($arrPhone) > 0){
				$obj = $this->submit(array('grabId'=>'','username'=>'harold','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		else if($object['source']=="raywhite.co.id"){
			foreach($html->find('a[class=wa-marketing]') as $elements){
				$handphone = $elements->plaintext;
				$handphone = preg_replace('/\s+/', '',$handphone);
 				$handphone = preg_replace("/[^0-9]/", "",$handphone);
				$handphone = $tool->compilePhone($handphone);
				if($phoneStatus = $tool->phoneValidation($handphone)){
					$arrPhone[$handphone] = $object['subCategory'];
				}
			}
			if(count($arrPhone) > 0){
				$obj = $this->submit(array('grabId'=>'','username'=>'harold','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		else if($object['source']=="lamudi.co.id"){
			$params = json_decode($curl['data'],true);
			if(ISSET($params['mobilePhone'])){
				$handphone = $params['mobilePhone'];
				$handphone = preg_replace('/\s+/', '',$handphone);
				$handphone = preg_replace("/[^0-9]/", "",$handphone);
				$handphone = str_replace('+','',$handphone);
				$handphone = $tool->compilePhone($handphone);
			}
			if($phoneStatus = $tool->phoneValidation($handphone)){
				$arrPhone[$handphone] = $object['subCategory'];
			}
			if(count($arrPhone) > 0){
				$obj = $this->submit(array('grabId'=>'','username'=>'lamudi','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		else if($object['source']=="rumahhokie.com"){
			foreach($html->find('ul[class=dealer-contacts] li a') as $elements){
				$handphone = $elements->plaintext;
				$handphone = preg_replace('/\s+/', '',$handphone);
 				$handphone = preg_replace("/[^0-9]/", "",$handphone);
 				$handphone = str_replace('+','',$handphone);
				$handphone = $tool->compilePhone($handphone);
				if($phoneStatus = $tool->phoneValidation($handphone)){
					$arrPhone[$handphone] = $object['subCategory'];
				}
			}
			if(count($arrPhone) > 0){
				$obj = $this->submit(array('grabId'=>'','username'=>'rumahhokie','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		else if($object['source']=="jualo.com"){
			foreach($html->find('input[id=abuse_report_ad_id]') as $elements){
				$id = $elements->value;
			}
			//read only whatsapp
			if(ISSET($html->find('.contact-seller-whatsapp',0)->plaintext)){
				$contactType = 'whatsapp';
				$urlRender = 'https://jualo.com/iklan/'.$id.'/get_seller_phone_number?contact_type='.$contactType;
				$curl = $tool->curl(array('url'=>$urlRender,'proxy'=>$proxy,'timeout'=>60,'userAgent'=>$arrAgent[array_rand($arrAgent)]));
				if(!ISSET($curl['object']['contact_url'])){
					$curl = $tool->curl(array('url'=>$urlRender,'proxy'=>$proxy,'timeout'=>60,'userAgent'=>$arrAgent[array_rand($arrAgent)]));
				}
				if(ISSET($curl['object']['contact_url'])){
					$obj = $curl['object']['contact_url'];
					$obj = explode('?',$obj);
					$handphone = str_replace('https://wa.me/','',$obj[0]);
					$handphone = preg_replace('/\s+/', '',$handphone);
					$handphone = preg_replace("/[^0-9]/", "",$handphone);
					$handphone = str_replace('+','',$handphone);
					$handphone = $tool->compilePhone($handphone);
					if($phoneStatus = $tool->phoneValidation($handphone)){
						$arrPhone[$handphone] = $object['subCategory'];
					}
				}
			}
			if(count($arrPhone) > 0){
				$obj = $this->submit(array('grabId'=>'','username'=>'jualo','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			}
		}
		//for debug
		if($debug){
			echo $html;
		}
		if(!empty($obj['notification'])){
			setCookie('tries',null,-1,'/');
			//remove from url
			if(!ISSET($urlList)){
				$field = array('url'=>$object['url']);
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=deleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}
			else{
				$field = array('securityKey'=>$securityKey,'data'=>$tool->safeJsonEncode(array_keys($urlList)));
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=bulkDeleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}

		}
		if(count($arrPhone) > 0){
			if(!ISSET($obj['notification'])){
				$obj['notification'] = 'Tidak ada notif '.implode(',',$arrPhone);
			}
			return $obj['notification'].' (<a href="'.$object['url'].'">'.$object['url'].'</a>) #'.$proxy.' ['.implode(',',array_keys($arrPhone)).']';
		}
		else{
			//remove from url
			if(!ISSET($urlList)){
				$field = array('url'=>$object['url']);
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=deleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}
			else{
				$field = array('data'=>$tool->safeJsonEncode(array_keys($urlList)));
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=bulkDeleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}
			return 'tidak menemukan nomor (<a href="'.$object['url'].'">'.$object['url'].'</a>) #'.$proxy;
		}
	}
	//its for v2 and v3 only
	function processOlx(
		String $version,
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$debug = false;
		
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		//get url list
		if(!ISSET($urlList)){
			$object['url'] = $renderUrl;
		}
		else{
			$object['url'] = 'https://google.com';
		}
		$object['source'] = $renderSite;
		$object['category'] = $category;
		$object['subCategory'] = $subCategory;
		//do initialization
		if($version=="v3"){
			$filePath = "$pyCommand $localhostPath"."grabber/newv3.py";
		}
		else{
			$filePath = "$pyCommand $localhostPath"."grabber/newv2.py";
		}
		$urlList = array_slice($urlList,0,5); //for TEST PURPOSE
		//convert into
		$result = array();
		foreach($urlList as $id=>$arr){
			$result[$arr['profileUid']] = $arr['url'];
		}
		$dataUrl = json_encode($result);
		$dataUrl = str_replace('"','\"',$dataUrl);
		$command = "$filePath $dataUrl";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		if(empty($output)){
			return 'data kosong';
		}
		$result = explode('==>',$output);
		if(!ISSET($result[1])){
			return 'kesalahan data: '.$result[0];
		}
		$result = $result[1];
		$result = json_decode($result, true);
		  if(is_array($result) && count($result)==0){
			  return 'Tidak ada nomor ditemukan';
		  }
		  else if(empty($result)){
			  return 'tidak ada output';
		  }			
		  else if(!is_array($result)){
			  return 'output error: '.$result;
		  }
		foreach($result as $id=>$arr){
			$handphone = str_replace('+','',$arr['telnumber']);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$categoryVal = $urlList[$arr['website']]['subCategory'];
				$arrPhone[trim($handphone)] = $categoryVal;
			}			
		}
		if(count($arrPhone) > 0){
			$obj = $this->submit(array('grabId'=>'','username'=>'harold','category'=>$object['category'],'type'=>$object['subCategory'],'source'=>$object['source'],'handphone'=>$arrPhone,'silent'=>true));
			//inserting uid from $result
			$bind = '';
			$params = array();
			$query = array();
			foreach($result as $arr){
				$handphone = str_replace('+','',$arr['telnumber']);
				$handphone = $tool->compilePhone($handphone);
				$bind .= 'sss';
				$params[] = $arr['name'];
				$params[] = $arr['uid'];
				$params[] = $handphone;
				$query[] = "(?,?,?)";
			}
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = implode(',',$query);
			//inserting data
			$sql = "INSERT INTO olx_rendered_uid(name,profileUid,nomor) VALUES $query ON DUPLICATE KEY UPDATE nomor=VALUES(nomor)";
			$process = $conn->prepare($sql);
			call_user_func_array(array($process,'bind_param'),$params);
			$process->execute();
			$process->close();
		}
		//define securityKey
		$getValue = new getValue();
		$securityKey = $getValue->settings('securityKey');		
		if(!empty($obj['notification'])){
			setCookie('tries',null,-1,'/');
			//remove from url
			if(!ISSET($urlList)){
				$field = array('url'=>$object['url']);
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=deleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}
			else{
				$field = array('securityKey'=>$securityKey,'data'=>$tool->safeJsonEncode(array_keys($urlList)));
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=bulkDeleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}

		}
		if(count($arrPhone) > 0){
			if(!ISSET($obj['notification'])){
				$obj['notification'] = 'Tidak ada notif '.implode(',',$arrPhone);
			}
			$waktu = $tool->getTime("Y-m-d H:i:s",'');
			return '['.$waktu.'] '.$obj['notification'].' (<a href="'.$object['url'].'">'.$object['url'].'</a>) # ['.implode(',',array_keys($arrPhone)).']';
		}
		else{
			//remove from url
			if(!ISSET($urlList)){
				$field = array('url'=>$object['url']);
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=deleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}
			else{
				$field = array('data'=>$tool->safeJsonEncode(array_keys($urlList)));
				$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=bulkDeleteUrl&rand='.rand(0,999),'post'=>true,'field'=>$field));
			}
			return 'tidak menemukan nomor (<a href="'.$object['url'].'">'.$object['url'].'</a>)';
		}
	}	
	function submit($arrData){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$securityKey = $getValue->settings('securityKey');
		$silent = false;
		if(!is_array($arrData)){
			$required = array('category','handphone');
			foreach($required as $value){
				if(empty($_POST[$value])){
					if(!$silent){
						funcstatus('failed',getstr('emptyfield',array($value)),'');
					}
					else{
						return 'field '.$value.' tidak lengkap';
					}
					return;
				}
				${$value} = $_POST[$value];
			}
		}
		else{
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		$cookie = dirname(__FILE__).'/cookie.txt';
		$field = array('securityKey'=>$securityKey,'category'=>$category,'source'=>$source,'input'=>json_encode($handphone));
		if(ISSET($grabId)){
			$field['grabId'] = $grabId;
		}
		$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=addNumber','post'=>true,'field'=>$field));
		return array('status'=>$curl['status'],'notification'=>$curl['notification']);
	}
	function submitUrl($arrData){
		$tool = new tool();
		$cookie = dirname(__FILE__).'/cookie.txt';
		$getValue = new getValue();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$securityKey = $getValue->settings('securityKey');
		$field = array('grabId'=>$grabId,'securityKey'=>$securityKey,'source'=>$source,'url'=>json_encode($arrUrl),'category'=>$category,'subCategory'=>$subCategory);
		$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=addUrl','post'=>true,'field'=>$field));
		return array('status'=>$curl['status'],'notification'=>$curl['notification']);
	}
	function submitUrlProfile(
		String $grabId,
		String $source,
		Array $arrUrl,
		String $category,
		String $subCategory,
		Array $arrData = []
	){
		$tool = new tool();
		$getValue = new getValue();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$securityKey = $getValue->settings('securityKey');
		$field = array('grabId'=>$grabId,'securityKey'=>$securityKey,'source'=>$source,'url'=>json_encode($arrUrl),'category'=>$category,'subCategory'=>$subCategory);
		$curl = $tool->curl(array('url'=>'https://beyondlimit.co/api.php?f=addUrlProfile','post'=>true,'field'=>$field));
		return array('status'=>$curl['status'],'notification'=>$curl['notification']);
	}
	function getTime($type,$date){
		//do local first
		$cookie = $_SERVER["DOCUMENT_ROOT"].'/botrd/cookie.txt';
		$ch = curl_init();
		$waktu = date("Y-m-d H:i:s");
		$waktu = strtotime($waktu)+(3600*5);
		$waktu = date($type,$waktu);
		return $waktu;
		/*
		curl_setopt($ch,CURLOPT_URL,'https://rumahdaerah.com/api.php');
		curl_setopt($ch, CURLOPT_ENCODING, 'gzip');
		curl_setopt($ch,CURLOPT_COOKIESESSION,true);
		curl_setopt($ch,CURLOPT_COOKIEFILE,$cookie);
		curl_setopt($ch,CURLOPT_COOKIEJAR,$cookie);
		curl_setopt($ch,CURLOPT_AUTOREFERER,true);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
		curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
		curl_setopt($ch,CURLOPT_TIMEOUT,60);
		curl_setopt($ch,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13');
		curl_setopt($ch, CURLOPT_REFERER, 'http://www.google.com');
		curl_setopt($ch, CURLOPT_AUTOREFERER, true);
		$waktu = curl_exec($ch);
		if(empty($waktu)){
			getTime($type,$date);
			return;
		}
		$waktu = strtotime($waktu);
		$waktu = date($type,$waktu);
		return $waktu;
		*/
	}
	function settings($type){
		global $conn;
		$sql = "SELECT value FROM settings WHERE type=?";
		$process = $conn->prepare($sql);
		$process->bind_param('s',$type);
		$process->bind_result($value);
		$process->execute();
		$process->store_result();
		if($process->num_rows > 0){
			$process->fetch();
			return $value;
		}
	}
}

class botFacebook{
	function facebook(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		if(!ISSET($_GET['server'])){
			return array('status'=>'failed','notification'=>'harap isikan server');
		}
		//set server
		$server = $_GET['server'];
		//build activity
		$status = $this->buildDailyActivity($server);
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');
		$command = "$pyCommand $localhostPath"."facebook/facebook.py $server";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		$body = 'Selesai: '.$output;
		$script = "<script>
		setTimeout(function(){
			window.location.reload();
			setTimeout(function(){
				window.location.reload();
			},900000);
		},3000);
		</script>";
		$body .= '['.$status['notification'].']'.$script;
		return array('status'=>'success','notification'=>'bot facebook berjalan','callback'=>array('data'=>$body));
	}	
	function buildDailyActivity(
		String $server,
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$waktu = $tool->getTime("Y-m-d H:i:s",'');
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		//set facebookReset cron
		$type = 'facebookReset'.$server;
		//get facebook reset
		$facebookReset = $getValue->settings($type);
		if(empty($facebookReset)){
			$sql = "INSERT INTO settings(type,value) VALUES(?,?)";
			$process = $conn->prepare($sql);
			$process->bind_param('ss',$type,$waktu);
			$process->execute();
			$process->close();
			$facebookReset = $getValue->settings($type);			
		}
		else if($facebookReset > $waktu){
			return array('status'=>'failed','notification'=>'reset akan dilakukan pada '.$facebookReset);
		}
		$arrFacebook = $getValue->facebookAccount(array('server'=>$server));
		if(count($arrFacebook)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('akun')));
		}
		//reset user stats
		$sql = "UPDATE facebook_account SET 
			likes=0,
			comment=0,
			addFriend=0,
			confirmFriend=0,
			unFriend=0,
			profileWalk=0,
			profilePostStatus=0,
			profilePostPhoto=0,
			groupInvite=0,
			groupPostStatus=0,
			groupPostPhoto=0 WHERE server=?";
		$process = $conn->prepare($sql);
		$process->bind_param('i',$server);
		$process->execute();
		$process->close();
		//move facebook_activity to facebook_activity_log
		$sql = "INSERT INTO facebook_activity_log SELECT * FROM facebook_activity WHERE done=1";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		//truncating current activity
		$sql = "TRUNCATE facebook_activity";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		//building daily activity
		foreach($arrFacebook as $id=>$arr){
			$bind = '';
			$params = array();
			$query = array();
			$toBuild = array(
				'likes'=>'likeInterval',
				'comment'=>'commentInterval',
				'addFriend'=>'addFriendInterval',
				'confirmFriend'=>'confirmFriendInterval',
				'unFriend'=>'unFriendInterval',
				'profileWalk'=>'profileWalkInterval',
				'profilePostStatus'=>'profilePostInterval',
				'profilePostPhoto'=>'profilePostInterval',
				'groupInvite'=>'groupInviteInterval',
				'groupPostStatus'=>'groupPostInterval',
				'groupPostPhoto'=>'groupPostInterval'
			);
			//reset interval if exists
			foreach($toBuild as $activity=>$intervalField){
				unset(${$intervalField});
			}
			//define total activity
			$totalActivity = 0;
			foreach($toBuild as $activity=>$intervalField){
				$amount = $arr[$activity];
				$max = $arr['max'.ucwords($activity)];
				//effectiveness
				$effectiveness = rand(70,100);
				$max = floor($max*$effectiveness)/100;
				//set interval
				$interval = $arr[$intervalField];
				$lateInterval = $interval*2;
				//define setTime
				if(!ISSET(${$intervalField})){
					${$intervalField} = new DateTime($waktu);
					$eachActivityInterval = rand(30,60)*$totalActivity;
					${$intervalField}->modify('+'.$eachActivityInterval.' second'); //giving random [30-90 seconds]
				}
				$increment = 1;
				//define reduce increment [groupInvite could be randomly into 5]
				if($activity=='groupInvite') $increment = rand(3,5);
				//do looping
				while($amount < $max){
					$bind .= 'sss';
					$params[] = $arr['email'];
					$params[] = $activity;
					$params[] = ${$intervalField}->format("Y-m-d H:i:s");
					$query[] = "(?,?,?)";
					$amount += $increment;
					//modify next run
					$next = rand($interval,$lateInterval);
					${$intervalField}->modify("+$next minute");					
				}
				$totalActivity++;
			}
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = implode(',',$query);
			$sql = "INSERT INTO facebook_activity(email,activity,runAt) VALUES $query";
			$process = $conn->prepare($sql);
			call_user_func_array(array($process,'bind_param'),$params);
			$process->execute();
			$process->close();
		}
		//set nextReset
		$nextReset = new DateTime($waktu);
		$nextReset->setTime(0,0,0);		
		$nextReset->modify('+1 day');
		$nextReset = $nextReset->format("Y-m-d H:i:s");				
		//send facebook reset as done
		$sql = "UPDATE settings SET value=? WHERE type=?";
		$process = $conn->prepare($sql);
		$process->bind_param('ss',$nextReset,$type);
		$process->execute();
		$process->close();
		return array('status'=>'success','notification'=>getStr('strsend',array('build activity')));
	}
	//set globals
	function setInterval(
		Array $arrData = []
	){
		global $conn;
		$likeInterval = 3;
		$confirmFriendInterval = 3;
		$groupInviteInterval = 10;
		$profilePostInterval = 90;
		$groupPostInterval = 90;
		$sql = "ALTER TABLE facebook_account 
			CHANGE likeInterval likeInterval INT(11) NOT NULL DEFAULT $likeInterval,
			CHANGE confirmFriendInterval confirmFriendInterval INT(11) NOT NULL DEFAULT $confirmFriendInterval,
			CHANGE groupInviteInterval groupInviteInterval INT(11) NOT NULL DEFAULT $groupInviteInterval,
			CHANGE profilePostInterval profilePostInterval INT(11) NOT NULL DEFAULT $profilePostInterval,
			CHANGE groupPostInterval groupPostInterval INT(11) NOT NULL DEFAULT $groupPostInterval";
		if(!$process=$conn->query($sql)){
			$arrError[] = 'alter table facebook_account';
		}	
		$sql = "UPDATE facebook_account SET likeInterval=?,confirmFriendInterval=?,groupInviteInterval=?,profilePostInterval=?,groupPostInterval=?";
		$process = $conn->prepare($sql);
		$process->bind_param('iiiii',$likeInterval,$confirmFriendInterval,$groupInviteInterval,$profilePostInterval,$groupPostInterval);
		$process->execute();
		$process->close();
		return array('status'=>'success','notification'=>'set interval berhasil');
	}
	function resetAccount(
		Array $arrData = []
	){
		global $conn;
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$sql = "UPDATE facebook_account SET 
			maxLikes=40,
			maxComment=10,
			maxAddFriend=40,
			maxConfirmFriend=50,
			maxUnFriend=20,
			maxProfileWalk=20,
			maxProfilePostStatus=2,
			maxProfilePostPhoto=2,
			maxGroupInvite=100,
			maxGroupPostStatus=1";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		return array('status'=>'success','notification'=>'berhasil reset account Facebook');
	}
}

class botInstagram{
	function instagram(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		//build activity
		$status = $this->buildDailyActivity();
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');
		$command = "$pyCommand $localhostPath"."instagram/instagram.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		$body = 'Selesai: '.$output;
		$script = "<script>
		setTimeout(function(){
			window.location.reload();
			setTimeout(function(){
				window.location.reload();
			},900000);
		},3000);
		</script>";
		$body .= '['.$status['notification'].']';
		echo $body.$script;
	}	
	function buildDailyActivity(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$waktu = $tool->getTime("Y-m-d H:i:s",'');
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		//get facebook reset
		$instagramReset = $getValue->settings('instagramReset');
		if($instagramReset > $waktu){
			return array('status'=>'failed','notification'=>'reset akan dilakukan pada '.$instagramReset);
		}
		$arrInstagram = $getValue->instagramAccount();
		if(count($arrInstagram)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('akun')));
		}
		//reset user stats
		$sql = "UPDATE instagram_account SET 
			post=0,
			likes=0,
			comment=0,
			follow=0,
			unfollow=0
		";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		//move instagram_activity to instagram_activity_log
		$sql = "INSERT INTO instagram_activity_log SELECT * FROM instagram_activity_log WHERE done=1";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		//truncating temp banned
		$sql = "TRUNCATE instagram_temp_banned";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		//truncating current activity
		$sql = "TRUNCATE instagram_activity";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		//building daily activity
		foreach($arrInstagram as $id=>$arr){
			$bind = '';
			$params = array();
			$query = array();
			$toBuild = array(
				'post'=>'postInterval',
				'likes'=>'likeInterval',
				'comment'=>'commentInterval',
				'follow'=>'followInterval',
				'unfollow'=>'unfollowInterval',
			);
			//reset interval if exists
			foreach($toBuild as $activity=>$intervalField){
				unset(${$intervalField});
			}
			//define total activity
			$totalActivity = 0;
			foreach($toBuild as $activity=>$intervalField){
				$amount = $arr[$activity];
				$max = $arr['max'.ucwords($activity)];
				//effectiveness
				$effectiveness = rand(70,100);
				$max = floor($max*$effectiveness)/100;
				$interval = $arr[$intervalField];
				$lateInterval = $interval*2;
				//define setTime
				if(!ISSET(${$intervalField})){
					${$intervalField} = new DateTime($waktu);
					$eachActivityInterval = rand(30,60)*$totalActivity;
					${$intervalField}->modify('+'.$eachActivityInterval.' second'); //giving random [30-90 seconds]
				}
				while($amount < $max){
					$bind .= 'sss';
					$params[] = $arr['email'];
					$params[] = $activity;
					$params[] = ${$intervalField}->format("Y-m-d H:i:s");
					$query[] = "(?,?,?)";
					$amount++;
					//modify next run
					$next = rand($interval,$lateInterval);
					${$intervalField}->modify("+$next minute");					
				}
				$totalActivity++;
			}
			array_unshift($params,$bind);
			$params = $tool->refValues($params);
			$query = implode(',',$query);
			$sql = "INSERT INTO instagram_activity(email,activity,runAt) VALUES $query";
			$process = $conn->prepare($sql);
			call_user_func_array(array($process,'bind_param'),$params);
			$process->execute();
			$process->close();
		}
		//send instagram reset as done
		$nextReset = new DateTime($waktu);
		$nextReset->setTime(0,0,0);		
		$nextReset->modify('+1 day');
		$nextReset = $nextReset->format("Y-m-d H:i:s");
		$sql = "UPDATE settings SET value=? WHERE type='instagramReset'";
		$process = $conn->prepare($sql);
		$process->bind_param('s',$nextReset);
		$process->execute();
		$process->close();
		return array('status'=>'success','notification'=>getStr('strsend',array('build activity')));
	}
	function resetAccount(
		Array $arrData = []
	){
		global $conn;
		$sql = "UPDATE instagram_account SET 
		maxPost=1,
		maxLikes=10,
		maxComment=2,
		maxFollow=20,
		maxUnfollow=20";
		$process = $conn->prepare($sql);
		$process->execute();
		$process->close();
		return array('status'=>'success','notification'=>'berhasil reset account Instagram');		
	}
}

class botServer{
	function lamudi(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();		
		$bot = new bot();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$command = "$pyCommand $localhostPath"."lamudi/run.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		//convert String json into array
		$result = json_decode($output,true);
		if(!is_array($result)){
			return $output;
		}
		if(count($result)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('phone number')));
		}
		//define category
		$site = 'lamudi.co.id';
		$category = 'property';
		$type = 'rumah';
		$arrPhone = array();
		foreach($result as $rawPhone){
			$handphone = trim($rawPhone);
			$handphone = str_replace('+','',$handphone);
			$handphone = str_replace('-','',$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[trim($handphone)] = $type;
			}			
		}
		$obj = $bot->submit(array('username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return array('status'=>$obj['status'],'notification'=>$obj['notification']);
	}
	function rumah123(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();		
		$bot = new bot();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$command = "$pyCommand $localhostPath"."rumah123/run.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		//convert String json into array
		$result = json_decode($output,true);
		if(!is_array($result)){
			return $output;
		}
		if(count($result)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('phone number')));
		}
		//define category
		$site = 'rumah123.com';
		$category = 'property';
		$type = 'rumah';
		$arrPhone = array();
		foreach($result as $rawPhone){
			$handphone = trim($rawPhone);
			$handphone = str_replace('+','',$handphone);
			$handphone = str_replace('-','',$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[trim($handphone)] = $type;
			}			
		}
		$obj = $bot->submit(array('username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return array('status'=>$obj['status'],'notification'=>$obj['notification']);
	}	
	function rumahcom(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();		
		$bot = new bot();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$command = "$pyCommand $localhostPath"."rumahcom/run.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		//convert String json into array
		$result = json_decode($output,true);
		if(!is_array($result)){
			return $output;
		}
		if(count($result)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('phone number')));
		}
		//define category
		$site = 'rumah.com';
		$category = 'property';
		$type = 'rumah';
		$arrPhone = array();
		foreach($result as $rawPhone){
			$handphone = trim($rawPhone);
			$handphone = str_replace('+','',$handphone);
			$handphone = str_replace('-','',$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[trim($handphone)] = $type;
			}			
		}
		$obj = $bot->submit(array('username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return array('status'=>$obj['status'],'notification'=>$obj['notification']);
	}		
	function ninetynine(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();		
		$bot = new bot();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$command = "$pyCommand $localhostPath"."99/run.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = trim($output);
		//convert String json into array
		$result = json_decode($output,true);
		if(!is_array($result)){
			return $output;
		}
		if(count($result)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('phone number')));
		}
		//define category
		$site = '99.co';
		$category = 'property';
		$type = 'rumah';
		$arrPhone = array();
		foreach($result as $rawPhone){
			$handphone = trim($rawPhone);
			$handphone = str_replace('+','',$handphone);
			$handphone = str_replace('-','',$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[trim($handphone)] = $type;
			}			
		}
		$obj = $bot->submit(array('username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return array('status'=>$obj['status'],'notification'=>$obj['notification']);
	}	
	function rumahku(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();		
		$bot = new bot();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$command = "$pyCommand $localhostPath"."rumahku/run.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = explode('=>',$output)[1];
		$output = trim($output);
		//convert String json into array
		$result = json_decode($output,true);
		if(!is_array($result)){
			return $output;
		}
		if(count($result)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('phone number')));
		}
		//define category
		$site = 'rumahku';
		$category = 'property';
		$type = 'rumah';
		$arrPhone = array();
		foreach($result as $rawPhone){
			$handphone = trim($rawPhone);
			$handphone = str_replace('+','',$handphone);
			$handphone = str_replace('-','',$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[trim($handphone)] = $type;
			}			
		}
		$obj = $bot->submit(array('username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return array('status'=>$obj['status'],'notification'=>$obj['notification']);
	}		
	function dotproperty(
		Array $arrData = []
	){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();		
		$bot = new bot();
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		$pyCommand = $getValue->settings('pyCommand');
		$localhostPath = $getValue->settings('localhostPath');	
		$command = "$pyCommand $localhostPath"."dotproperty/run.py";
		$command = escapeshellcmd($command);
		$output = shell_exec($command);
		$output = explode('=>',$output)[1];
		$output = trim($output);
		//convert String json into array
		$result = json_decode($output,true);
		if(!is_array($result)){
			return $output;
		}
		if(count($result)==0){
			return array('status'=>'failed','notification'=>getStr('strnotfound',array('phone number')));
		}
		//define category
		$site = 'dotproperty';
		$category = 'property';
		$type = 'rumah';
		$arrPhone = array();
		foreach($result as $rawPhone){
			$handphone = trim($rawPhone);
			$handphone = str_replace('+','',$handphone);
			$handphone = str_replace('-','',$handphone);
			$handphone = $tool->compilePhone($handphone);
			if($tool->phoneValidation($handphone)){
				$arrPhone[trim($handphone)] = $type;
			}			
		}
		$obj = $bot->submit(array('username'=>'harold','category'=>$category,'type'=>$type,'source'=>$site,'handphone'=>$arrPhone,'silent'=>true));
		return array('status'=>$obj['status'],'notification'=>$obj['notification']);
	}					
}

class tool{
	function getOS() {
		if (DIRECTORY_SEPARATOR === '/') {
			$os = 'mac';
		}
		else if (DIRECTORY_SEPARATOR === '\\') {
			$os = 'windows';
		}
		return $os;
	}
	function variable($data){
		global $conn;
		$parameter = $GLOBALS['parameter'];
		$field = array('websiteName');
		foreach($field as $value){
			$data = str_replace('['.$value.']',$parameter[$value],$data);
		}
		return $data;
	}
	function convertDate($waktu){
		$waktu = new DateTime($waktu);
		$arrBulan = array('Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember');
		$date = $waktu->format('d').' '.$arrBulan[$waktu->format('n')-1].' '.$waktu->format('Y');
		return $date;
	}
	function convertTime($waktu){
		$data = '';
		$curTime = $this->getTime("Y-m-d H:i:s",'');
		$start = new DateTime($curTime);
		$end = $start->diff(new DateTime($waktu));
		$month = $end->m;
		$day = $end->d;
		$hour = $end->h;
		$minute = $end->i;
		$second = $end->s;
		if($day > 0 || $month > 0){
			$data = $this->convertDate($waktu);
		}
		else if($day==0 && $month==0){
			if($hour > 0){
				$data = $hour.' jam, '.$minute.' menit yang lalu';
			}
			else if($minute > 0 && empty($data)){
				$data = $minute.' menit yang lalu';
			}
			else if(empty($data)){
				$data = 'baru saja';
			}
		}
		return $data;
	}
	function phoneValidation($handphone){
		global $conn;
		$getValue = new getValue();
		$tool = new tool();
		$detect = false;
		$arrPhone = $getValue->arrPhone;
		//convert phone
		$handphone = $tool->decompilePhone($handphone);
		foreach($arrPhone as $value){
			if(stripos($handphone,$value)!==false){
				$pos = stripos($handphone,$value);
				if($pos==0){
					$detect = true;
				}
			}
		}
		//get length
		$jumlah = strlen($handphone);
		if($jumlah < 10 || $jumlah > 13){
			return false;
		}
		return $detect;
	}
	function getTime($type,$date){
		global $conn;
		$getValue = new getValue();
		if(empty($date)){
			$date = date("Y-m-d H:i:s");
			$date = strtotime($date);
			$difference = $getValue->settings('timeDelay')*3600;
			$date -= $difference;
			$date = date($type,$date);
		}
		else{
			$date = strtotime($date);
			$difference = $getValue->settings('timeDelay')*3600;
			$date -= $difference;
			$date = date($type,$date);
		}
		return $date;
	}
	function compilePhone($number){
		$phone = preg_replace('/^0/', '62', $number);
		return $phone;
	}
	function slug($text){
		$text = strtolower($text);
		$text = str_replace(' ', '-', $text); // Replaces all spaces with hyphens.
		$text = preg_replace('!-+!', '-', $text);
		$text = preg_replace('/[^A-Za-z0-9\-]/', '', $text); // Removes special chars.
		$text = str_replace('--','-',$text);
		return $text;
	}
	function reverseSlug($text){
		$text = strtolower($text);
		$text = str_replace('--','-',$text);
		$text = str_replace('-', ' ', $text); // Replaces all spaces with hyphens.
		$text = preg_replace('! +!', ' ', $text);
		return $text;
	}
	function decompilePhone($number){
		$phone = preg_replace('/^62/', '0', $number);
		return $phone;
	}
	function generateString($length) {
		$characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
		$charactersLength = strlen($characters);
		$randomString = '';
		for ($i = 0; $i < $length; $i++) {
			$randomString .= $characters[rand(0, $charactersLength - 1)];
		}
		return $randomString;
	}
	function generateStringOnly($length) {
		$characters = '123456789ABCDEFGHIJKLMNPQRSTUVWXYZ';
		$charactersLength = strlen($characters);
		$randomString = '';
		for ($i = 0; $i < $length; $i++) {
			$randomString .= $characters[rand(0, $charactersLength - 1)];
		}
		return $randomString;
	}
	function generateNumber($length) {
		$characters = '0123456789';
		$charactersLength = strlen($characters);
		$randomString = '';
		for ($i = 0; $i < $length; $i++) {
			$randomString .= $characters[rand(0, $charactersLength - 1)];
		}
		return $randomString;
	}
	function refValues($arr){
		if (strnatcmp(phpversion(),'5.3') >= 0) //Reference is required for PHP 5.3+
		{
			$refs = array();
			foreach($arr as $key => $value)
				$refs[$key] = &$arr[$key];
			return $refs;
		}
		return $arr;
	}
	function safeJsonEncode($value, $options = 0, $depth = 512, $utfErrorFlag = false) {
		$encoded = json_encode($value, $options, $depth);
		switch (json_last_error()) {
			case JSON_ERROR_NONE:
				return $encoded;
			case JSON_ERROR_DEPTH:
				return 'Maximum stack depth exceeded'; // or trigger_error() or throw new Exception()
			case JSON_ERROR_STATE_MISMATCH:
				return 'Underflow or the modes mismatch'; // or trigger_error() or throw new Exception()
			case JSON_ERROR_CTRL_CHAR:
				return 'Unexpected control character found';
			case JSON_ERROR_SYNTAX:
				return 'Syntax error, malformed JSON'; // or trigger_error() or throw new Exception()
			case JSON_ERROR_UTF8:
				$clean = $this->utf8ize($value);
				if ($utfErrorFlag) {
					return 'UTF8 encoding error'; // or trigger_error() or throw new Exception()
				}
				return $this->safeJsonEncode($clean, $options, $depth, true);
			default:
				return 'Unknown error'; // or trigger_error() or throw new Exception()

		}
	}
	function utf8ize($mixed) {
		if (is_array($mixed)) {
			foreach ($mixed as $key => $value) {
				$mixed[$key] = $this->utf8ize($value);
			}
		} else if (is_string ($mixed)) {
			return utf8_encode($mixed);
		}
		return $mixed;
	}
	function curl($arrData){
		global $conn;
		$encoding = 'gzip';
		$timeout = 20;
		$userAgent = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36';
		$cookie = dirname(__FILE__).'/cookie.txt';
		$referrer = 'https://google.com';
		$cookieRead = $cookie;
		foreach($arrData as $key=>$value){
			${$key} = $value;
		}
		try{
			$ch = curl_init();
			curl_setopt($ch,CURLOPT_URL,$url);
			if(ISSET($post)){
				curl_setopt($ch,CURLOPT_POST,1);
				curl_setopt($ch,CURLOPT_POSTFIELDS,$field);
			}
			if(ISSET($proxy)){
				$ip = $proxy;
				curl_setopt($ch, CURLOPT_PROXY, $proxy);
			}
			curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
			curl_setopt($ch,CURLOPT_FOLLOWLOCATION,1);
			curl_setopt($ch,CURLOPT_COOKIE,1);
			curl_setopt($ch,CURLOPT_COOKIEJAR,$cookie);
			curl_setopt($ch,CURLOPT_COOKIEFILE,$cookieRead);
			curl_setopt($ch,CURLOPT_HEADER,false);
			curl_setopt($ch,CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
			curl_setopt($ch,CURLOPT_ENCODING,$encoding);
			curl_setopt($ch,CURLOPT_USERAGENT,$userAgent);
			curl_setopt($ch,CURLOPT_REFERER,'https://www.rumahku.com/p/7YLJL019/rumah-dijual-bsd-city-tangerang-selatan-15310');
			curl_setopt($ch,CURLOPT_AUTOREFERER,true);
			curl_setopt($ch,CURLOPT_TIMEOUT,$timeout);
			$data = curl_exec($ch);
			if(curl_errno($ch)){
				$error = curl_error($ch);
				curl_close($ch);
				return array('status'=>'failed','notification'=>getStr('strinvalid',array($error.' ('.$url.')')),'data'=>$data);
				return;
			}
			else{
				$httpCode = curl_getinfo($ch,CURLINFO_HTTP_CODE);
				if($httpCode=="200"){
					if(!ISSET($plain)){
						$myObj = json_decode($data,true);
						if(!ISSET($myObj['notification'])){
							$myObj['notification'] = 'no notification, skip it';
						}
						if(json_last_error()===JSON_ERROR_NONE){
							return array('status'=>$myObj['status'],'notification'=>$myObj['notification'],'object'=>$myObj,'data'=>$data);
						}
						else{
							return array('status'=>'failed','notification'=>'Terjadi kesalahan json ('.$url.') ('.$data.')');
						}
					}
					else{
						return array('status'=>'success','notification'=>getStr('strsuccess',''),'data'=>$data);
					}
				}
				else{
					return array('status'=>'failed','notification'=>getStr('strinvalid',array('http kode '.$httpCode)),'callback'=>array('kode'=>$httpCode));
				}
			}
		}
		catch(Exception $e){
			return array('status'=>'failed','notification'=>$e);
		}
	}
	function modernCurl($arrData){
		global $conn;
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		$params = '';
		$field = array('url'=>$url);
		if(ISSET($proxy)){
			$field['proxy'] = $proxy;
		}
		foreach($field as $type=>$value){
			$params .= "&$type=$value";
		}
		$curl = $this->curl(array('url'=>'http://dijual.co.id/api.php?f=modernCurl&password=@bobby123@'.$params,'plain'=>true,'post'=>true,'field'=>$this->safeJsonEncode($field)));
		return array('status'=>'success','notification'=>getStr('strsuccess',''),'data'=>$curl['data']);
	}
	function phantomJs($arrData){
		global $conn;
		if(is_array($arrData)){
			foreach($arrData as $key=>$value){
				${$key} = $value;
			}
		}
		$apiKey = 'a-demo-key-with-low-quota-per-ip-address';
		//get key from storage
		$curl = $this->curl(array('url'=>'http://beyondlimit.co/api.php?f=getApi&password=@bobby123@&type=phantomjs'));
		if($curl['status']=='success'){
			$object = json_decode($curl['object']['data'],true);
			$apiKey = $object['data']['api'];
		}
		$mainUrl = 'http://PhantomJScloud.com/api/browser/v2/'.$apiKey.'/';
		$payload = array(
			'url'=>$url,
			'renderType'=>'html'
		);
		$payload = json_encode($payload);
		$options = array(
			'http' => array(
				'header'  => "Content-type: application/json\r\n",
				'method'  => 'POST',
				'content' => $payload
			)
		);
		$context  = stream_context_create($options);
		$result = file_get_contents($mainUrl, false, $context);
		if ($result === FALSE) {
			return array('status'=>'failed','notification'=>'kesalahan render data');
		}
		return array('status'=>'success','data'=>$result);
	}
}

function funcstatus($status,$string,$data){
	$myObj = new stdClass();
	if(empty($data)){
		$data = array();
	}
	if(count($data) > 0){
		foreach($data as $key=>$value){
			$myObj->{$key} = $value;
		}
	}
	$myObj->status = $status;
	$myObj->notification = $string;
	$myJson = json_encode($myObj);
	echo $myJson;
}
?>
