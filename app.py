import re
from datetime import datetime
from flask import Flask, render_template, request
import LineaRegresiones
import PyRegresion

app = Flask(__name__)

# Home 
@app.route("/")
def home():
    return "Hello, Flask!"

# Ruta Actividad 3 Casos de uso
@app.route("/Casodeuso/")
def Casodeuso():

    return render_template('casodeuso.html')

# Ruta para hora actual
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()

    match_object = re.fullmatch("[a-zA-Z]+", name)
    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = f"Hello everyone!!!!!, {clean_name} ! Hour: {now}"
    return content 

#Ruta ejemplo de html 
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
    grafica = LineaRegresiones.generate_plot()  # Obtener el gráfico de regresión

    if request.method == "POST":
        hours = float(request.form["hours"])
        predictResult = LineaRegresiones.calculateGrade(hours)

    return render_template("linearRegresionGrades.html", result=predictResult, plot_url=grafica)


@app.route("/SalarioMensual/", methods=["GET", "POST"])
def calcularsalarios():
    predictResult = None
    grafico = PyRegresion.generate_plot()  # Obtener el gráfico de regresión

    if request.method == "POST":
        salario = float(request.form["salario"])
        predictResult = PyRegresion.calcularsalario(salario)

    return render_template("HtRegresion.html", result=predictResult, plot_url=grafico)

import string

ALFABETO = string.ascii_lowercase

def algoritmo_descifrado(texto_cifrado, clave_descifrado):
    """
    Esta función descifra el texto cifrado a partir de una clave de descifrado
    """

    texto_plano = ""

    for letra in texto_cifrado:
        if letra not in ALFABETO:
            texto_plano += letra
        else:
            indice_letra_cifrada = ALFABETO.index(letra)
            indice_letra_descifrada = indice_letra_cifrada - clave_descifrado

            texto_plano += ALFABETO[indice_letra_descifrada]

    return texto_plano

if __name__ == "__main__":
    # Solicitamos el texto a cifrar al usuario
    texto_cifrado = input("Por favor introduce el texto cifrado: ").lower()

    # Solicitamos 
    clave_descifrado = int(input("Por favor introduce la clave de descifrado: "))

    texto_plano = algoritmo_descifrado(texto_cifrado, clave_descifrado)

    print(texto_plano)
