-- 1. Выведите записи из таблицы prices, где цена находится в диапазоне от 1000 до 50000 включительно.
SELECT * FROM prices WHERE price BETWEEN 1000 AND 50000;

-- 2. Выведите цены товаров (prices), у которых: price находится в диапазоне от 500 до 70000; и product_id меньше или равен 5.
SELECT * FROM prices WHERE price BETWEEN 500 AND 70000 AND product_id <= 5;

-- 3. Выведите цены товаров, которые: меньше 100 или; находятся в диапазоне от 60000 до 70000.
SELECT * FROM prices WHERE price < 100 OR price BETWEEN 60000 AND 70000;