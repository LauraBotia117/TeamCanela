from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "data/modelos.db"

def obtener_modelos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_modelo FROM modelos_clasificacion")
    modelos = cursor.fetchall()
    conn.close()
    return modelos

def obtener_modelos_detalle():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_modelo, descripcion, fuente_informacion, contenido_grafico FROM modelos_clasificacion")
    modelos = cursor.fetchall()
    conn.close()
    return modelos

def obtener_modelo_por_id(modelo_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modelos_clasificacion WHERE id = ?", (modelo_id,))
    modelo = cursor.fetchone()
    conn.close()
    return modelo

@app.route("/")
def index():
    modelos = obtener_modelos()
    modelos_detalle = obtener_modelos_detalle()
    return render_template("index.html", modelos=modelos, modelos_detalle=modelos_detalle)

@app.route("/modelo/<int:modelo_id>")
def modelo(modelo_id):
    modelos = obtener_modelos()  
    modelo = obtener_modelo_por_id(modelo_id)
    return render_template("modelo.html", modelo=modelo, modelos=modelos)

if __name__ == "__main__":
    app.run(debug=True)
