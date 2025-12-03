import numpy as np
import pandas as pd

# --- Chargement automatique du CPI ---
_cpi_df = pd.read_csv("Data/USCPI_1774-2024.csv", skiprows=2)
_cpi_df["Year"] = _cpi_df["Year"].astype(int)
_cpi_df.set_index("Year", inplace=True)

# Series CPI propre
cpi = _cpi_df["U.S. Consumer Price Index *"]
cpi.index.name = None


def real_price(values, dates, base=2024):
    """
    Convertit des valeurs nominales en dollars constants (base = base).
    Le CPI est automatiquement chargé depuis Data/USCPI_1774-2024.csv.
    """

    vals = pd.Series(values)
    yrs  = pd.Series(dates).astype(int)

    if not yrs.isin(cpi.index).all():
        missing = yrs[~yrs.isin(cpi.index)].unique()
        raise ValueError(f"Années CPI manquantes : {missing}")

    ratio = cpi.loc[base] / cpi.loc[yrs].values
    out = vals * ratio

    # Retour au même format
    if isinstance(values, np.ndarray):
        return out.to_numpy()
    elif isinstance(values, list):
        return out.tolist()
    elif isinstance(values, (pd.Series, pd.DataFrame)):
        return out
    else:
        return float(out.iloc[0])