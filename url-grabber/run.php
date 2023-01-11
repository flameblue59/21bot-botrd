<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');

$bot = new bot();
$body = '<script>
setTimeout(function(){
    window.location.reload();
    setTimeout(function(){
        window.location.reload();
    },300000);
},3000);
</script>';
$status = $bot->sendUrl();
echo $body.$status;
?>