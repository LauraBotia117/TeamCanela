import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

def generar_dataset():
    np.random.seed(42)  # Fijar semilla para reproducibilidad
    
    # Generación de variables independientes
    duracion_llamada = np.random.randint(1, 61, 100)  # Duración en minutos (1 a 60)
    plan_contratado = np.random.choice([0, 1], size=100)  # 0 = No, 1 = Sí
    historial_pago = np.random.rand(100)  # Valores entre 0 y 1
    
    # Generación de variable objetivo (cancelación de servicio)
    cancelacion = np.where((duracion_llamada < 20) & (plan_contratado == 0) & (historial_pago < 0.5), "Sí", "No")
    
    # Creación del DataFrame
    dataset = pd.DataFrame({
        "Duracion_Llamada": duracion_llamada,
        "Plan_Contratado": plan_contratado,
        "Historial_Pago": historial_pago,
        "Cancelacion": cancelacion
    })
    
    return dataset

def obtener_dataset_html():
    dataset = generar_dataset()
    return dataset.to_html(classes='table table-bordered', index=False)
