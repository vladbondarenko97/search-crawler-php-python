<?php
$url = trim(base64_decode($argv[1]));
$title = trim(base64_decode($argv[2]));
$desc = trim(base64_decode(base64_decode(file_get_contents($argv[3]))));
$rank = $argv[4];

if(!is_numeric($rank)) {
    die('Rank Error');
}

if(strtolower(substr($url, 0, 4)) != 'http') die('2');

if($desc == '') die('2');

$title = substr($title, 0, 128);
$desc = preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $desc);
$title = preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $title);

if(strpos($url, '#') !== false) {
    $url = explode('#', $url);
    $url = $url[0];
}

mysql_connect('localhost', 'root', '');
mysql_select_db('search') or die('DB ERROR');
$show_results = mysql_query("SELECT * FROM search WHERE url LIKE '".mysql_real_escape_string($url)."'");
$number = mysql_numrows($show_results);
$i = 0;
if($number == 0) {
        $add_results = mysql_query("INSERT INTO search VALUES ('','".mysql_real_escape_string($url)."', '".htmlentities(mysql_real_escape_string($title))."', '".htmlentities(mysql_real_escape_string($desc))."', '0', '".$rank."')");
        echo '1';
} else {
        echo '2';
}
echo mysql_error();
mysql_close();
?>