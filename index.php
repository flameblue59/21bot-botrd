<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');
$vpassword = $_GET['password'];
$password = "stidaccom";
if($vpassword!=$password){
	header('Location: /');
}
$data = '<head>
		<link rel="stylesheet" href="https://rumahdaerah.com/lib/fontawesome/css/all.css" integrity="sha384-lKuwvrZot6UHsBSfcMvOkWwlCMgc0TaWr+30HWe3a4ltaBwTZhyTEggF5tJv8tbt" crossorigin="anonymous">
		<link rel="stylesheet" href="https://rumahdaerah.com/css/all.css" type="text/css"/>
		<script src="https://rumahdaerah.com/js/jquery-3.3.1.min.js"></script>
</head>';
$data .= '<div class="container"><div class="row"><h2 class="mainTitle">Halaman robot RumahDaerah.com</h2><div id="activity" class="boxActivity"> </div><button class="btn btn-primary m-2 ml-auto" id="btnBot">off</button></div>
<script>
var stateajax = false;
var robot = "off";
var chance = 25;
$(document).ready(function(){
	$("#btnBot").click(function(){
		nyalakanRobot("on");
	});
});

function nyalakanRobot(status){
	$("#btnBot").html(status);
	robot = status;
	var itvJob = setInterval(function(){
		var number = Math.floor(Math.random() * 100);
		if(number > chance){
			if(!stateajax){
				console.log("run");
				stateajax = true;
				$.ajax({
					url: "/botrd/core/bridge.php",
					type: "POST",
					cache: false,
					contentType: false,
					processData: false,
					success: function(result){
						stateajax = false;
						if(result.length > 0){
							var myObj = JSON.parse(result);
							var status = myObj.status;
							if(status=="success"){
								$("#activity").prepend(myObj.activity+"<br/>");
							}
							else{
								$("#activity").prepend("Terjadi sebuah kesalahan");
							}
							if($("#activity").text().length > 10000){
								$("#activity").html("");
							}
						}
					},
					error: function(result){
						stateajax = false;
						$("#activity").prepend("Tidak bisa membuka file");
					}
				});
			}
		}
	},1000);
}
</script>';
echo $data;
?>