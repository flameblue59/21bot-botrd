<?php
require_once($_SERVER["DOCUMENT_ROOT"].'/botrd/core/header.php');
$getValue = new getValue();
$tool = new tool();
$arrAccount = $getValue->account(array('identifier'=>'email'));
if(count($arrAccount) > 0){
    $arrAccount = array_keys($arrAccount);
    echo $tool->safeJsonEncode($arrAccount);
}
else{
    echo 'tidak ada akun terbanned';
}
?>