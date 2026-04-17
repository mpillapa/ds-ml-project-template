# Proyecto Final de Fundamentos de Ciencia de Datos - USFQ

Este es tu entorno de trabajo (*boilerplate*) profesional. Ustedes podrán utilizar este repositorio como base para estructurar su trabajo final o cualquier producto de datos a nivel productivo.

El objetivo de este proyecto es predecir los precios medios de las viviendas en distritos de California, partiendo desde los datos crudos hasta un despliegue básico en una API.

## Estructura del Repositorio

- `data/`: Contiene los datos crudos, intermedios y procesados (NO se suben a Git).
- `notebooks/`: Espacio interactivo en Jupyter para EDA y experimentación de modelos.
- `src/`: Código fuente modular en Python (carga, procesamiento, entrenamiento y API).
- `models/`: Donde debes guardar tu modelo predictivo entrenado (ej. `.pkl`).

---

## Nota sobre la carpeta `models/`

Ojo, la carpeta `models/` la metí al `.gitignore`, o sea que el modelo entrenado (`model.pkl`) no está subido acá. Les cuento el porqué, porque me topé con esto y quiero dejarlo documentado:

Cuando hice el push, GitHub me lo rechazó porque `model.pkl` pesaba **276 MB** y el límite por archivo de GitHub es de **100 MB**. Así que tocó sacarlo del commit y dejarlo solo en local.

### ¿Y por qué pesa tanto?

Resulta que mi modelo ganador fue un `RandomForestRegressor` y en la experimentación los mejores hiperparámetros me salieron bastante "grandes". Esta es la configuración que uso en [`src/models/train_model.py`](src/models/train_model.py):

- `n_estimators=200` → son 200 árboles entrenados, cada uno aporta su peso al `.pkl`.
- `max_depth=30` → árboles bien profundos, con muchos splits internos.
- `min_samples_leaf=1` → dejo que cada hoja llegue hasta una sola muestra, lo que genera todavía más nodos.
- `max_features=6` y `random_state=42` → estos no influyen en el peso, más bien en la varianza y la reproducibilidad.

Entre 200 árboles muy profundos y hojas con una sola muestra, el `.pkl` termina en ~276 MB. Básicamente cada árbol se "aprende" muchísimos detalles del train y eso se guarda tal cual al serializar con `joblib`.

### ¿Cómo regenero el modelo?

Como no está subido, si clonan el repo y quieren el `model.pkl`, solo hay que correr:

```bash
python src/models/train_model.py
```

Eso toma `data/interim/train_set.csv`, entrena el Random Forest con la misma config y deja el `model.pkl` y el `feature_columns.pkl` dentro de `models/` en su máquina. De ahí la API (`src/api/main.py`) ya lo puede cargar sin problema.

---

## Instrucciones: Proyecto Final Fundamentos de DS

Tu objetivo es completar el código faltante en los `notebooks/` y `src/` guiándote por las instrucciones (`docstrings`) dejadas en cada archivo.

### Fase 1: Recolección y Análisis Exploratorio
1. Ejecuta y completa **`src/data/make_dataset.py`** para descargar los datos (`housing.tgz`) en la carpeta `data/raw/`.
2. Completa **`src/data/split_data.py`** para realizar la partición de datos (Train/Test) asegurando no tener fuga de datos (*data leakage*). Guarda los resultados en `data/interim/`.
3. Dirígete a **`notebooks/01_exploracion.ipynb`**. Realiza el Análisis Exploratorio (EDA) a profundidad sobre tus datos de entrenamiento. Visualiza problemas de calidad y documenta tus hallazgos.

### Fase 2: Ingeniería de Variables y Limpieza
4. Experimenta en **`notebooks/02_limpieza_enriquecimiento.ipynb`**. Resuelve el manejo de faltantes, codificación de textos categóricos y crea nuevas variables combinadas (ej. recámaras por hogar).
5. Traslada la lógica funcional que aprendiste al script **`src/features/build_features.py`** para que este proceso se pueda repetir fácilmente con datos nuevos.

### Fase 3: Modelado y Optimización
6. Experimenta en **`notebooks/03_experimentacion.ipynb`**. Entrena un `LinearRegression`, `SGDRegressor`, `DecisionTree` y `RandomForest`. Haz un *fine-tuning* (grid search) al ganador, justifica tu elección y evalúa el subajuste/sobreajuste contra tu set de prueba.
7. Modifica **`src/models/train_model.py`** para configurar el flujo final: entrenar tu modelo ganador sobre las variables procesadas y guardarlo (serializarlo con `joblib`) en la carpeta `models/`.

### Fase 4: Despliegue en Producción
8. Abre **`src/api/main.py`**. En este script base de FastAPI, carga tu modelo y procesa las peticiones (POST) para regresar una predicción de precio en tiempo real.

---

## Instrucciones de Configuración Inicial

1. **Clonar este repositorio** en tu máquina local.
2. **Crear un entorno virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Mac/Linux
   # .venv\Scripts\activate   # En Windows
   ```
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Rúbrica de Calificación (100 Puntos Totales)

Este proyecto busca evaluar que puedas entablar un puente entre la teoría de la Maestría y la ingeniería de datos en la industria.

| Criterio | Descripción | Puntos |
| :--- | :--- | :---: |
| **1. Análisis Exploratorio y Calidad de Datos** | EDA profundo, uso de visualizaciones (distribución, mapas geográficos, dispersión), hallazgos de métricas y validación correcta de Train/Test Split. | **15 pts** |
| **2. Limpieza y Feature Engineering** | Correcto manejo de imputaciones, codificación nominal/ordinal justificada, y creación de nuevas variables. Integración correcta en los scripts base (`src/features`). | **15 pts** |
| **3. Experimentación y Selección de Modelos** | Prueba exhaustiva de modelos (SGD, Árboles, Regresión Lineal, Ensembles). Adecuada selección de hiperparámetros de validación cruzada. Análisis riguroso del Benchmark final. | **25 pts** |
| **4. Despliegue Básico con FastAPI** | El modelo debe cargarse sin errores en la API, y recibir parámetros (`JSON`) respondiendo predicciones congruentes por medio del protocolo HTTP. | **15 pts** |
| **5. Presentación del Proyecto** | Comunicación clara, entendimiento del caso de negocio frente a stakeholders. La manera cómo se transmiten los resultados, seguridad, elocuencia y conclusiones ejecutivas del equipo. | **30 pts** | 

¡Mucho éxito!
