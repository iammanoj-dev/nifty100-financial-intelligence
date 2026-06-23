SELECT
    company_id,
    debt_to_equity
FROM financial_ratios
WHERE debt_to_equity IS NOT NULL
ORDER BY debt_to_equity DESC
LIMIT 10;

