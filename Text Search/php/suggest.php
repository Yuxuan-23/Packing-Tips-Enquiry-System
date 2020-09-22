<?php
$db_server = "sophia.cs.hku.hk";
$db_user = "yxwang2";
$db_pwd = "19960201";
$conn = mysqli_connect($db_server, $db_user, $db_pwd, $db_user) or die(mysqli_error());

$pre = (isset($_GET['pre']) ? $_GET['pre'] : "");


echo '{';
$names = array();
mysqli_query($conn,"SET NAMES 'utf8'");
$sql = "SELECT name FROM Objects WHERE name LIKE '".$pre."%' ORDER BY times DESC";
$res = mysqli_query($conn, $sql) or die(mysqli_error());
if (mysqli_num_rows($res) > 0) {
	while($row = mysqli_fetch_assoc($res)) {
		array_push($names, $row['name']);
	}
} else {
	
}
echo '"name":[';
$add_delimiter = false;
for ($i=0; $i<count($names); $i++) {
echo ($add_delimiter ? ', ' : '') . '"' . $names[$i] . '"';
$add_delimiter = true;
}
echo ']';

echo '}';
mysqli_close($conn);
?>