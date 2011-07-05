<?php

$mystring = system('filemover --action getfilename --app testapp --type invoice', $retval);
echo($mystring);
