SELECT
    id,
    company_name,
    roe_percentage
FROM companies
WHERE roe_percentage IS NOT NULL
ORDER BY roe_percentage DESC
LIMIT 10;
