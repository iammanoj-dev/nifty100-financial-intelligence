import logging

logger = logging.getLogger(__name__)


def free_cash_flow(
    operating_activity,
    investing_activity,
):
    """
    Free Cash Flow
    """

    return (
        operating_activity
        + investing_activity
    )


def cfo_quality_score(
    cfo,
    pat,
):
    """
    CFO / PAT
    """

    if pat == 0:
        return None, None

    score = cfo / pat

    if score > 1:
        label = "High Quality"

    elif score >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return score, label


def capex_intensity(
    investing_activity,
    sales,
):
    """
    CapEx Intensity

    abs(CFI)/Sales *100
    """

    if sales == 0:
        return None, None

    intensity = (
        abs(investing_activity)
        / sales
    ) * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return intensity, label


def fcf_conversion_rate(
    free_cash_flow_value,
    operating_profit,
):
    """
    FCF Conversion Rate
    """

    if operating_profit == 0:
        return None

    return (
        free_cash_flow_value
        / operating_profit
    ) * 100


def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_pat_score=None,
):
    """
    Capital Allocation Classifier
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):

        if (
            cfo_pat_score is not None
            and cfo_pat_score > 1
        ):
            label = "Shareholder Returns"

        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Unknown"

    return (
        cfo,
        cfi,
        cff,
        label,
    )
