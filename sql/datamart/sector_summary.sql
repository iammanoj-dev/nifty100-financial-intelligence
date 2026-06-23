SELECT
    broad_sector,
    COUNT(*) AS company_count,
    AVG(index_weight_pct) AS avg_index_weight
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;
