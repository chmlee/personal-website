#!/bin/bash

rm template
copy=false
n=1
while IFS= read -r line; do
    
    #echo $n
    #n=`echo $(($n + 1))`
    
    if [[ $line =~ "Template Start" ]]; then
        copy=true
    elif [[ $line =~ "Template End" ]]; then
        copy=false
        echo $line >> template
    fi
    
    #echo $line $copy 
    
    if $copy; then
        echo "$line" >> template
    fi

done < index.html

echo "</div>" >> template
echo "</body>" >> template

