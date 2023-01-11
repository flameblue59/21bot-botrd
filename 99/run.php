<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$botServer = new botServer();
$body = '<script>
setTimeout(function(){
    window.location.reload();
    setTimeout(function(){
        window.location.reload();
    },600000);
},3000);
</script>';
$status = $botServer->rumahcom();
if(!is_array($status)){
    die($status);
}
echo $body.$status['notification'];
?>