# Proyecto de Consulta de Propiedades Inmobiliarias

Este proyecto consiste en desarrollar un servidor HTTP que permita realizar consultas sobre propiedades inmobiliarias almacenadas en una base de datos. El servidor responderá a las solicitudes GET con información sobre propiedades que coincidan con los parámetros proporcionados en la URL.

## Tecnologías Utilizadas

- Python: Utilizaremos Python como lenguaje de programación principal para desarrollar el servidor HTTP.
- BaseHTTPRequestHandler: Utilizaremos la clase BaseHTTPRequestHandler de la biblioteca http.server para manejar las solicitudes HTTP entrantes.
- Mysql: Utilizaremos SQLite como base de datos para almacenar la información sobre las propiedades inmobiliarias.
- JSON: Utilizaremos el formato JSON para la comunicación de datos entre el servidor y el cliente.
- Pydancti:  es una librería de validación de datos y serialización en Python que te permite definir y validar modelos de datos de forma sencilla y declarativa.

## Enfoque de Desarrollo

1. **Diseño del Servidor HTTP**: Implementaremos un servidor HTTP utilizando la clase BaseHTTPRequestHandler para manejar las solicitudes GET entrantes. Definiremos métodos para manejar diferentes tipos de solicitudes y estableceremos la lógica para procesar y responder a estas solicitudes.

2. **Conexión a la Base de Datos**: Implementaremos una función para establecer una conexión a la base de datos SQLite que contiene la información sobre las propiedades inmobiliarias.

3. **Consulta de Propiedades**: Desarrollaremos consultas SQL para recuperar la información de las propiedades inmobiliarias según los parámetros proporcionados en la URL de la solicitud GET. Procesaremos estos parámetros y construiremos consultas dinámicas para filtrar los resultados de la base de datos.

4. **Respuesta al Cliente**: Convertiremos los resultados de las consultas a formato JSON y los enviaremos como respuesta al cliente. Manejaremos diferentes escenarios, como la presencia o ausencia de resultados y la validación de los parámetros de entrada.

5. **Manejo de Errores**: Implementaremos el manejo de errores para manejar situaciones como la falta de conexión a la base de datos, solicitudes incorrectas o errores internos del servidor. Utilizaremos códigos de estado HTTP apropiados y mensajes de error descriptivos para informar al cliente sobre el estado de la solicitud.

6. **Validacion de los Datos**: Implementamos el manejo de datos al momento en el que el cliente ingresa los datos atraves de los query paramters. se uso la libreria pydantic que nos ayuda con que los datos sean correctos y estén bien formados.

## Filtros de la API

Aquí se describen los filtros que se pueden utilizar al hacer consultas a la API. Se espera que estos filtros sean enviados desde el front-end para filtrar los resultados de la consulta.

```json
{
  "filtros": {
    "year": {
      "tipo": "rango",
      "descripcion": "Filtrar por año de construcción"
    },
    "city": {
      "tipo": "texto",
      "descripcion": "Filtrar por ciudad"
    },
    "state": {
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
3. Ejecuta el servidor utilizando el comando `python main.py`.
4. Realiza solicitudes GET al servidor especificando los parámetros deseados en la URL.
5. El endpoint con el que se puede acceder a la api es http://localhost:8000/get_and_search/

## Ejecución de los Tests

1. **Navega al Directorio del Proyecto Donde se encuentra el archivo de los tests**: Cambia al directorio del proyecto clonado.

    ```bash
    cd prueba_habi/consulta_inmuebles
    ```

2. **Ejecuta los Tests**: Utiliza el módulo `unittest` para ejecutar los tests. Reemplaza `mytest.py` con el nombre del archivo que contiene tus tests.

    ```bash
    python -m unittest mytest.py
    ```

    Esto ejecutará todos los tests definidos en el archivo `mytest.py` y mostrará el resultado en la consola.

# Servicio de “Me gusta”

## Diagrama de Entidad-Relación

![Diagrama ER](https://raw.githubusercontent.com/oscarjsv/prueba_habi/main/assets/UML%20diagrams.png)

## Código SQL

```sql
CREATE TABLE Usuario (
    id INT PRIMARY KEY,
    nombre VARCHAR(255),
    email VARCHAR(255),
    -- otros atributos necesarios
);

CREATE TABLE Inmueble (
    id INT PRIMARY KEY,
    direccion VARCHAR(255),
    ciudad VARCHAR(255),
    estado VARCHAR(255),
    precio_venta DECIMAL,
    descripcion TEXT,
    -- otros atributos necesarios
);

CREATE TABLE MeGusta (
    id INT PRIMARY KEY,
    usuario_id INT,
    inmueble_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (inmueble_id) REFERENCES Inmueble(id)
);
```
## Descripcion

Creé el diagrama de Entidad-Relación y el código SQL de esta manera tras considerar el tipo de relación entre un usuario y un inmueble. En este diseño, un usuario puede dar "me gusta" a muchos inmuebles, y a su vez, un inmueble puede recibir "me gusta" de muchos usuarios. Además, la base de datos está diseñada para mantener un registro histórico de todos los "me gusta" que cada usuario ha dado a diferentes inmuebles. Esto implica la necesidad de rastrear y almacenar quién dio el "me gusta" (el usuario registrado), a qué inmueble se le dio el "me gusta" y cuándo se dio el "me gusta".

En este modelo, cada entidad tiene una llave primaria. Las llaves foráneas presentes en la entidad "MeGusta" son el ID del usuario y el ID del inmueble, lo que establece la relación entre un usuario y un inmueble.