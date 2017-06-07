#!/usr/bin/zsh
date=$(date "+%m%d%y%H%M%S");
keys_path=/home/tor/git/diplom/sockets/keys
openssl genrsa -out $keys_path/private-$date.pem 2048
php $keys_path/parse_pem_cert.php $keys_path/private-$date.pem > $keys_path/user_numbers$date.pem;
result=$($keys_path/../my_rsa.py test_message $keys_path/user_numbers$date.pem |\
   	grep -A2 decoded |\
   	cut -d$'\n' -f 3);
[[ $result == "test_message" ]] && echo "Keypair validated";
mv $keys_path/user_numbers$date.pem $keys_path/$1.pem
