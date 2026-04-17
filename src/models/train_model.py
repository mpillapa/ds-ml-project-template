import sys
import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from features.build_features import preprocess_pipeline


def train_and_save(train_path: str, model_output_path: str):
    # Cargamos los datos
    print("Cargando datos...")
    train = pd.read_csv(train_path)

    # Aplicamos el pipeline de features
    print("Aplicando pipeline de features...")
    train = preprocess_pipeline(train)

    # Separamos las features del target
    X_train = train.drop("median_house_value", axis=1)
    y_train = train["median_house_value"]

    # Entrenamos el modelo con los mejores hiperparámetros encontrados en la experimentación
    print("Entrenando modelo...")
    modelo = RandomForestRegressor(
        n_estimators=200,
        max_features=6,
        max_depth=30,
        min_samples_leaf=1,
        random_state=42
    )
    modelo.fit(X_train, y_train)

    # Evaluamos el RMSE en train para verificar que no haya sobreajuste extremo
    y_pred_train = modelo.predict(X_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    print(f"RMSE en Train: ${rmse_train:,.0f}")

    # Guardamos el modelo y las columnas de features para su uso en la API
    Path(model_output_path).mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, Path(model_output_path) / "model.pkl")
    joblib.dump(list(X_train.columns), Path(model_output_path) / "feature_columns.pkl")
    print(f"Modelo guardado en: {model_output_path}/model.pkl")
    print(f"Columnas guardadas en: {model_output_path}/feature_columns.pkl")


if __name__ == "__main__":
    train_and_save(
        train_path="data/interim/train_set.csv",
        model_output_path="models/"
    )
