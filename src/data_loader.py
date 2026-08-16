from pathlib import Path
from typing import Optional, Tuple
import pandas as pd

def get_data_path(filename: str = "mobile_game_inapp_purchases.csv") -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "raw" / filename

def load_raw_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    path = filepath or get_data_path()
    return pd.read_csv(path)

def clean_game_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Imputes missing values and formats types."""
    df_clean = df.copy()
    
    # Impute missing demographics and categorical fields
    df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
    df_clean["Gender"] = df_clean["Gender"].fillna("Unknown")
    df_clean["Country"] = df_clean["Country"].fillna("Unknown")
    df_clean["Device"] = df_clean["Device"].fillna("Other")
    df_clean["GameGenre"] = df_clean["GameGenre"].fillna("Other")
    
    if "LastPurchaseDate" in df_clean.columns:
        df_clean["LastPurchaseDate"] = pd.to_datetime(df_clean["LastPurchaseDate"], errors="coerce")
        
    paying_df = df_clean[df_clean["InAppPurchaseAmount"] > 0].copy()
    f2p_df = df_clean[df_clean["InAppPurchaseAmount"].isna() | (df_clean["InAppPurchaseAmount"] == 0)].copy()
    
    return paying_df, f2p_df

def filter_gaming_dataset(
    df: pd.DataFrame,
    genres: Optional[list] = None,
    segments: Optional[list] = None,
    devices: Optional[list] = None,
    countries: Optional[list] = None
) -> pd.DataFrame:
    """Filters dataset based on selected sidebar criteria."""
    filtered = df.copy()
    
    if genres:
        filtered = filtered[filtered["GameGenre"].isin(genres)]
    if segments:
        filtered = filtered[filtered["SpendingSegment"].isin(segments)]
    if devices:
        filtered = filtered[filtered["Device"].isin(devices)]
    if countries:
        filtered = filtered[filtered["Country"].isin(countries)]
        
    return filtered