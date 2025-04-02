from flask import Flask, render_template, request
import LineaRegresiones
import PyRegresion
import PyLogistica
from PyLogistica import obtener_matriz_confusion, obtener_metricas


app = Flask(__name__)

# Home 
@app.route("/")
def home():
    return render_template("index.html")

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
