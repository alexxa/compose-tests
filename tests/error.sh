#!/bin/bash

error='raw_error.log'

cat $error | while read line
do
	starter=$(echo "$line" | cut -f1 -d'{')
	error_msg=$(echo "$line" | awk -v FS="(Error: |\", \"stdout)" '{print $2}' | sed 's/^n //g; s/n$//g')
	printf "%s %s\n" "$starter" "$error_msg"
done | sed -e 'G' >> error.log

rm -f 'raw_error.log'
