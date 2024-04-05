# Proyecto de Consulta de Propiedades Inmobiliarias

Este proyecto consiste en desarrollar un servidor HTTP que permita realizar consultas sobre propiedades inmobiliarias almacenadas en una base de datos. El servidor responderá a las solicitudes GET con información sobre propiedades que coincidan con los parámetros proporcionados en la URL.

## Tecnologías Utilizadas

- Python: Utilizaremos Python como lenguaje de programación principal para desarrollar el servidor HTTP.
- BaseHTTPRequestHandler: Utilizaremos la clase BaseHTTPRequestHandler de la biblioteca http.server para manejar las solicitudes HTTP entrantes.
- Mysql: Utilizaremos SQLite como base de datos para almacenar la información sobre las propiedades inmobiliarias.
- JSON: Utilizaremos el formato JSON para la comunicación de datos entre el servidor y el cliente.

## Enfoque de Desarrollo

1. **Diseño del Servidor HTTP**: Implementaremos un servidor HTTP utilizando la clase BaseHTTPRequestHandler para manejar las solicitudes GET entrantes. Definiremos métodos para manejar diferentes tipos de solicitudes y estableceremos la lógica para procesar y responder a estas solicitudes.

2. **Conexión a la Base de Datos**: Implementaremos una función para establecer una conexión a la base de datos SQLite que contiene la información sobre las propiedades inmobiliarias.

3. **Consulta de Propiedades**: Desarrollaremos consultas SQL para recuperar la información de las propiedades inmobiliarias según los parámetros proporcionados en la URL de la solicitud GET. Procesaremos estos parámetros y construiremos consultas dinámicas para filtrar los resultados de la base de datos.

4. **Respuesta al Cliente**: Convertiremos los resultados de las consultas a formato JSON y los enviaremos como respuesta al cliente. Manejaremos diferentes escenarios, como la presencia o ausencia de resultados y la validación de los parámetros de entrada.

5. **Manejo de Errores**: Implementaremos el manejo de errores para manejar situaciones como la falta de conexión a la base de datos, solicitudes incorrectas o errores internos del servidor. Utilizaremos códigos de estado HTTP apropiados y mensajes de error descriptivos para informar al cliente sobre el estado de la solicitud.

## Filtros de la API

Aquí se describen los filtros que se pueden utilizar al hacer consultas a la API. Se espera que estos filtros sean enviados desde el front-end para filtrar los resultados de la consulta.

```json
{
  "filtros": {
    "año_construccion": {
      "tipo": "rango",
      "descripcion": "Filtrar por año de construcción (rango de años)"
    },
    "ciudad": {
      "tipo": "texto",
      "descripcion": "Filtrar por ciudad"
    },
    "estado_propiedad": {
      "tipo": "opciones",
      "descripcion": "Filtrar por estado de la propiedad",
      "opciones": ["pre_venta", "en_venta", "vendido"]
    }
  }
}
```
## Dudas

No se si dokerizar la aplicacion o no estoy pensandolo

## Ejecución del Proyecto

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando `pip install -r requirements.txt`.
3. Ejecuta el servidor utilizando el comando `python server.py`.
4. Realiza solicitudes GET al servidor especificando los parámetros deseados en la URL.


## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.