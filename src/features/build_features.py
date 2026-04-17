"""
Módulo para limpieza y enriquecimiento (Feature Engineering) usando funciones simples.
"""

import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    INSTRUCCIONES:
    1. Maneja los valores faltantes.
       Puedes llenarlos con la mediana de la columna.
    2. Retorna el DataFrame limpio.
    """
    # Tu código aquí
    mediana = df["total_bedrooms"].median()
    df["total_bedrooms"] = df["total_bedrooms"].fillna(mediana)
    return df

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    INSTRUCCIONES:
    1. Agrega nuevas variables derivando las existentes, por ejemplo:
       - 'rooms_per_household' = total_rooms / households
       - 'population_per_household' = population / households
       - 'bedrooms_per_room' = total_bedrooms / total_rooms
    2. Retorna el DataFrame enriquecido.
    """
    # Tu código aquí
    df["rooms_per_household"]      = df["total_rooms"]    / df["households"]
    df["bedrooms_per_room"]        = df["total_bedrooms"] / df["total_rooms"]
    df["population_per_household"] = df["population"]     / df["households"]

    # Distancia a San Francisco y Los Ángeles
    SF_LAT, SF_LON = 37.77, -122.42
    LA_LAT, LA_LON = 34.05, -118.24

    df["dist_sf"] = np.sqrt(
        (df["latitude"] - SF_LAT)**2 + (df["longitude"] - SF_LON)**2
    )
    df["dist_la"] = np.sqrt(
        (df["latitude"] - LA_LAT)**2 + (df["longitude"] - LA_LON)**2
    )

    # Ingreso por cuarto disponible
    df["income_per_room"] = df["median_income"] / df["rooms_per_household"]

    return df

def preprocess_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función orquestadora que toma el DataFrame crudo y aplica limpieza y enriquecimiento.
    """
    df_clean = clean_data(df)
    df_featured = create_features(df_clean)
    
    # IMPORTANTE: Aquí los alumnos deberían añadir codificación de variables categóricas
    # (ej. get_dummies para 'ocean_proximity') si no usan Pipelines de Scikit-Learn.
    df_encoded  = pd.get_dummies(df_featured, columns=["ocean_proximity"])
    return df_encoded

if __name__ == "__main__":
    print("Módulo de feature engineering... (Falta el código!)")
