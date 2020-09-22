<?php
$db_server = "sophia.cs.hku.hk";
$db_user = "yxwang2";
$db_pwd = "19960201";
$conn = mysqli_connect($db_server, $db_user, $db_pwd, $db_user) or die(mysqli_error());

$keyword = (isset($_GET['keyword']) ? $_GET['keyword'] : "");


echo '{';
$category = array();
$names = array();
mysqli_query($conn,"SET NAMES 'utf8'");
$sql = "SELECT category, names from Tips WHERE names LIKE '%".$keyword."%' ORDER BY times DESC";
$res = mysqli_query($conn, $sql) or die(mysqli_error());
if (mysqli_num_rows($res) > 0) {
        while($row = mysqli_fetch_assoc($res)) {
                array_push($category, $row['category']);
                array_push($names, $row['names']);
        }
} else {
}
mysqli_query($conn,"SET NAMES 'utf8'");
$sql = "SELECT category, names from Tips WHERE category LIKE '%".$keyword."%' ORDER BY times DESC";
$res = mysqli_query($conn, $sql) or die(mysqli_error());
if (mysqli_num_rows($res) > 0) {
        while($row = mysqli_fetch_assoc($res)) {
                if(in_array($row['category'],$category)==False){
                        array_push($category, $row['category']);
                        array_push($names, $row['names']);
                }
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
echo ',"category":[';
        $add_delimiter = false;
        for ($i=0; $i<count($category); $i++) {
        echo ($add_delimiter ? ', ' : '') . '"' . $category[$i] . '"';
        $add_delimiter = true;
        }
        echo ']';
echo '}';
mysqli_close($conn);
?>
                                              
