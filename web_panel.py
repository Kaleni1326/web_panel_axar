
from flask import Flask, render_template, request, send_file, redirect, url_for, session
import json, io, csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

with open("datos_bot.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    estadisticas_usuarios = data["estadisticas"]
    etiquetas_usuarios = data["etiquetas"]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "axar2025":
            session["logged_in"] = True
            return redirect(url_for("panel"))
    return render_template("login.html")

@app.route("/panel")
def panel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    filtro = request.args.get("filtro", "").lower()
    filtrado = {
        uid: stats for uid, stats in estadisticas_usuarios.items()
        if filtro in uid.lower() or filtro in etiquetas_usuarios.get(uid, "").lower()
    }
    return render_template("panel.html", stats=filtrado, etiquetas=etiquetas_usuarios, timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

@app.route("/exportar")
def exportar():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID Usuario", "Etiqueta", "Manual", "Auto", "Historial"])
    for uid, stats in estadisticas_usuarios.items():
        writer.writerow([uid, etiquetas_usuarios.get(uid, ""), stats["predicciones_manual"], stats["predicciones_auto"], stats["veces_historial"]])
    output.seek(0)
    return send_file(io.BytesIO(output.read().encode()), mimetype='text/csv', as_attachment=True, download_name="estadisticas_axar.csv")

if __name__ == "__main__":
    app.run(debug=True)
