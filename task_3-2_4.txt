#!/bin/bash
echo "=== Сумма всех оценок ==="
awk '{sum += $2} END {print sum}' students.txt

echo -e "\n=== Средняя оценка ==="
awk '{sum += $2; n++} END {print sum/n}' students.txt

echo -e "\n=== Максимальная оценка ==="
awk 'NR==1 {max=$2} $2>max {max=$2} END {print max}' students.txt
