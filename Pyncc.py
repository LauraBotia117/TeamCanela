import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from io import BytesIO
import io
from sklearn.neighbors import NearestCentroid
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

datac = pd.read_csv('C:/Users/dnnru/Downloads/dataset_compras_supermercado.csv', sep=';', encoding='latin1')
datac.columns = datac.columns.str.strip()

datan = pd.read_csv('C:/Users/dnnru/Downloads/nuevos_clientes.csv', sep=',', encoding='latin1')
datan.columns = datan.columns.str.strip()

# datae = pd.read_excel('C:/Users/dnnru/Downloads/dataset_compras_supermercado.xlsx')
# print(datac.head())

def asignar_clase(row):
    categoria = row['categoria_compra']
    frecuencia = row['frecuencia_visita']
    gasto = row['monto_gasto']
    
    if categoria == 'Tecnologia':
        return 'Ocasional'
    
    elif categoria in ['Alimentos', 'Aseo', 'Ropa', 'Mascotas']:
        if frecuencia > 15:
            return 'Frecuente'
        elif 10 <= frecuencia <= 15:
            return 'Ocasional'
        elif frecuencia < 10:
            if gasto > 500000:
                return 'Ocasional'
            else:
                return 'Nuevo'
    
    return 'Nuevo'  # Valor por defecto por si acaso


datac['categoria_cliente'] = datac.apply(asignar_clase, axis=1)

X = datac[['frecuencia_visita', 'monto_gasto']]
y = datac['categoria_cliente']

#escalar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir el dataset en entrenamiento y prueba (80% entrenamiento, 30% prueba)
X_train, X_test, y_train, y_test = train_test_split( X_scaled, y, test_size=0.3, random_state=42, stratify=y)

# Entrenar
modelo = NearestCentroid()
modelo.fit(X_train, y_train)

# Hacer predicciones sobre los datos de prueba
y_pred = modelo.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
conf_matrix = confusion_matrix(y_test, y_pred)


# Guardar el modelo y el escalador
with open('modelo_entrenado.pkl', 'rb') as f:
    modelo = pickle.load(f)

with open('escalador.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Guardar Dataset Entrenamiento
with open('dataset_entrenamiento.pkl', 'wb') as f:
    pickle.dump(datac, f)

# Guardar Dataset Nuevos
with open('dataset_nuevo.pkl', 'wb') as f:
    pickle.dump(datan, f)

def predecir_cliente(frecuencia_visita, monto_gasto, categoria_compra):
    # Crear el DataFrame para los nuevos datos
    nuevos_datos = pd.DataFrame({
        'frecuencia_visita': [frecuencia_visita],
        'monto_gasto': [monto_gasto],
        'categoria_compra': [categoria_compra]
    })
    
    # Asignar la clase (esto no es necesario para predecir, pero si lo quieres para registrar el real + predicho, está bien)
    nuevos_datos['categoria_cliente'] = nuevos_datos.apply(asignar_clase, axis=1)

    # Preprocesar los datos
    X_nuevo = nuevos_datos[['frecuencia_visita', 'monto_gasto']]


    X_nuevo_scaled = scaler.transform(X_nuevo)


    # Hacer la predicción
    prediccion = modelo.predict(X_nuevo_scaled)

    # Devolver la predicción
    return prediccion[0]



def guardar_datos_prediccion(frecuencia_visita, monto_gasto, categoria_compra, resultado):
    # Crear un nuevo DataFrame para los nuevos datos
    nuevos_datos = pd.DataFrame({
        'frecuencia_visita': [frecuencia_visita],
        'monto_gasto': [monto_gasto],
        'categoria_compra': [categoria_compra],
        'categoria_cliente': [resultado]
    })
    
    # Guardar los datos en un archivo CSV
    nuevos_datos.to_csv('C:/Users/dnnru/Downloads/nuevos_clientes.csv', mode='a', header=False, index=False)

def obtener_dataset_pickle():
    with open('dataset_entrenamiento.pkl', 'rb') as f:
        df = pickle.load(f)
    return df.head().to_html(classes='table table-striped', index=False), df.tail().to_html(classes='table table-striped', index=False)

def descargar_csv_pickle():
    with open('dataset_entrenamiento.pkl', 'rb') as f:
        df = pickle.load(f)

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Retorna un archivo en memoria listo para ser enviado
    return io.BytesIO(output.getvalue().encode())

def descargar_excel_pickle():
    with open('dataset_entrenamiento.pkl', 'rb') as f:
        df = pickle.load(f)

    # Crear un archivo Excel en memoria usando openpyxl
    output = io.BytesIO()

    # Usar pandas con openpyxl como motor
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')

    output.seek(0)
    return output


def obtener_dataset_picklen():
    with open('dataset_nuevo.pkl', 'rb') as f:
        df = pickle.load(f)
    # Mostrar la tabla completa (sin cabeza ni cola)
    return df.to_html(classes='table table-striped', index=False)

def descargar_csv_picklen():
    with open('dataset_nuevo.pkl', 'rb') as f:
        df = pickle.load(f)

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Retorna un archivo CSV completo en memoria listo para ser enviado
    return io.BytesIO(output.getvalue().encode())

def descargar_excel_picklen():
    with open('dataset_nuevo.pkl', 'rb') as f:
        df = pickle.load(f)

    # Crear un archivo Excel en memoria usando openpyxl
    output = io.BytesIO()

    # Usar pandas con openpyxl como motor
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')

    output.seek(0)
    return output