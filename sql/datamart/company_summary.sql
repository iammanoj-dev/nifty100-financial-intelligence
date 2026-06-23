SELECT
    c.id,
    c.company_name,
    s.broad_sector,
    c.roe_percentage,
    c.roce_percentage,
    c.book_value
FROM companies c
LEFT JOIN sectors s
ON c.id = s.company_id;
