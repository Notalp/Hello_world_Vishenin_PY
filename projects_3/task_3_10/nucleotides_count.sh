#!/bin/bash

# Заголовок таблицы
printf "%-20s %-7s %-7s %-7s %-7s\n" "Файл" "A" "T" "G" "C"
printf "%-20s %-7s %-7s %-7s %-7s\n" "--------------------" "-------" "-------" "-------" "-------"

# Перебираю все .fasta файлы в текущей папке
for file in *.fasta; do
    # Проверка, что файл действительно существует (на случай, если нет ни одного .fasta)
    if [ ! -f "$file" ]; then
        continue
    fi

    # Пропускаю пустые файлы (размер 0 байт)
    if [ ! -s "$file" ]; then
        echo "Файл '$file' пуст, пропускаем."
        continue
    fi

    # Извлекаю последовательности: убираю строки с '>' и все переводы строк
    sequence=$(grep -v "^>" "$file" | tr -d '\n')

    # Подсчёт каждого нуклеотида (регистр: ищем и заглавные, и строчные)
    count_A=$(echo "$sequence" | grep -io "A" | wc -l)
    count_T=$(echo "$sequence" | grep -io "T" | wc -l)
    count_G=$(echo "$sequence" | grep -io "G" | wc -l)
    count_C=$(echo "$sequence" | grep -io "C" | wc -l)

    # Вывод строки таблицы с выравниванием
    printf "%-20s %-7s %-7s %-7s %-7s\n" "$file" "$count_A" "$count_T" "$count_G" "$count_C"
done
