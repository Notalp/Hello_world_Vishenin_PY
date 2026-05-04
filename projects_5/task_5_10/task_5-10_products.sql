-- 1. Вывести название и категорию всех товаров
SELECT name, category FROM products;

-- 2. Вывести список всех уникальных категорий товаров
SELECT DISTINCT category FROM products;

-- 3. Все товары, отсортированные по названию (А-Я)
SELECT * FROM products ORDER BY name ASC;

-- 4. Все товары, отсортированные по названию (Я-А)
SELECT * FROM products ORDER BY name DESC;

-- 5. Первые 10 товаров
SELECT * FROM products LIMIT 10;

-- 6. 10 товаров, начиная с 11-й записи
SELECT * FROM products LIMIT 10 OFFSET 10;

-- 7. 5 случайных товаров
SELECT * FROM products ORDER BY RANDOM() LIMIT 5;

-- 8. Все категории (без DISTINCT), отсортированные по алфавиту
SELECT category FROM products ORDER BY category ASC;

-- 9. Все товары, отсортированные сначала по категории, затем по названию
SELECT * FROM products ORDER BY category ASC, name ASC;