<?php
$db_server = "sophia.cs.hku.hk";
$db_user = "yxwang2";
$db_pwd = "19960201";
$conn = mysqli_connect($db_server, $db_user, $db_pwd, $db_user) or die(mysqli_error());

$keyword = (isset($_GET['keyword']) ? $_GET['keyword'] : "");

echo '{';
mysqli_query($conn,"SET NAMES 'utf8'");
$sql = "SELECT * from Objects WHERE name='".$keyword."'";
$res = mysqli_query($conn, $sql) or die(mysqli_error());

if (mysqli_num_rows($res) > 0) {
	echo '"status":"detail"';
	while($row = mysqli_fetch_assoc($res)) {
		echo ',"cid":' . $row['cid'];
		$times=$row['times']+1;
		$sql = "UPDATE Objects SET times=".$times." WHERE name='".$row['name']."'";
		mysqli_query($conn, $sql);

	}
} else {
	echo '"status":"fuzzy"';
}

echo '}';
mysqli_close($conn);
?>