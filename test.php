<?php
$uhrzeit = 0;
$aussentemp = 20;
$raumtemp = 21;


echo"ffgghghjhg";
// Verwende exec(), um das Python-Skript auszuführen
exec("python script.py $aussentemp $raumtemp", $output);

// $output wird die Ausgabe des Python-Skripts enthalten
echo "Ergebnis: " . implode($output);
?>