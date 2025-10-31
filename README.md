# Práctica 2 - Análisis de Datos con Python

Este repositorio contiene la resolución de la Práctica 2 de Lenguajes de Programación, enfocada en el análisis de datos de un archivo CSV usando Python.

El script `tarea de lenguajes.py` lee un archivo CSV (`actividad_2.csv`), procesa los datos en una sola pasada, realiza un análisis completo y genera dos archivos de salida en una carpeta `salida/`.

## 🚀 Características Principales

El script principal (`tarea de lenguajes.py`) realiza las siguientes tareas:

* **Procesamiento Eficiente:** Lee el archivo CSV una única vez para realizar todos los cálculos, ahorrando memoria y tiempo.
* **Análisis de Sesiones:**
    * Encuentra el/los día/s de la semana con más sesiones.
    * Calcula el promedio de sesiones por día de la semana.
* **Análisis de Campeones:**
    * Identifica al campeón con más entrenamientos en total.
    * Identifica al campeón que más entrena los fines de semana.
* **Análisis de Fechas:**
    * Calcula el total de días transcurridos entre el primer y último entrenamiento.
* **Programación Funcional:** Utiliza `lambda`, `sorted` y `map` para realizar análisis de datos de forma concisa (Puntos 5 y 6).
* **Generación de Salidas:** Crea una carpeta `salida/` con dos archivos:
    1.  `campeon.csv`: Un listado de cada campeón y su cantidad total de sesiones.
    2.  `detalle.json`: Un resumen que incluye el total de registros y un desglose anidado del conteo de cada campeón por cada día de la semana.

## 🛠️ Cómo Ejecutar el Proyecto

1.  **Clonar el repositorio** (o descargar los archivos):
    ```bash
    git clone [https://github.com/BranGZ/Trabajos.git](https://github.com/BranGZ/Trabajos.git)
    cd Trabajos
    ```

2.  **Tener los archivos:** Asegúrate de tener los siguientes archivos en la misma carpeta:
    * `tarea de lenguajes.py` (el script principal)
    * `actividad_2.csv` (los datos de entrada)

3.  **Ejecutar el script:**
    ```bash
    python "tarea de lenguajes.py"
    ```

4.  **Verificar la salida:**
    * El script imprimirá los resultados de los análisis (Puntos 3 al 7) en la consola.
    * Se creará una nueva carpeta `salida/` que contendrá los archivos `campeon.csv` y `detalle.json`.
