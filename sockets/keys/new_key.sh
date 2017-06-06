#!/usr/bin/zsh
date=$(date "+%m%d%y%H%M%S");
openssl genrsa -out private-$date.pem 2048;
php parse_pem_cert.php private-$date.pem > user_numbers$date.pem;
result=$(../my_rsa.py test_message user_numbers$date.pem |\
   	grep -A2 decoded |\
   	cut -d$'\n' -f 3);
[[ $result == "test_message" ]] && echo "Keypair validated";
mv user_numbers$date.pem $1.pem
