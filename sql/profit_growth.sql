SELECT
    company_id,
    compounded_profit_growth
FROM analysis
WHERE compounded_profit_growth IS NOT NULL
ORDER BY company_id;
