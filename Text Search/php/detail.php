<?php
$db_server = "sophia.cs.hku.hk";
$db_user = "yxwang2";
$db_pwd = "19960201";
$conn = mysqli_connect($db_server, $db_user, $db_pwd, $db_user) or die(mysqli_error());

$category = (isset($_GET['c']) ? $_GET['c'] : "");

echo '{';
mysqli_query($conn,"SET NAMES 'utf8'");
$sql = "SELECT carry_on, checked, detail, times from Tips WHERE category='".$category."'";
$res = mysqli_query($conn, $sql) or die(mysqli_error());

if (mysqli_num_rows($res) > 0) {
	while($row = mysqli_fetch_assoc($res)) {
		echo '"carry_on":' . $row['carry_on'];
		echo ', "checked":' . $row['checked'];
		echo ', "detail":"' . $row['detail'] . '"';
		$times=$row['times']+1;
		$sql = "UPDATE Tips SET times=".$times." WHERE category='".$category."'";
		mysqli_query($conn, $sql);
	}
} else {
}

echo '}';
mysqli_close($conn);
?>