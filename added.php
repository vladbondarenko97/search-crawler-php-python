<?php
mysql_connect('localhost', 'root', '');
mysql_select_db('search') or die('DB ERROR');
$show_results = mysql_query("SELECT * FROM search");
$number = mysql_numrows($show_results);
$i=0;
while($i<$number) {
    $url = mysql_result($show_results, $i, 'url');
    echo $url.PHP_EOL;
    $i++;
}
?>