SELECT
    company_id,
    AVG(volume) AS avg_volume
FROM stock_prices
GROUP BY company_id
ORDER BY avg_volume DESC
LIMIT 10;
