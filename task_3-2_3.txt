#!/bin/bash
echo "=== Студенты с оценкой выше 80 ==="
awk '$2 > 80' students.txt

echo -e "\n=== Студенты с оценкой ниже 70 ==="
awk '$2 < 70' students.txt

echo -e "\n=== Первая строка файла ==="
awk 'NR == 1' students.txt
