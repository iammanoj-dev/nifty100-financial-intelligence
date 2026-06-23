SELECT
    (SELECT COUNT(*) FROM companies) AS total_companies,
    (SELECT COUNT(*) FROM sectors) AS total_sector_records,
    (SELECT COUNT(*) FROM stock_prices) AS total_stock_records,
    (SELECT AVG(roe_percentage) FROM companies) AS avg_roe;
