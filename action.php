<?php


$arg1 = $argv[1];
$arg2 = $argv[2];
if(strtolower($arg1) == 'truncate') {
    echo 'Truncating table "search"...'.PHP_EOL;
    mysql_connect('localhost', 'root', '');
    mysql_select_db('search') or die('DB ERROR');
    $show_results = mysql_query("TRUNCATE table `search`");
    $mysql = mysql_error();
    if(isset($mysql) && $mysql != '') {
        echo 'MySQL Message: '.$mysql.PHP_EOL;
    }

    die('Task accomplished successfully.'.PHP_EOL);

} elseif(strtolower($arg1) == 'check') {
    $url = $arg2;
    mysql_connect('localhost', 'root', '');
    mysql_select_db('search') or die('DB ERROR');
    $show_results = mysql_query("SELECT * FROM search WHERE url LIKE '".mysql_real_escape_string($url)."'");
    $number = mysql_numrows($show_results);
    if($number == '0') {
        echo 'out';
    } else {
        echo 'in';
    }
    echo mysql_error();
    die();
}
echo 'Nothing to do.'.PHP_EOL;

?>