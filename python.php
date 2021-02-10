<?php 

$command = escapeshellcmd('/var/www/html/recruit/app.py');
$output = shell_exec($command);
echo $output;

?>
