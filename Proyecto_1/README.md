# Proyecto 1 MLOPS

Desarrollado por **Grupo 3**.

Integrantes:
* Anthony Amaury Bossa
* José Luis Vega
* Víctor Andrés De La Hoz

## Desarrollo:
A continuación encontrará las instrucciones relacionadas con la solución del proyecto 1.

1. Clone el repositorio usando el comando:

    `git clone https://github.com/thonybossa/MLOPS.git`

2. Ubiquese en el directorio correspondiente al proyecto 1:

    `cd MLOPS/Proyecto_1`

3. Instale las dependencias necesarias para obtener los datos del proyecto usando el comando:

    `pip install -r requirements.txt`

4. Descargue los datos del proyecto usando el comando:

    `dvc pull`

    *Nota: En este caso los datos están almacenados en una carpeta de google drive, por lo que se abrirá automáticamente una ventana de autenticación de google drive. Ingrese con su cuenta de google y permita los accesos según sus preferencias.*

5. Ejecute desde la terminal el comando
    ```bash
    docker-compose up
    ```
    Automáticamente docker:
    * Revisará si la imagen tensorflow/tfx:1.12 existe en local, de lo contrario la traerá y la construirá.
    * Una vez construida la imagen, procederá con el levantado del contenedor en el puerto indicado. En este punto existen dos opciones:
        * Seguir el link que aparece al final en la terminal cuyo formato es:
        ```zsh
        http://127.0.0.1:8888/lab?token=<TOKEN>
        ```
    * Dirigirse a un buscador y escriba la dirección `localhost:8888` en la que se desplegará una web de jupyter en donde deberá colocar el token que aprece en el link mencionado anteriormente.

6. Ejecute cualquiera de los dos noteboks disponibles, en este caso la selección de características y el pipeline de datos están en dos notebooks diferentes. Tenga en cuenta que gracias a `dvc`, todos los archivos, existen en el directorio `data` y no es necesario descargarlos y/o generarlos de nuevo.