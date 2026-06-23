SELECT
    company_id,
    pe_ratio,
    pb_ratio,
    dividend_yield_pct
FROM market_cap
WHERE year = (
    SELECT MAX(year)
    FROM market_cap
)
ORDER BY pe_ratio DESC
LIMIT 20;
