#!/usr/bin/bash

dump_file=$1;
pgpdump -i $dump_file | egrep -m 6 "RSA [n,e,d,p,q,u]" | sed "s/^\tRSA //g"
