SELECT
    company_id,
    market_cap_crore
FROM market_cap
WHERE year = (
    SELECT MAX(year)
    FROM market_cap
)
ORDER BY market_cap_crore DESC
LIMIT 10;
