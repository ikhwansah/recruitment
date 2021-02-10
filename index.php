<?php 

$command = escapeshellcmd('/var/www/html/recruit/test.py');
$output = shell_exec($command);
echo $output;

?>
