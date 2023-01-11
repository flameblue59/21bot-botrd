<?php
function getStr($string,$arr){
	global $conn;
	$strsuccess = "Berhasil memproses permintaan";
	$strfailed = "Gagal memproses permintaan";
	$strused = "[value1] telah digunakan";
	$strprocess = "Berhasil memproses [value1]";
	$strnotprocess = "Tidak dapat memproses [value1]";
	$strcreate = "[value1] berhasil dibuat";
	$strsend = "[value1] berhasil dikirim";
	$strnotsend = "Gagal mengirimkan [value1]";
	$strchange = "[value1] berhasil dirubah";
	$strnotchange = "Gagal mengubah [value1]";
	$strinsert = "Berhasil menambahkan [value1]";
	$strnotinsert = "Gagal menambahkan [value1]";
	$strdelete = "[value1] berhasil dihapus";
	$strnotdelete = "Gagal menghapus [value1]";
	$strnotfound = "[value1] tidak ditemukan";
	$strnotmatch = "[value1] tidak sama";
	$strexists = "[value1] sudah ada";
	$strnotexists = "Tidak ada [value1]";
	$strmax = "[value1] mencapai batas maksimum, tidak bisa membuat lagi";
	$strduplicate = "[value1] duplikat, harap ganti dengan yang lain!";
	$strnotuploaded = "[value1] tidak terunggah";
	$struploaded = "[value1] terunggah";
	$strincorrect = "[value1] tidak benar";
	$strbonus = "Anda berhasil mendapatkan bonus top up sebesar Rp. [value1]";
	$strinvalid = "Isikan [value1] dengan benar";
	$strnotactivate = "[value1] belum diaktifasi";
	$strerror = "Kesalahan [value1]";
	$strbanned = "[value1] diblokir";
	$strregistered = "[value1] sudah terdaftar";
	$strlogin = "Berhasil masuk, selamat datang ([value1])";
	$strregister1 = "Pendaftaran email selesai, anda akan segera dialihkan ke halaman pendaftaran";
	$strregister2 = "Pendaftaran berhasil, anda akan segera login secara otomatis";
	$strlogout = "Berhasil keluar dari akun, sampai jumpa kembali!";
	$strregisterexist = "Email sudah terdaftar silahkan login";
	$strregisterdone = "Email sudah terdaftar namun belum teraktifasi, anda akan segera dialihkan ke halaman pendaftaran";
	//general
	$noaccess = "Anda tidak memiliki access";
	$emptyfield = "Harap isikan ([value1])";
	$strreset = "Berhasil mereset [value1]";
	$strresetfailed = "Tidak ada [value1] untuk direset";
	//bid
	$bidlow = "Bid terlalu rendah, min [value1]";
	//form
	$strnumber = "[value1] harus berupa numerik/angka";
	$strlong = "[value1] terlalu panjang (maks [value2] karakter), tambahkanlah beberapa kata";
	$strshort = "[value1] terlalu pendek (min [value2] karakter), kurangilah beberapa kata";
	$strsearch = "Berhasil menemukan [value1] [value2], membangun data..";
	$strnotsearch = "Tidak menemukan hasil, cobalah mencari lebih luas";
	$stryoutube = "Video harus dari Youtube";
	$strnocapital = "Penggunaan huruf capital berlebihan pada [value1], buatlah sebagaimana mestinya!";
	$strbelow = "[value1] kurang dari [value2]";
	//contact
	$strmessagesend = "Pesan berhasil terkirim ke penjual, anda akan segera dihubungi dalam waktu dekat";
	//processing string
	$string = ${$string};
	if(is_array($arr)){
		foreach($arr as $key=>$value){
			$key++;
			$string = str_replace('[value'.$key.']',$value,$string);
		}
	}
	return $string;
}
?>