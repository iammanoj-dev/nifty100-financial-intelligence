# Sprint 2 Review

## Completed

- Implemented profitability ratios (NPM, OPM, ROE, ROCE, ROA)
- Implemented leverage and efficiency ratios
- Implemented CAGR engine with edge-case handling
- Implemented cash flow KPIs
- Populated financial_ratios table in SQLite
- Generated capital allocation classifications
- Built ratio validation engine
- Generated ratio_edge_cases.log

## Formula Decisions

- ROE calculated as Net Profit / (Equity + Reserves)
- ROCE uses EBIT / Capital Employed
- Debt-free companies return D/E = 0
- Banks and NBFCs exempt from leverage warning
- CAGR edge cases handled separately

## Edge Cases

- Zero denominator
- Negative equity
- Debt-free companies
- Turnaround companies
- Decline to loss
- Zero base CAGR
- Duplicate source records
- Year normalization between datasets

## Improvements

- Source Excel contains duplicate rows.
- OPM validation warnings caused by source inconsistencies.
- Future improvement: clean duplicates during ETL.

## Sprint Status

Sprint 2 completed successfully.
