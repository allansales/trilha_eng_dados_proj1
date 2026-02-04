import pandas as pd
import numpy as np
import holidays
from datetime import timedelta

def get_is_sla_violated(df:pd.DataFrame, hours_to_resolve_colname:str, expected_hours_colname:str) -> pd.DataFrame:
    """
    Check whether the SLA is violated or not.
    """
    return((df[hours_to_resolve_colname] > df[expected_hours_colname]))

def get_expected_sla_hours_to_resolution(df:pd.DataFrame, priority_colname:str) -> pd.DataFrame:
    """
    Insert the expected SLA hours by priority to the dataframe.
    """
    hours_expected = pd.DataFrame({priority_colname:['High', 'Medium', 'Low'], 'expected_sla_hours_to_resolution':[24, 72, 120]})
    df = df.merge(hours_expected, on=priority_colname, how='left')
    return df

def get_business_hours_diff(start, end) -> int:
    """
    Compute the difference of business hours between in two timestamps.
    It is considered a business day, any day between monday and friday that are not national holidays.
    """

    country_holidays = holidays.Brazil()

    if pd.isna(start) or pd.isna(end) or start >= end:
        return 0.0

    # Normalize dates
    start_date = start.normalize()
    end_date = end.normalize()

    # Get range of business days
    business_days = pd.date_range(
        start=start_date,
        end=end_date,
        freq="B"
    )

    # Remove holidays
    business_days = [
        day for day in business_days
        if day.date() not in country_holidays
    ]

    total_hours = 0.0

    for day in business_days:
        day_start = day
        day_end = day + timedelta(days=1)

        effective_start = max(start, day_start)
        effective_end = min(end, day_end)

        hours = (effective_end - effective_start).total_seconds() / 3600

        if hours > 0:
            total_hours += hours

    return total_hours