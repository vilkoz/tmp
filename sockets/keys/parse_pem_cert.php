<?php
require_once("ASNValue.class.php");
function PemToDer($Pem) {
    //Split lines:
    $lines = explode("\n", trim($Pem));
    //Remove last and first line:
    unset($lines[count($lines)-1]);
    unset($lines[0]);
    //Join remaining lines:
    $result = implode('', $lines);
    //Decode:
    $result = base64_decode($result);
    return $result;
}

function PrintHex($binary)
{
	$i = 0;
	echo "(".intval(strlen($binary) * 8). " bits) - ";
	while ($i < strlen($binary))
	{
		printf("%02x ", ord($binary[$i]));
		$i++;
	}
	printf("\n");
}
if(count($argv) != 2)
{
	echo ("provide key filename!\n");
	exit();
}
$PrivateDER = PemToDer(file_get_contents($argv[1]));
//Decode root sequence
$body = new ASNValue();
$body->Decode($PrivateDER);
$bodyItems = $body->GetSequence();

//Read key values:

/* echo("head = ".base64_encode($bodyItems[0]->GetIntBuffer())."\n"); */
$n = $bodyItems[1]->GetIntBuffer();
echo("n");
/* echo("n: ".base64_encode($n)."\n"); */
PrintHex($n);
$e = $bodyItems[2]->GetInt();
/* echo("e: ".base64_encode($e)."\n"); */
echo("e(17 bits) - 01 00 01 \n");
/* PrintHex($e); */
$d = $bodyItems[3]->GetIntBuffer();
/* echo("d: ".base64_encode($d)."\n"); */
echo("d");
PrintHex($d);
$Prime1 = $bodyItems[4]->GetIntBuffer();
$Prime2 = $bodyItems[5]->GetIntBuffer();
$Exponent1 = $bodyItems[6]->GetIntBuffer();
$Exponent2 = $bodyItems[7]->GetIntBuffer();
$Coefficient = $bodyItems[8]->GetIntBuffer();
?>
