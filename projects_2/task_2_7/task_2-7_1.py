# Исходный список файлов
files = ["seq1", "seq2", "seq3", "seq4"]

# Фиксированная дата взятия образца
sample_date = "2026-02-17"

# Проходим по каждому файлу в списке
for name in files:
    # Добавляем расширение .fasta и дату
    new_name = name + "_" + sample_date + ".fasta"
    # Выводим результат
    print(new_name)