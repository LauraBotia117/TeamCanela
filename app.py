from flask import Flask, render_template, request, send_file
import sqlite3
import LineaRegresiones
import PyRegresion
import PyLogistica
from Pyncc import predecir_cliente, guardar_datos_prediccion, obtener_dataset_pickle, descargar_csv_pickle, descargar_excel_pickle, obtener_dataset_picklen, descargar_csv_picklen, descargar_excel_picklen
from poblar_db import obtener_modelo_por_id, obtener_modelos, obtener_modelos_detalle
from PyLogistica import obtener_matriz_confusion, obtener_metricas


app = Flask(__name__, template_folder='Templates')

# Home 
@app.route("/")
def home():
    return render_template("inicioflask.html")

# Ruta Actividad 3 Casos de uso
@app.route("/Casodeuso/")
def Casodeuso():
    return render_template('casodeuso.html')

# Ruta para hora actual
@app.route("/hello/<name>")
def hello_there(name):
    from datetime import datetime
    import re
    
    now = datetime.now()
    match_object = re.fullmatch("[a-zA-Z]+", name)
    clean_name = match_object.group(0) if match_object else "Friend"
    
    content = f"Hello everyone!!!!!, {clean_name} ! Hour: {now}"
    return content 

# Ruta ejemplo de html 
@app.route("/examplehtml/")
def examplehtml():
    return render_template("example.html")

# Ruta para calcular la regresión logistica
@app.route("/RegresionLogistica/")
def RegresionLogistica():
    return render_template("RegresionLogistica.html")

# Ruta para calcular la regresión lineal
@app.route("/linearegresion/", methods=["GET", "POST"])
def calculategrades():
    predictResult = None
    grafica = LineaRegresiones.generate_plot()

    if request.method == "POST":
        hours = float(request.form["hours"])
        predictResult = LineaRegresiones.calculateGrade(hours)

    return render_template("linearRegresionGrades.html", result=predictResult, plot_url=grafica)

@app.route("/SalarioMensual/", methods=["GET", "POST"])
def calcularsalarios():
    predictResult = None
    grafico = PyRegresion.generate_plot()

    if request.method == "POST":
        salario = float(request.form["salario"])
        predictResult = PyRegresion.calcularsalario(salario)

    return render_template("HtRegresion.html", result=predictResult, plot_url=grafico)


#SEMANA 6
@app.route("/Telecomunicaciones/")
def menu():
    return render_template("MenuNavegacionLogistica.html")

@app.route("/Telecomunicaciones/Dataset")
def dataset():
    from PyLogistica import obtener_dataset_html
    dataset_html = obtener_dataset_html()
    return render_template("DatasetLogistica.html", dataset_html=dataset_html)

@app.route("/Telecomunicaciones/Predecir", methods=["GET", "POST"])
def predecir():
    resultado = None

    if request.method == "POST":
        duracion_llamada = float(request.form["duracion_llamada"])
        plan_contratado = int(request.form["plan_contratado"])
        historial_pago = float(request.form["historial_pago"])
        
        # Usamos el modelo de regresión logística para predecir
        resultado = PyLogistica.predecir_cancelacion(duracion_llamada, plan_contratado, historial_pago)

    return render_template("PredecirLogistica.html", resultado=resultado)

@app.route('/Telecomunicaciones/Resultados')
def mostrar_resultados():
    matriz_confusion = obtener_matriz_confusion()
    accuracy, precision, recall = obtener_metricas()
    return render_template('ResultadosLogistica.html', matriz_confusion=matriz_confusion, accuracy=accuracy, precision=precision, recall=recall)

#SEMANA 7
@app.route("/modelo/")
def index():
    modelos = obtener_modelos()
    modelos_detalle = obtener_modelos_detalle()
    return render_template("index.html", modelos=modelos, modelos_detalle=modelos_detalle)

@app.route("/modelo/<int:modelo_id>")
def modelo(modelo_id):
    modelos = obtener_modelos()  
    modelo = obtener_modelo_por_id(modelo_id)
    return render_template("modelo.html", modelo=modelo, modelos=modelos)

#SEMANA 8
@app.route("/Supermercado/")
def menusup():
    return render_template("MenuNavegacionNcc.html")

@app.route("/Supermercado/Predecir", methods=["GET", "POST"])
def supermerpredecir():
    prediccion = None
    if request.method == "POST":
        frecuencia_visita = float(request.form["frecuencia_visita"])
        monto_gasto = float(request.form["monto_gasto"])
        categoria_compra = request.form["categoria_compra"]
        
        # Llamar a la función para obtener la predicción
        prediccion = predecir_cliente(frecuencia_visita, monto_gasto, categoria_compra)

        guardar_datos_prediccion(frecuencia_visita, monto_gasto, categoria_compra, prediccion)
    
    return render_template("PredecirSup.html", prediccion=prediccion)

@app.route("/Supermercado/Dataset/")
def menudat():
    return render_template("MenuDataset.html")

@app.route('/Supermercado/Dataset/Modelo', methods=['GET', 'POST'])
def datasetm_ncc():
    # Obtener el inicio y fin del dataset desde el archivo pickle
    inicio_html, fin_html = obtener_dataset_pickle()

    if request.method == 'POST':
        if 'csv' in request.form:
            csv_file = descargar_csv_pickle()
            return send_file(
                csv_file,
                mimetype='text/csv',
                as_attachment=True,
                download_name='dataset_entrenamiento.csv'
            )
        elif 'excel' in request.form:
            excel_file = descargar_excel_pickle()
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='dataset_entrenamiento.xlsx'
            )

    return render_template('DsNccM.html', inicio_html=inicio_html, fin_html=fin_html)

@app.route('/Supermercado/Dataset/Nuevo', methods=['GET', 'POST'])
def datasetn_ncc():
    dataset_html = obtener_dataset_picklen()

    if request.method == 'POST':
        if 'csv' in request.form:
            csv_file = descargar_csv_picklen()
            return send_file(
                csv_file,
                mimetype='text/csv',
                as_attachment=True,
                download_name='dataset_nuevo.csv'
            )
        elif 'excel' in request.form:
            excel_file = descargar_excel_picklen()
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='dataset_nuevo.xlsx'
            )

    return render_template('DsNccN.html', dataset_html=dataset_html)