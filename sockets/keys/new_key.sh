#!/usr/bin/zsh
date=$(date "+%m%d%y%H%M%S");
path="/home/tor/git/diplom/sockets/keys";
openssl genrsa -out $path/private-$date.pem 2048;
php $path/parse_pem_cert.php $path/private-$date.pem > $path/user_numbers$date.pem;
result=$($path/../my_rsa.py test_message $path/user_numbers$date.pem |\
   	grep -A2 decoded |\
   	cut -d$'\n' -f 3);
[[ $result == "test_message" ]] && echo "Keypair validated";
mv $path/user_numbers$date.pem $path/$1.pem
