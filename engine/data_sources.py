"""
Stubs for data integrations:
- AMFI daily NAV (https://www.amfiindia.com/net-asset-value)
- NSE data policy: https://www.nseindia.com/market-data/nse-data-policy (use authorised feeds)
- Alpha Vantage global equities: https://www.alphavantage.co/
"""
from typing import Optional
import pandas as pd

def load_holdings_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    required = {"asset_class","instrument","amount"}
    if not required.issubset(set(df.columns)):
        raise ValueError(f"CSV must have columns: {required}")
    return df

def fetch_nav_stub(symbol: str) -> Optional[float]:
    # placeholder to be replaced with real fetch
    return None
