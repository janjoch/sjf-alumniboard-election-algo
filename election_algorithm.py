import numpy as np

import pandas as pd


def import_xlsx(
    io,
):
    df = pd.read_excel(
        io=io,
        skiprows=(1,),
        false_values=(np.nan, "", pd.NA),
    )
    return df
