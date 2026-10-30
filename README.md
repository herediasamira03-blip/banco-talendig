# Banco Talendig – API Inteligente de Solicitudes Bancarias

## 1. Descripción del proyecto

Banco Talendig es un proyecto educativo que consiste en desarrollar una API REST para gestionar solicitudes de apertura de cuentas bancarias.

La aplicación permite registrar, consultar, actualizar y eliminar solicitudes, validar los datos de los solicitantes mediante reglas de negocio y utilizar inteligencia artificial generativa para explicar los resultados de la evaluación y ofrecer recomendaciones orientativas sobre el tipo de cuenta solicitado.

La integración con Google Gemini permite generar explicaciones personalizadas a partir de la información registrada. Los resultados del análisis también se almacenan en la base de datos SQLite.

**Importante:** Este proyecto tiene fines exclusivamente académicos. No representa una herramienta bancaria real ni sustituye los procesos oficiales de evaluación financiera. Todas las pruebas deben realizarse con datos ficticios.

## 2. Tecnologías utilizadas

- **Python 3.10+:** lenguaje de programación.
- **FastAPI:** desarrollo de la API REST.
- **Pydantic:** validación de datos de entrada.
- **SQLAlchemy:** interacción con la base de datos.
- **SQLite:** almacenamiento de las solicitudes.
- **Google Gemini API:** generación de explicaciones mediante inteligencia artificial.
- **Google Gen AI SDK:** conexión con el servicio de Gemini.
- **uv:** gestión de dependencias y entorno del proyecto.
- **Uvicorn:** servidor para ejecutar la aplicación.

## 3. Reglas de negocio

La API aplica las siguientes condiciones para evaluar las solicitudes:

- Edad mínima del solicitante: 18 años.
- Salario anual mínimo requerido: RD$300,000.
- El salario anual se calcula multiplicando el salario mensual por 12.
- El solicitante debe cumplir ambas condiciones para satisfacer los criterios académicos de evaluación.
- Los tipos de cuenta permitidos son `ahorro` y `corriente`.

**Fórmula de cálculo:**

Salario anual = Salario mensual × 12.

## 4. Instalación y configuración

### Requisitos previos

- Python 3.10 o superior.
- uv instalado.
- Una clave de API de Google Gemini para utilizar la funcionalidad de inteligencia artificial.

### Pasos de instalación

1. Clonar o descargar el repositorio.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. Instalar las dependencias ejecutando:

```bash
uv sync
```

4. Crear un archivo llamado `.env` tomando como referencia `.env.example`.
5. Configurar las variables de entorno:

```env
GEMINI_API_KEY=tu_clave_privada_de_gemini
GEMINI_MODEL=gemini-3.8-flash
```

La clave debe obtenerse desde Google AI Studio. No debe compartirse ni publicarse en el repositorio.

## 5. Ejecución del proyecto

Desde la carpeta principal del proyecto, ejecutar:

```bash
uv run uvicorn main:app --reload
```

Cuando el servidor esté activo, se puede acceder a la documentación interactiva de Swagger mediante:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

La base de datos SQLite se crea automáticamente al iniciar la aplicación y permite conservar los registros de las solicitudes.

## 6. Endpoints disponibles

- Método HTTP: GET | Ruta: / | Funcionalidad: Verificar el inicio de la API.

- Método HTTP: POST | Ruta: /solicitudes | Funcionalidad: Registrar una nueva solicitud bancaria.

- Método HTTP: GET | Ruta: /solicitudes | Funcionalidad: Consultar todas las solicitudes registradas.

- Método HTTP: GET | Ruta: /solicitudes/{solicitud_id} | Funcionalidad: Consultar una solicitud por su identificador.

- Método HTTP: PUT | Ruta: /solicitudes/{solicitud_id} | Funcionalidad: Actualizar los datos de una solicitud existente.

- Método HTTP: DELETE | Ruta: /solicitudes/{solicitud_id} | Funcionalidad: Eliminar una solicitud.

- Método HTTP: POST | Ruta: /solicitudes/{solicitud_id}/analizar | Funcionalidad: Generar una explicación mediante Google Gemini y guardar el análisis en la base de datos SQLite.

## 7. Validaciones de datos

La API utiliza Pydantic para validar la información recibida antes de procesarla.

Las validaciones incluyen:

- **Nombre:** debe contener entre 2 y 80 caracteres.
- **Edad:** debe estar comprendida entre 18 y 100 años.
- **Salario mensual:** debe ser mayor que cero y no superar RD$10,000,000.
- **Tipo de cuenta:** únicamente admite `ahorro` o `corriente`.

También se aplican las reglas de negocio relacionadas con la edad mínima y el salario anual requerido.

### Códigos de respuesta

200: Operación realizada correctamente.
201: Solicitud creada exitosamente.
404: Solicitud no encontrada.
422: Los datos enviados no cumplen las validaciones establecidas.
502: Se produjo un error al comunicarse con el servicio de inteligencia artificial.
503: El servicio de inteligencia artificial no está disponible o la clave de acceso no está configurada.

## 8. Ejemplo de prueba en Swagger

Para registrar una solicitud, ingresar al endpoint `POST /solicitudes` y utilizar los siguientes datos ficticios:

```json
{
  "nombre": "Cliente Demo",
  "edad": 25,
  "salario_mensual": 35000,
  "tipo_cuenta": "ahorro"
}
```

El salario anual calculado será de RD$420,000, por lo que el solicitante cumple las condiciones académicas de edad y salario.

Una vez creada la solicitud, se debe copiar el identificador generado y utilizarlo para probar los demás endpoints.

Para ejecutar el análisis con inteligencia artificial, utilizar:

`POST /solicitudes/{solicitud_id}/analizar`

Este endpoint requiere una clave válida de Google Gemini configurada en el archivo `.env`. La API genera una explicación del resultado de la evaluación y almacena el análisis en la base de datos.


## 9. Estructura del proyecto

```text
banco-talendig/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── services.py
│
├── capturas/
│   ├── INSTRUCCIONES.txt
│   ├── docs-endpoints.png
│   ├── crear-solicitud.png
│   ├── consultar-solicitudes.png
│   ├── consultar-por-id.png
│   ├── actualizar-solicitud.png
│   ├── eliminar-solicitud.png
│   └── analizar-con-ia.png
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

**Nota:** El archivo `.env` se utiliza localmente y no debe incluirse en el repositorio. Las imágenes de la carpeta `capturas` deben corresponder a pruebas reales ejecutadas en la aplicación.

## 10. Seguridad y consideraciones

- La clave de Google Gemini se almacena en una variable de entorno.
- El archivo `.env` está excluido del control de versiones mediante `.gitignore`.
- No se deben publicar claves privadas ni credenciales.
- No se deben utilizar datos personales o financieros reales.
- La base de datos SQLite no debe compartirse si contiene información sensible.
- Las explicaciones generadas por inteligencia artificial son orientativas y tienen fines académicos.

## 11. Conclusión

El desarrollo de Banco Talendig permitió aplicar conocimientos de programación con Python, construcción de API REST, validación de datos, operaciones CRUD, persistencia mediante SQLite e integración de servicios de inteligencia artificial.

La incorporación de Google Gemini amplía las funcionalidades de la aplicación al permitir generar explicaciones automatizadas y personalizadas sobre los resultados de las evaluaciones.

El proyecto demuestra la integración de diferentes tecnologías para construir una solución funcional de gestión y análisis de solicitudes bancarias con fines educativos.