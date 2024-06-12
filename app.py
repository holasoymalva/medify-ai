import json
import os
from datetime import datetime, timedelta

# Ruta del archivo JSON
FILE_PATH = 'medicamentos.json'

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
    print(f'Medicamento {nombre} agregado con frecuencia de {frecuencia} horas, inicio del tratamiento el {inicio} y duración de {duracion} días.')

# Función para registrar la toma de un medicamento
def registrar_toma(nombre, fecha=None):
    medicamentos = load_medicamentos()
    medicamento = next((med for med in medicamentos if med['nombre'] == nombre), None)
    if medicamento:
        ahora = datetime.now().isoformat() if fecha is None else fecha
        medicamento['historial'].append(ahora)
        save_medicamentos(medicamentos)
        print(f'Registro de toma para {nombre} a las {ahora}.')
    else:
        print(f'Medicamento {nombre} no encontrado.')

# Función para ver el historial de tomas de un medicamento y calcular días restantes
def ver_historial(nombre):
    medicamentos = load_medicamentos()
    medicamento = next((med for med in medicamentos if med['nombre'] == nombre), None)
    if medicamento:
        inicio = medicamento['inicio']
        if isinstance(inicio, str):
            inicio = datetime.fromisoformat(inicio)
        else:
            print("Error: La fecha de inicio no está en el formato correcto.")
            return
        
        duracion = medicamento['diasRestantes']
        hoy = datetime.now()
        dias_pasados = (hoy - inicio).days
        dias_restantes = max(duracion - dias_pasados, 0)
        
        print(f'Historial de tomas para {nombre}:')
        for index, toma in enumerate(medicamento['historial']):
            print(f'{index + 1}. {toma}')
        print(f'Días restantes del tratamiento: {dias_restantes}')
    else:
        print(f'Medicamento {nombre} no encontrado.')

# Ejemplos de uso
if __name__ == '__main__':
    while True:
        print("\n1. Agregar Medicamento")
        print("2. Registrar Toma de Medicamento")
        print("3. Ver Historial de Medicamento")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del medicamento: ")
            frecuencia = int(input("Ingrese la frecuencia de toma en horas: "))
            inicio = input("Ingrese la fecha de inicio del tratamiento (YYYY-MM-DDTHH:MM:SS): ")
            duracion = int(input("Ingrese la duración del tratamiento en días: "))
            agregar_medicamento(nombre, frecuencia, inicio, duracion)
        elif opcion == '2':
            nombre = input("Ingrese el nombre del medicamento: ")
            registrar_toma(nombre)
        elif opcion == '3':
            nombre = input("Ingrese el nombre del medicamento: ")
            ver_historial(nombre)
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intente nuevamente.")