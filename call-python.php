<?php
/*
Plugin name: Call Python
Author:..
....
*/

$pyScript = "/var/www/html/recruit/app.py";

exec("/usr/bin/python $pyScript", $output);
var_dump($output);
?>
