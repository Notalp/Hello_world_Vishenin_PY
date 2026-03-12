#!/bin/bash

echo "=== Этап 1: Создание файлов ==="
# Цикл for для создания файлов test1.txt ... test10.txt
for i in {1..10}; do
    touch "test${i}.txt"
    echo "  Создан файл: test${i}.txt"
done

# Проверяю, что файлы создались
echo -e "\nСодержимое папки после создания:"
ls -l test*.txt 2>/dev/null || echo "Файлы не найдены."

echo -e "\n=== Этап 2: Удаление файлов в обратном порядке ==="
# Цикл while для удаления от test10.txt до test1.txt
# Инициализирую счётчик
counter=10
while [ $counter -ge 1 ]; do
    # Формирую имя файла
    filename="test${counter}.txt"
    # Проверяю, существует ли файл, и удаляю
    if [ -f "$filename" ]; then
        rm "$filename"
        echo "  Удалён файл: $filename"
    else
        echo "  Файл $filename не найден (уже удалён?)."
    fi
    # Уменьшаю счётчик на 1
    ((counter--))
done

echo -e "\n=== Проверка после удаления ==="
ls -l test*.txt 2>/dev/null && echo "Файлы остались!" || echo "Все файлы успешно удалены."
