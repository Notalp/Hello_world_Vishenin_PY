SELECT
    product_id,
    COUNT(*) AS price_count,
    AVG(price) AS average_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM prices
GROUP BY product_id;