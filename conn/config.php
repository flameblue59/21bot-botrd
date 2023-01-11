<?php
$db_host = "localhost";
$db_username = "root";
$db_password = "";
$db_database = "bot_number";

$conn = new mysqli($db_host,$db_username,$db_password,$db_database);

if($conn->connect_errno){
	die('no connection');
}
?>