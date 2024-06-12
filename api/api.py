import json
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from threading import Thread
import time

# Ruta del archivo JSON
FILE_PATH = '../medicamentos.json'

# Función para cargar los datos de los medicamentos desde el archivo JSON
def load_medicamentos():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    else:
        return []

# Función para guardar los datos de los medicamentos en el archivo JSON
def save_medicamentos(medicamentos):
    with open(FILE_PATH, 'w') as file:
        json.dump(medicamentos, file, indent=2)

# Función para agregar un nuevo medicamento
def agregar_medicamento(nombre, frecuencia, inicio, duracion):
    medicamentos = load_medicamentos()
    medicamentos.append({
        'nombre': nombre,
        'frecuencia': frecuencia,
        'historial': [],
        'inicio': inicio,
        'diasRestantes': duracion
    })
    save_medicamentos(medicamentos)
    return f'Medicamento {nombre} agregado con frecuencia de {frecuencia} horas, inicio del tratamiento el {inicio} y duración de {duracion} días.'

# Función para registrar la toma de un medicamento
def registrar_toma(nombre, fecha=None):
    medicamentos = load_medicamentos()
    medicamento = next((med for med in medicamentos if med['nombre'] == nombre), None)
    if medicamento:
        ahora = datetime.now().isoformat() if fecha is None else fecha
        medicamento['historial'].append(ahora)
        save_medicamentos(medicamentos)
        return f'Registro de toma para {nombre} a las {ahora}.'
    else:
        return f'Medicamento {nombre} no encontrado.'

# Función para ver el historial de tomas de un medicamento y calcular días restantes
def ver_historial(nombre):
    medicamentos = load_medicamentos()
    medicamento = next((med for med in medicamentos if med['nombre'] == nombre), None)
    if medicamento:
        inicio = medicamento['inicio']
        if isinstance(inicio, str):
            inicio = datetime.fromisoformat(inicio)
        else:
            return "Error: La fecha de inicio no está en el formato correcto."
        
        duracion = medicamento['diasRestantes']
        hoy = datetime.now()
        dias_pasados = (hoy - inicio).days
        dias_restantes = max(duracion - dias_pasados, 0)
        
        historial = medicamento['historial']
        return {
            'historial': historial,
            'dias_restantes': dias_restantes
        }
    else:
        return f'Medicamento {nombre} no encontrado.'

# Función para enviar notificaciones de recordatorio
def enviar_notificaciones():
    from plyer import notification

    while True:
        medicamentos = load_medicamentos()
        for medicamento in medicamentos:
            if medicamento['historial']:
                ultima_toma = datetime.fromisoformat(medicamento['historial'][-1])
                proxima_toma = ultima_toma + timedelta(hours=medicamento['frecuencia'])
                ahora = datetime.now()
                if ahora >= proxima_toma:
                    notification.notify(
                        title=f"Recordatorio de Medicamento: {medicamento['nombre']}",
                        message=f"Es hora de tomar tu medicamento: {medicamento['nombre']}",
                        timeout=10
                    )
                    # Registrar automáticamente la toma después de la notificación
                    registrar_toma(medicamento['nombre'])
            else:
                # Si no hay historial, programar desde la fecha de inicio
                inicio = datetime.fromisoformat(medicamento['inicio'])
                ahora = datetime.now()
                if ahora >= inicio:
                    notification.notify(
                        title=f"Recordatorio de Medicamento: {medicamento['nombre']}",
                        message=f"Es hora de tomar tu medicamento: {medicamento['nombre']}",
                        timeout=10
                    )
                    # Registrar automáticamente la toma después de la notificación
                    registrar_toma(medicamento['nombre'])
        time.sleep(60)  # Verificar cada minuto

# Configurar la aplicación Flask
app = Flask(__name__)

# Ruta para agregar un nuevo medicamento
@app.route('/medicamentos', methods=['POST'])
def api_agregar_medicamento():
    data = request.json
    nombre = data.get('nombre')
    frecuencia = data.get('frecuencia')
    inicio = data.get('inicio')
    duracion = data.get('duracion')
    return jsonify({'message': agregar_medicamento(nombre, frecuencia, inicio, duracion)})

# Ruta para registrar la toma de un medicamento
@app.route('/medicamentos/toma', methods=['POST'])
def api_registrar_toma():
    data = request.json
    nombre = data.get('nombre')
    fecha = data.get('fecha', None)
    return jsonify({'message': registrar_toma(nombre, fecha)})

# Ruta para ver el historial de tomas de un medicamento
@app.route('/medicamentos/historial', methods=['GET'])
def api_ver_historial():
    nombre = request.args.get('nombre')
    historial = ver_historial(nombre)
    return jsonify(historial)

# Iniciar el hilo de notificaciones
notificaciones_thread = Thread(target=enviar_notificaciones, daemon=True)
notificaciones_thread.start()

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)