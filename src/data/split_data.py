"""
Script para dividir los datos en conjunto de entrenamiento y conjunto de prueba.
"""

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

def split_and_save_data(raw_data_path: str, interim_data_path: str):
    """
    INSTRUCCIONES:
    1. Lee el archivo CSV descargado previamente en `raw_data_path` usando pandas.
    2. Separa los datos con `train_test_split()`. Te recomendamos un test_size=0.2 y random_state=42.
    3. (Opcional pero recomendado) Puedes usar `StratifiedShuffleSplit` basado en la variable
       del ingreso medio (median_income) para que la muestra sea representativa.
    4. Guarda los archivos resultantes (ej. train_set.csv y test_set.csv) en la carpeta `interim_data_path`.
    """

    # Leemos los datos
    data = pd.read_csv(raw_data_path)

    # Separamos los datos usando StratifiedShuffleSplit basado en median_income
    data["income_cat"] = pd.cut(data["median_income"],
                                bins=[0., 1.5, 3.0, 4.5, 6., float("inf")],
                                labels=[1, 2, 3, 4, 5])
    
    from sklearn.model_selection import StratifiedShuffleSplit
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(data, data["income_cat"]):
        train_set = data.loc[train_index].drop("income_cat", axis=1)
        test_set = data.loc[test_index].drop("income_cat", axis=1)

    # Guardamos los archivos resultantes
    Path(interim_data_path).mkdir(parents=True, exist_ok=True)
    train_set.to_csv(Path(interim_data_path) / "train_set.csv", index=False)
    test_set.to_csv(Path(interim_data_path) / "test_set.csv", index=False)


if __name__ == "__main__":
    RAW_PATH     = "data/raw/housing/housing.csv"
    INTERIM_PATH = "data/interim/"
    split_and_save_data(RAW_PATH, INTERIM_PATH)

