#!/bin/bash

installed_modules='installed_modules.log'
enabled_modules='enabled_modules.log'
failed_modules='error.log'
failed_modules_amount=$(cat $failed_modules | wc -l)

sed '/Last metadata expiration/Q' installed_modules.log

echo "----------------------------------------------------------------------"
printf "\n%-25s =>  %-25s\n" "MODULE" "STATE"
echo "----------------------------------------------------------------------"

while IFS='' read -r line || [[ -n "$line" ]]; do
        if $(grep -q "$line" "$failed_modules"); then
            printf "%-25s =>  %-25s\n" "$line" "Error: See logs [1, 2]"
	elif $(grep -q "$line" "$installed_modules"); then
	    printf "%-25s =>  %-25s\n" "$line" "installed"
	    echo  "$item"
	elif $(grep -q "$line" "$enabled_modules"); then
            printf "%-25s =>  %-25s\n" "$line" "enabled"
	else
            printf  "%-25s =>  %-25s\n" "$line" "Error: something is wrong"
	fi
done < "$1"

