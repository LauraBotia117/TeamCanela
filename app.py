from flask import Flask, render_template, request
import LineaRegresiones
import PyRegresion

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

