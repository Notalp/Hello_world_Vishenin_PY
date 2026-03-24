#!/bin/bash
echo "=== Файловая система и заполнение ==="
df -h | awk 'NR>1 {print $1, $5}' | while read fs usage; do
    # Убираем символ % из значения использования
    percent=$(echo $usage | tr -d '%')
    if [ $percent -gt 90 ]; then
        echo "ВНИМАНИЕ: $fs заполнена на $usage (более 90%!)"
    else
        echo "$fs $usage"
    fi
done
