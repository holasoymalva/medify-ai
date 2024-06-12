# Medify-AI : API de Gestión de Medicamentos

Esta es una API RESTful para gestionar el registro de medicamentos y enviar notificaciones para recordar cuándo tomar tus medicamentos, creada con Flask.

Nota : La version V1 solo cuenta con el consumo y seguimiento de manera local. La version V2 ya cuenta con una integracion a una base de datos en tiempo real y gestion personalizada de usuario. Y la version V3 se encuentra en desarrollo con una integracion a GEMINY para una mejor experiencia en la gestion de la informacion y facilidad de uso.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Rutas de la API](#rutas-de-la-api)
- [Ejemplos de uso](#ejemplos-de-uso)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/holasoymalva/medify-ai.git
   cd medify-ai
   ```
2. Crea un entorno virtual e instala las dependencias:
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
   ```
## Uso

1. Ejecuta la aplicación Flask:
   ```bash
    python app.py
   ```
2. La API estará disponible en http://127.0.0.1:5000.

## Rutas de la API

### Agregar un nuevo medicamento
* URL: /medicamentos
* Método: POST
* Descripción: Agrega un nuevo medicamento.
* Cuerpo de la solicitud:
   ```json
    {
        "nombre": "Nombre del Medicamento",
        "frecuencia": 8,
        "inicio": "YYYY-MM-DDTHH:MM:SS",
        "duracion": 5
    }
   ```

###   Registrar la toma de un medicamento
* URL: /medicamentos/toma
* Método: POST
* Descripción: Registra la toma de un medicamento.
* Cuerpo de la solicitud:
   ```json
    {
        "nombre": "Nombre del Medicamento",
        "fecha": "YYYY-MM-DDTHH:MM:SS"  // Opcional
    }
   ```
