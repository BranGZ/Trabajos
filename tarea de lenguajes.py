# --- 1. IMPORTACIONES ---
# Importamos las librerías que usaremos
from pathlib import Path # Para manejar rutas de archivos y carpetas
from datetime import datetime # Para convertir texto en fechas y horas
import csv # Para leer el archivo .csv
import json # Para escribir el archivo .json

# --- 2. CONFIGURACIÓN INICIAL ---
# Definimos la ruta donde está nuestro archivo de datos
ruta = Path("actividad_2.csv")

# --- 3. INICIALIZACIÓN DE VARIABLES ACUMULADORAS ---
# Preparamos todas las variables que "llenaremos" mientras leemos el archivo.

# Contador para el total de registros (Punto 9)
# Usamos un contador en lugar de una lista para ahorrar memoria.
total_registros = 0 

# --- Variables para el Punto 3 (Conteo de días) ---
conteo_de_dias = {}
dias_de_la_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

# --- Variables para Puntos 5, 7, 9 (Conteos de campeones) ---
conteo_campeon_mas_entreno = {} # Punto 5: Conteo total de campeones
conteo_campeon_fin_de_semana = {} # Punto 7: Conteo de campeones solo en finde
conteo_por_dia_campeon = {} # Punto 9: Diccionario anidado (día -> campeón -> conteo)

# --- Variables para el Punto 4 (Fechas min/max) ---
primer_dia_de_entrenamiento = None
ultimo_dia_de_entrenamiento = None

# Pre-llenamos los diccionarios que dependen de los días
# Así evitamos errores al intentar sumar en una llave que no existe
for dia in dias_de_la_semana:
    conteo_de_dias[dia] = 0 # Deja listo {'lunes': 0, 'martes': 0, ...}
    conteo_por_dia_campeon[dia] = {} # Deja listo {'lunes': {}, 'martes': {}, ...}


# --- 4. PROCESAMIENTO PRINCIPAL (UN ÚNICO BUCLE) ---
# Usamos 'with open' para que el archivo se abra y cierre automáticamente
with ruta.open("r", encoding="utf-8") as f:
    # Usamos DictReader para que cada fila sea un diccionario (fila['campeon'])
    reader_csv = csv.DictReader(f)

    for fila in reader_csv:
        # --- Conteo de Registros (para Punto 9) ---
        # Sumamos 1 por cada fila que leemos
        total_registros += 1

        # --- Punto 2: Procesamiento de Fechas ---
        fecha = fila['timestamp'] # Obtenemos el texto de la fecha
        formato = "%Y-%m-%d %H:%M" # Definimos el formato en que viene
        # Convertimos el texto en un objeto 'datetime' real
        objeto_datetime = datetime.strptime(fecha, formato)
        # Obtenemos el día de la semana (0=Lunes, 6=Domingo)
        dia = objeto_datetime.weekday()


        # Guardamos el objeto 'datetime' completo en la fila (útil para el futuro)
        fila['timestamp_datetime'] = objeto_datetime
        # Guardamos el número del día (0-6) en la fila
        fila['numero_dia'] = dia
        # Guardamos el nombre del día (ej. 'lunes') en la fila
        fila['nombre_dia'] = dias_de_la_semana[dia].lower()
        

       # --- Punto 3: Conteo de Días ---
        # Usamos el número 'dia' (0-6) para obtener el nombre (ej. 'lunes')
        # y sumamos 1 al contador de ese día.
        conteo_de_dias[dias_de_la_semana[dia]] += 1

        # --- Punto 4: Búsqueda de Fechas Min/Max ---
        # Obtenemos solo la fecha (sin hora) de la fila actual
        fecha_actual = objeto_datetime.date()
        
        # Revisa si es la primera fila que leemos
        if primer_dia_de_entrenamiento is None:
            # Si es la primera, es el inicio y el fin por ahora
            primer_dia_de_entrenamiento = fecha_actual
            ultimo_dia_de_entrenamiento = fecha_actual
        else:
            # Si no es la primera, comparamos
            # Buscamos una fecha más antigua (menor)
            if fecha_actual < primer_dia_de_entrenamiento:
                primer_dia_de_entrenamiento = fecha_actual
            # Buscamos una fecha más reciente (mayor)
            if fecha_actual > ultimo_dia_de_entrenamiento:
                ultimo_dia_de_entrenamiento = fecha_actual

        # --- Punto 5: Conteo Total de Campeones ---
        # Obtenemos el nombre del campeón de esta fila
        campeon_actual = fila['campeon']
        
        # Chequeamos si ya lo hemos contado antes
        if campeon_actual not in conteo_campeon_mas_entreno:
            # Si es la primera vez, lo inicializamos en 1
            conteo_campeon_mas_entreno[campeon_actual] = 1
        else:
            # Si ya existe, solo le sumamos 1
            conteo_campeon_mas_entreno[campeon_actual] += 1

        # --- Punto 7: Conteo de Campeones (Solo Fin de Semana) ---
        # 1. Filtramos: esta lógica solo se ejecuta si el día es 'sabado' O 'domingo'
        if fila['nombre_dia'] == 'sabado' or fila['nombre_dia'] == 'domingo':
            
            # 2. Hacemos el mismo conteo del Punto 5, pero en el diccionario del finde
            if campeon_actual not in conteo_campeon_fin_de_semana:
                conteo_campeon_fin_de_semana[campeon_actual] = 1
            else:
                conteo_campeon_fin_de_semana[campeon_actual] += 1

        # --- Punto 9: Conteo Anidado (Día -> Campeón) ---
        # 1. Obtenemos el diccionario INTERNO que corresponde a este día
        #    (ej. la variable apunta al {'lunes': {}} )
        campeones_del_dia = conteo_por_dia_campeon[fila['nombre_dia']]

        # 2. Contamos el campeón DENTRO de ese diccionario interno
        if campeon_actual not in campeones_del_dia:
            campeones_del_dia[campeon_actual] = 1
        else:
            campeones_del_dia[campeon_actual] += 1


# --- 5. ANÁLISIS Y RESULTADOS (POST-BUCLE) ---

# --- Punto 3: Día/s con más sesiones ---
print("--- Punto 3: Día/s con más sesiones ---")

# 1. Ordenamos el diccionario 'conteo_de_dias'
#    Usamos .items() para obtener pares (dia, conteo)
lista_dias_ordenada = sorted(
    conteo_de_dias.items(),
    key=lambda item: item[1],  # Ordenamos por el conteo (el segundo elemento, item[1])
    reverse=True               # De mayor a menor
)

# 2. Obtenemos el número máximo (está en el primer ítem, en la posición [1])
max_sesiones = lista_dias_ordenada[0][1]

# 3. Filtramos la lista ordenada (con "Comprensión de Listas")
#    Nos quedamos solo con los días (dia[0])
#    cuyo conteo (dia[1]) sea igual al máximo
dias_ganadores = [
    dia[0] 
    for dia in lista_dias_ordenada 
    if dia[1] == max_sesiones     
]

print(f"La cantidad máxima de entrenamientos en un dia fue: {max_sesiones}")
print(f"El/los día/s con mas entrenamientos fueron: {dias_ganadores}")

# --- Punto 4: Días transcurridos ---
print("--- Punto 4: Días transcurridos ---")

# Restamos las fechas que encontramos en el bucle
diferencia_dias = ultimo_dia_de_entrenamiento - primer_dia_de_entrenamiento
# Obtenemos la cantidad de días de esa diferencia
dias_transcurridos = diferencia_dias.days

print(f"En total pasaron: {dias_transcurridos}")

# --- Punto 5: Campeón con más sesiones ---
print("--- Punto 5: Campeón con más sesiones ---")
# 1. Ordenamos el diccionario de campeones, igual que con los días
lista_ordenada = sorted(
    conteo_campeon_mas_entreno.items(),   
    key=lambda item: item[1],           
    reverse=True                        
)
# 2. El ganador es el primer ítem de la lista (ej. ('Thresh', 72))
campeon_ganador = lista_ordenada[0] 

print(f"El campeón que más entrenó fue: {campeon_ganador[0]} con {campeon_ganador[1]} sesiones")

# --- Punto 6: Promedio por día ---
print("--- Punto 6: Promedio por día ---")
# 1. Calculamos el total de semanas
total_semanas = dias_transcurridos/7

# 2. Creamos una 'lambda' que toma un par (item)
#    y devuelve un par nuevo (dia, promedio)
funcion_promedio = lambda item: (
    item[0],  # Mantenemos el día (item[0])
    round(item[1] / total_semanas, 2) # Calculamos y redondeamos el promedio
)

# 3. 'map' aplica esa función a CADA ítem de 'conteo_de_dias'
lista_de_promedios = list(
    map(funcion_promedio, conteo_de_dias.items())
)

# 4. Convertimos la lista de pares de vuelta en un diccionario
promedios_por_dia_map = dict(lista_de_promedios)

print(f"Promedio de entrenamientos por dia: {promedios_por_dia_map}")


# --- Punto 7: Campeón de Fin de Semana ---
print("--- Punto 7: Campeón de Fin de Semana ---")
# (Usamos el método de 'max' y 'for' para mostrar otra forma)
# 1. Encontramos el número máximo de sesiones del finde
max_finde = max(conteo_campeon_fin_de_semana.values())
campeon_finde = []
# 2. Recorremos el diccionario del finde
for campeon, conteo_especifico in conteo_campeon_fin_de_semana.items():
    # 3. Buscamos a todos los que empaten con el máximo
    if conteo_especifico == max_finde:
        campeon_finde.append(campeon)
print(f"El campeon que mas entrena los findes es: {campeon_finde}")

# --- 6. GENERACIÓN DE ARCHIVOS (Puntos 8 y 9) ---

# --- Punto 8: Creando archivo CSV ---
print("--- Punto 8: Creando archivo CSV ---")
# 1. Definimos la ruta de la carpeta de salida
ruta_salida = Path('salida')
# 2. Creamos la carpeta (exist_ok=True para evitar errores si ya existe)
ruta_salida.mkdir(exist_ok=True)
# 3. Definimos la ruta completa del archivo CSV
path_csv = ruta_salida / 'campeon.csv'

# 4. Abrimos el CSV en modo 'w' (escritura)
#    'newline=""' es importante para que no haga filas en blanco
with path_csv.open("w", newline='', encoding='utf-8') as archivo_csv:
    # 5. Creamos un "escritor" de CSV
    writer_csv = csv.writer(archivo_csv)
    # 6. Escribimos la fila del encabezado (los títulos)
    writer_csv.writerow(['campeon', 'cantidad'])

    # 7. Recorremos el diccionario de campeones
    for campeon, cantidad in conteo_campeon_mas_entreno.items():
        # 8. Escribimos una fila por cada campeón
        writer_csv.writerow([campeon, cantidad])

# --- Punto 9: Creando archivo JSON ---
print("--- Punto 9: Creando archivo JSON ---")
# 1. Armamos el diccionario final que pide el enunciado
datos_para_json = {}
# 2. 'total_registros' lo contamos en el bucle principal
datos_para_json['total_registros'] = total_registros
# 3. 'conteo_por_dia_campeon' lo llenamos en el bucle principal
datos_para_json['detalle_por_dia'] = conteo_por_dia_campeon

# 3. Definimos la ruta del archivo JSON
path_del_json = ruta_salida / 'detalle.json'
# 4. Abrimos el JSON en modo 'w' (escritura)
with open(path_del_json, 'w', encoding='utf-8') as archivo_json:
    # 5. Usamos json.dump() para "volcar" nuestro diccionario al archivo
    #    'indent=4' hace que el JSON quede ordenado y legible
    json.dump(datos_para_json, archivo_json, indent=4)

print("Proceso completado.")    



