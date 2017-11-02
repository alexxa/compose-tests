#!/bin/bash

failed_modules=$(grep -oP ".*?(?= =>)" error.log | sed s,/default,, | sort | uniq)

python tests/parse_yaml.py

sed '/Last metadata expiration/Q' modules_list.log

echo "----------------------------------------------------------------------"
printf "\n%-25s =>  %-25s\n" "MODULE" "STATE"
echo "----------------------------------------------------------------------"

while IFS='' read -r line || [[ -n "$line" ]]; do
        if echo "$failed_modules" | grep -q "^$line$"; then
            printf "%-25s =>  %-25s\n" "$line" "Error: See logs [1, 2]"
        else
            printf  "%-25s =>  %-25s\n" "$line" "pass"
	fi
done < "$1"

