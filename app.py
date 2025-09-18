# app.py
from flask import (
    Flask, render_template, request, redirect, send_file,
    url_for, flash
)
import os
import pandas as pd
import numpy as np
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from flask import session
import pickle, base64



def cargar_datos_fuente(opcion_fuente, archivo=None):
    if opcion_fuente == 'archivo' and archivo:
        if archivo.filename.endswith('.csv'):
            return pd.read_csv(archivo)
        elif archivo.filename.endswith('.xlsx'):
            return pd.read_excel(archivo)
        elif archivo.filename.endswith('.txt'):
            return pd.read_csv(archivo, delimiter=';')
    elif opcion_fuente == 'bd':
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///datos_baliza.db')
        return pd.read_sql('SELECT * FROM lecturas', con=engine)
    return pd.DataFrame()

# -----------------------------------------------------------------------------
# Configuración básica de Flask
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "clave-secreta"
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -----------------------------------------------------------------------------
# Configuración de la base de datos (SQLite)
# -----------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos_baliza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# Modelo de la tabla
# -----------------------------------------------------------------------------
class Datos(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    fecha       = db.Column(db.DateTime, nullable=False)
    temperatura = db.Column(db.Float)
    humedad     = db.Column(db.Float)
    presion     = db.Column(db.Float)
    iaq         = db.Column(db.Integer)
    eco2        = db.Column(db.Integer)
    tvoc        = db.Column(db.Integer)

    def as_dict(self):
        return {
            'Fecha':        self.fecha,
            'Temperatura':  self.temperatura,
            'Humedad':      self.humedad,
            'Presión':      self.presion,
            'IAQ':          self.iaq,
            'ECO2':         self.eco2,
            'TVOC':         self.tvoc,
        }

# Crea la tabla si no existe
with app.app_context():
    db.create_all()

# -----------------------------------------------------------------------------
# Funciones auxiliares
# -----------------------------------------------------------------------------
def _leer_archivo(filepath):
    """Devuelve un DataFrame con separador detectado automáticamente."""
    if filepath.endswith('.csv') or filepath.endswith('.txt'):
        # Detectar separador automáticamente
        with open(filepath, 'r', encoding='utf-8') as f:
            linea = f.readline()
            sep = ';' if linea.count(';') > linea.count(',') else ','
        return pd.read_csv(filepath, sep=sep)
    if filepath.endswith(('.xls', '.xlsx')):
        return pd.read_excel(filepath)
    raise ValueError("Formato no soportado")


def _lista_uploads():
    """Lista los archivos admitidos que hay en la carpeta uploads/"""
    return [f for f in os.listdir(app.config['UPLOAD_FOLDER'])
            if f.lower().endswith(('.csv','.xls','.xlsx','.txt'))]

# -----------------------------------------------------------------------------
# Rutas
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------ Configuración de rutas para gráficas ------------------------

@app.route('/crear_grafica', methods=['GET', 'POST'])
def crear_grafica():
    fuente = request.form.get('fuente')
    archivo = None
    if fuente == 'archivo':
        archivo_nombre = request.form.get('nombre_archivo')
        archivo_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo_nombre)
        archivo = open(archivo_path, 'rb')
    df = cargar_datos_fuente(fuente, archivo)
    if archivo:
        archivo.close()

    archivos = _lista_uploads()

    if request.method == 'POST':
        tipo      = request.form.get('tipo')
        variables = request.form.getlist('variables')
        fuente    = request.form.get('fuente')

        if not variables:
            flash("Debes marcar al menos una variable.", "warning")
            return redirect(url_for('crear_grafica'))

        # Obtener datos
        if fuente == 'bd':
            query = Datos.query.order_by(Datos.fecha.desc()).limit(100).all()[::-1]
            df = pd.DataFrame([d.as_dict() for d in query])
        else:
            nombre = request.form.get('nombre_archivo')
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre)
            df = _leer_archivo(ruta)

        if df.empty:
            flash("No hay datos disponibles.", "warning")
            return redirect(url_for('crear_grafica'))

        # Normalizar columnas
        df.columns = [c.strip().lower() for c in df.columns]
        df = df.rename(columns={
            'temperatura': 'temperature',
            'humedad': 'humidity',
            'presion': 'pressure'
        })

        # Verificar columna de fecha
        col_fecha = 'fecha' if 'fecha' in df.columns else 'timestamp'
        if col_fecha not in df.columns:
            flash("No se encuentra la columna de fecha/timestamp.", "danger")
            return redirect(url_for('crear_grafica'))

        for v in variables:
            if v.lower() not in df.columns:
                flash(f"La columna '{v}' no existe en los datos.", "danger")
                return redirect(url_for('crear_grafica'))

        # Preparar datos para la gráfica
        fechas = pd.to_datetime(df[col_fecha], dayfirst=True).dt.strftime('%Y-%m-%d %H:%M').tolist()
        data = {v: df[v.lower()].tolist() for v in variables}

        return render_template('crear_grafica.html', tipo=tipo, variables=variables,
                               fechas=fechas, data=data, archivos=archivos)

    return render_template('crear_grafica.html', archivos=archivos)

#------------------------------------------------------- Graf guardadas ------- 
@app.route('/guardar_grafica', methods=['POST'])
def guardar_grafica():
    tipo = request.form.get('tipo')
    variables = request.form.getlist('variables')

    fechas = request.form.getlist('fechas')
    data = {v: request.form.getlist(f'data_{v}') for v in variables}

    if not tipo or not variables or not fechas:
        flash("Faltan datos para guardar la gráfica.", "danger")
        return redirect(url_for('crear_grafica'))

    nueva = {
        'tipo': tipo,
        'variables': variables,
        'fechas': fechas,
        'data': data
    }

    # Guardar en archivo JSON
    ruta = os.path.join(app.root_path, 'graficas.json')
    try:
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                existentes = json.load(f)
        else:
            existentes = []

        existentes.append(nueva)

        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(existentes, f, ensure_ascii=False, indent=2)

        flash("Gráfica guardada exitosamente.", "success")

    except Exception as e:
        flash("Error al guardar la gráfica.", "danger")
        print("Error al guardar gráfica:", e)

    return redirect(url_for('graficas_guardadas'))


#------------------------------------------------------- Mostrar Graf -----------
@app.route('/graficas_guardadas')
def graficas_guardadas():
    if not os.path.exists(GUARDADAS_FILE):
        graficas = []
    else:
        with open(GUARDADAS_FILE, 'r') as f:
            graficas = json.load(f)
        # Filtra aquellas que no tengan fechas o variables
        graficas = [g for g in graficas if g.get('fechas') and g.get('variables') and g.get('data')]
    return render_template('graficas_guardadas.html', graficas=graficas)


#-------------------------------------------------------- Regenerar Graf --------
@app.route('/recrear_grafica/<int:indice>')
def recrear_grafica(indice):
    try:
        with open('graficas.json', 'r', encoding='utf-8') as f:
            graficas = json.load(f)
        g = graficas[indice]
    except (FileNotFoundError, IndexError):
        flash("No se pudo cargar la gráfica.", "danger")
        return redirect(url_for('graficas_guardadas'))

    # Leer últimos 100 datos de la BD
    query = Datos.query.order_by(Datos.fecha.desc()).limit(100).all()[::-1]
    df = pd.DataFrame([d.as_dict() for d in query])
    df.columns = [c.lower() for c in df.columns]

    fechas = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d %H:%M').tolist()
    data = {v: df[v.lower()].tolist() for v in g['variables']}

    return render_template('crear_grafica.html',
                           tipo=g['tipo'],
                           variables=g['variables'],
                           fechas=fechas,
                           data=data,
                           archivos=_lista_uploads())

#-------------------------------------------------------- Borrar Graf -----------
@app.route('/eliminar_grafica', methods=['POST'])
def eliminar_grafica():
    idx = int(request.form.get('indice'))
    if os.path.exists('graficas_guardadas.json'):
        with open('graficas_guardadas.json', 'r') as f:
            lista = json.load(f)
        if 0 <= idx < len(lista):
            del lista[idx]
            with open('graficas_guardadas.json', 'w') as f:
                json.dump(lista, f)
            flash("Gráfica eliminada correctamente.", "success")
    return redirect(url_for('graficas_guardadas'))

#--------------------------------------------------------- Limpiar Graf ----------
GUARDADAS_FILE = 'graficas_guardadas.json'

def limpiar_graficas_guardadas():
    if not os.path.exists(GUARDADAS_FILE):
        print("❌ No existe el archivo de gráficas guardadas.")
        return

    with open(GUARDADAS_FILE, 'r') as f:
        graficas = json.load(f)

    print(f"🔍 Total original: {len(graficas)} gráficas")

    # Filtra solo las gráficas válidas
    graficas_validas = [
        g for g in graficas
        if g.get('tipo') and g.get('variables') and g.get('fechas') and g.get('data')
        and isinstance(g['fechas'], list) and len(g['fechas']) > 0
        and isinstance(g['data'], dict) and all(isinstance(v, list) for v in g['data'].values())
    ]

    print(f"✅ Gráficas válidas: {len(graficas_validas)}")

    # Reescribe solo las válidas
    with open(GUARDADAS_FILE, 'w') as f:
        json.dump(graficas_validas, f, indent=2)

    print("🧼 Limpieza completada.")

# Ejecutar si se llama directamente
if __name__ == '__main__':
    limpiar_graficas_guardadas()


# ----------------------------------------------------------- Análisis estad ----
@app.route('/estadistica', methods=['GET', 'POST'])
def estadistica():
    fuente = request.form.get('fuente')
    archivo = None
    if fuente == 'archivo':
        archivo_nombre = request.form.get('nombre_archivo')
        archivo_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo_nombre)
        archivo = open(archivo_path, 'rb')
    df = cargar_datos_fuente(fuente, archivo)
    if archivo:
        archivo.close()

    archivos = _lista_uploads()
    tabla_html = None

    if request.method == 'POST':
        metricas = request.form.getlist('metricas')
        fuente   = request.form.get('fuente')
        if not metricas:
            flash("Selecciona al menos una métrica.", "warning")
            return redirect(url_for('estadistica'))

        # 1) Carga de datos
        if fuente == 'bd':
            df = pd.read_sql(Datos.query.statement, db.session.bind)
        else:
            nombre = request.form['nombre_archivo']
            ruta   = os.path.join(app.config['UPLOAD_FOLDER'], nombre)
            df     = _leer_archivo(ruta)

        # 2) Normalización de columnas
        df.columns = [c.strip().lower() for c in df.columns]
        df = df.rename(columns={
            'temperatura': 'temperature',
            'humedad':     'humidity',
            'presion':     'pressure'
        })

        if df.empty:
            flash("No hay datos para analizar.", "warning")
            return redirect(url_for('estadistica'))

        # 3) Selección de las seis variables clave (en inglés)
        numeric_cols = ['temperature','humidity','pressure','iaq','eco2','tvoc']
        faltantes = [c for c in numeric_cols if c not in df.columns]
        if faltantes:
            flash(f"Faltan columnas: {', '.join(faltantes)}", "danger")
            return redirect(url_for('estadistica'))

        df = df[numeric_cols]

        # 4) Cálculo de métricas
        calc = {}
        if 'media'      in metricas: calc['Media']      = df.mean()
        if 'mediana'    in metricas: calc['Mediana']    = df.median()
        if 'maximo'     in metricas: calc['Máximo']     = df.max()
        if 'minimo'     in metricas: calc['Mínimo']     = df.min()
        if 'desviacion' in metricas: calc['Desviación'] = df.std()

        # 5) Construcción de la tabla HTML
        tabla = pd.DataFrame(calc).T.reset_index().rename(columns={'index':'Métrica'})
        tabla_html = tabla.to_html(classes='table table-striped', index=False)

        # 6) Guardar en sesión para exportar
        session['tabla_data'] = base64.b64encode(pickle.dumps(tabla)).decode('utf-8')

    return render_template('estadistica.html',
                           archivos=archivos,
                           tabla=tabla_html)



#---------------------------------------------------------- Descarga estad --------
@app.route('/descargar_analisis', methods=['POST'])
def descargar_analisis():
    formato = request.form.get('formato', 'excel')
    data_str = session.get('tabla_data')

    if not data_str:
        flash("No hay datos para exportar.", "warning")
        return redirect(url_for('estadistica'))

    try:
        df = pickle.loads(base64.b64decode(data_str))
    except Exception as e:
        flash("Error al procesar los datos.", "danger")
        return redirect(url_for('estadistica'))

    output = BytesIO()

    if formato == 'excel':
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(output, download_name="analisis.xlsx", as_attachment=True)

    elif formato == 'csv':
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(output, download_name="analisis.csv", as_attachment=True)

    else:
        flash("Formato no soportado.", "danger")
        return redirect(url_for('estadistica'))


# ------------------------------------------------------- Subir documentos ------
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('archivo')
        if not file:
            flash("No se seleccionó archivo.", "danger")
            return redirect(request.url)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            df = _leer_archivo(filepath)
        except ValueError:
            flash("Formato no soportado. Usa CSV, Excel o TXT.", "danger")
            return redirect(request.url)

        # Normalizamos nombres
        df.columns = [c.strip().lower() for c in df.columns]

        # Insertamos en la BD
        for _, row in df.iterrows():
            dato = Datos(
                fecha = pd.to_datetime(
                    row.get('fecha') or row.get('date') or datetime.now()
                ),
                temperatura = row.get('temperatura'),
                humedad     = row.get('humedad'),
                presion     = row.get('presión') or row.get('presion'),
                iaq         = row.get('iaq'),
                eco2        = row.get('eco2'),
                tvoc        = row.get('tvoc')
            )
            db.session.add(dato)
        db.session.commit()

        flash(f"Archivo '{file.filename}' subido e importado con éxito.", "success")
        return redirect(url_for('upload'))

    return render_template('upload.html')

# --------------------------------------------------- Descargar documentos ------
@app.route('/descargar')
def descargar():
    return render_template('descargar.html')

@app.route('/descargar_datos', methods=['POST'])
def descargar_datos():
    variables    = request.form.getlist('variables')
    fecha_inicio = pd.to_datetime(request.form['fecha_inicio'])
    fecha_fin    = pd.to_datetime(request.form['fecha_fin'])
    formato      = request.form.get('formato', 'excel')

    query = (Datos.query
             .filter(Datos.fecha.between(fecha_inicio, fecha_fin))
             .order_by(Datos.fecha))

    registros = [d.as_dict() for d in query]
    if not registros:
        flash("No hay datos en ese rango de fechas.", "warning")
        return redirect(url_for('descargar'))

    df = pd.DataFrame(registros)
    df = df[['Fecha'] + variables]

    fname = f"datos_{fecha_inicio:%Y%m%d}_{fecha_fin:%Y%m%d}."
    if formato == 'excel':
        filename = fname + "xlsx"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df.to_excel(filepath, index=False)
    elif formato == 'csv':
        filename = fname + "csv"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df.to_csv(filepath, index=False)
    elif formato == 'txt':
        filename = fname + "txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df.to_csv(filepath, sep='\t', index=False)
    else:
        flash("Formato no soportado.", "danger")
        return redirect(url_for('descargar'))

    return send_file(filepath, as_attachment=True, download_name=filename)

# -----------------------------------------------------------------------------
# Arranque
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
