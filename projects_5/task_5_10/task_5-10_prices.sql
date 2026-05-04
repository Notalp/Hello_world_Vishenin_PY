-- 1. 5 самых дорогих записей
SELECT * FROM prices ORDER BY price DESC LIMIT 5;

-- 2. 10 последних добавленных записей (по created_at) — от новых к старым
SELECT * FROM prices ORDER BY created_at DESC LIMIT 10;

-- 3. 10 самых дешёвых цен
SELECT * FROM prices ORDER BY price ASC LIMIT 10;

-- 4. Пропустить первые 20 самых дорогих, показать следующие 10
SELECT * FROM prices ORDER BY price DESC LIMIT 10 OFFSET 20;