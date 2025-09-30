#==============================================#
#==TPI - Gestión de Datos de Países en Python==#
#==============================================#

#========# Importaciones ========#
from __future__ import annotations # Para compatibilidad con versiones anteriores de Python
import csv # Módulo para manejar archivos CSV
from typing import List, Dict, Literal, Iterable # Tipos de datos para anotaciones
#================================#

#========# Definición de Dict País ========#
#==nombre(str), poblacion(int), superficie(int), continente(str)==#
Registro = Dict[str, object] # Tipo de dato para representar un registro de país
#==========================================#

#=========================================================================#
#==Encabezados esperados en el CSV (en el orden que indica el enunciado)==#
#==Declarar CSV_FIELDS permite validar que el CSV tenga lo que necesitamos==#
CSV_FIELDS = ["nombre", "poblacion", "superficie", "continente"] #  Campos del CSV
#=========================================================================#

#=========================================================================#
#=========Funcion cargar_csv (con validaciones)===========================#
#==Recibe la ruta al archivo y devuelve una lista de diccionarios (Registro)==#
def cargar_csv(ruta: str) -> List[Registro]: 
   
    datos: List[Registro] = [] #=donde iremos guardando los países válidos.=#
    errores = 0 #=para contar cuántas filas se descartan (sirve para el resumen final)=#

    #==Bloque try Envuuelve todo el proceso de lectura para capturar==#
        # FileNotFoundError → ruta incorrecta/archivo inexistente.
        # ValueError → errores “esperables” como encabezados inválidos.
        # Exception general → cualquier otro problema de I/O/parsing inesperado.
        # Esto evita que el programa se caiga; en su lugar muestra un mensaje claro.

    try:
        #==Bloque with abre el archivo y asegura su cierre posterior==#
            # utf-8-sig permite leer CSVs con BOM sin que el primer encabezado quede “sucio”.
            # newline="" es la recomendación oficial del módulo csv para manejar saltos de línea de forma portable.

        with open(ruta, "r", encoding="utf-8-sig", newline="") as f:
            lector = csv.DictReader(f) #Convierte cada fila en un dict usando la primera fila como encabezados.
            faltantes = [c for c in CSV_FIELDS if c not in (lector.fieldnames or [])] #Verifica que todos los campos esperados estén presentes.
           #=Si faltan campos, lanza ValueError con detalles.=#

            if faltantes:
                raise ValueError(
                    f"Encabezados faltantes en CSV: {faltantes}. Se esperaban {CSV_FIELDS}"
                )
            #==Procesa cada fila del CSV.==#
            for i, fila in enumerate(lector, start=2):  # start=2 por encabezados en fila 1
                #==Valida y limpia cada campo.==#
                try:
                    nombre = (fila.get("nombre") or "").strip() #.get() maneja claves faltantes sin lanzar KeyError.
                    continente = (fila.get("continente") or "").strip() #.strip() elimina espacios en blanco al inicio y final.
                    if not nombre or not continente: # Valida que nombre y continente no estén vacíos.
                        raise ValueError("nombre/continente vacío") # Si están vacíos, lanza ValueError.

                    # Limpia y convierte población y superficie a enteros.
                    poblacion_str = (fila.get("poblacion") or "").replace("_", "").replace(" ", "") # Elimina guiones bajos y espacios.
                    superficie_str = (fila.get("superficie") or "").replace("_", "").replace(" ", "") # Elimina guiones bajos y espacios.
                    poblacion = int(poblacion_str) # Convierte a entero (lanza ValueError si no es posible).
                    superficie = int(superficie_str) # Convierte a entero (lanza ValueError si no es posible).

                    if poblacion < 0 or superficie <= 0: # Valida que población y superficie sean positivas.
                        raise ValueError("poblacion/superficie con valores no válidos") # Si no lo son, lanza ValueError.

                    #==Si todo es válido, agrega el registro a la lista.==#
                    datos.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente,
                    })
                except Exception as e: # Captura cualquier error en la fila actual.
                    errores += 1       # Incrementa el contador de errores.
                    print(f"[AVISO] Fila {i} inválida: {e}. Se omite.") # Muestra un aviso con el número de fila y el error.
    except FileNotFoundError: # Captura error si el archivo no se encuentra.
        print(f"[ERROR] No se encontró el archivo: {ruta}")
    except ValueError as ve:  # Captura errores de validación (como encabezados faltantes).
        print(f"[ERROR] CSV inválido: {ve}")
    except Exception as ex:   # Captura cualquier otro error inesperado.
        print(f"[ERROR] No se pudo leer el CSV ({type(ex).__name__}): {ex}")

    print(f"[OK] Registros cargados: {len(datos)}. Filas con error omitidas: {errores}.") # Resumen final.
    return datos # Devuelve la lista de registros válidos
#=========================================================================#

#================# Funcion normalizar_texto=================#
#==Normaliza texto para comparación insensible a mayúsculas/minúsculas y espacios==#
def normalizar_texto(s: str) -> str:

    return (s or "").strip().lower()
#===========================================================#

#================# Funcion buscar_por_nombre=================#
def buscar_por_nombre(datos: List[Registro], consulta: str) -> List[Registro]:
    q = normalizar_texto(consulta) # Normaliza la consulta para comparación
    if not q: # Si la consulta está vacía, devuelve una lista vacía
        return [] 
    return [r for r in datos if q in normalizar_texto(str(r.get("nombre", "")))] # Filtra los registros que contienen la consulta en el nombre
#============================================================#

#================# Función mostrar_registro =================#
#==Imprime un país en una línea legible==#
def mostrar_registro(r: Registro) -> None:
   
    print(
        f"- {r['nombre']} | Población: {r['poblacion']:,} | "
        f"Superficie: {r['superficie']:,} km² | Continente: {r['continente']}"
        .replace(",", ".")  # usar punto como separador de miles
    )
#==========================================================#

#======================MENU================================#


#================# Función menú principal =================#
#==========================================================#
 
#========== Menú principal (Iteración 1):==================#
def menu() -> None:
 
    datos: List[Registro] = [] # Lista para almacenar los registros cargados
    ruta_csv_por_defecto = "data/paises.csv" # Ruta por defecto del archivo CSV

    while True: # Bucle infinito hasta que el usuario decida salir
        print("\n=== GESTIÓN DE PAÍSES (Iteración 1) ===") # Título del menú
        print("1) Cargar CSV") # Opción para cargar el archivo CSV
        print("2) Buscar país por nombre (parcial o exacta)") # Opción para buscar un país por nombre
        print("3) Ver total de registros cargados") # Opción para ver el total de registros cargados
        print("4) Filtros") # Opción para acceder al submenú de filtros
        print("5) Ordenamientos") # Opción para acceder al submenú de ordenamientos
        print("6) Estadísticas") # Opción para acceder al submenú de estadísticas
        print("0) Salir") # Opción para salir del programa
        opcion = input("Elija una opción: ").strip() # Solicita al usuario que elija una opción

        if opcion == "1": # Si el usuario elige la opción 1
            ruta = input(f"Ingrese ruta CSV [Enter para '{ruta_csv_por_defecto}']: ").strip() # Solicita la ruta del archivo CSV
            if not ruta: # Si no se ingresa una ruta, usa la ruta por defecto
                ruta = ruta_csv_por_defecto # Usa la ruta por defecto
            datos = cargar_csv(ruta) # Carga los datos del archivo CSV

        elif opcion == "2": # Si el usuario elige la opción 2
            if not datos:   # Verifica si hay datos cargados
                print("[INFO] No hay datos cargados. Use la opción 1 primero.") # Informa al usuario que no hay datos cargados
                continue
            q = input("Nombre a buscar (parcial o exacto): ").strip() # Solicita el nombre a buscar
            resultados = buscar_por_nombre(datos, q) # Busca los países que coinciden con el nombre ingresado
            if resultados: # Si se encontraron resultados
                print(f"[OK] Se encontraron {len(resultados)} coincidencia(s):") # Informa la cantidad de coincidencias encontradas
                for r in resultados: # Itera sobre los resultados encontrados
                    mostrar_registro(r) # Muestra cada registro encontrado
            else: # Si no se encontraron resultados
                print("[INFO] No se encontraron países para esa búsqueda.") # Informa al usuario que no se encontraron países

        elif opcion == "3": # Si el usuario elige la opción 3
            print(f"[INFO] Total de registros cargados: {len(datos)}") # Muestra el total de registros cargados

        elif opcion == "4": # Si el usuario elige la opción 4
            submenu_filtros(datos) # Llama al submenú de filtros

        elif opcion == "5": # Si el usuario elige la opción 5
            submenu_ordenamientos(datos) # Llama al submenú de ordenamientos

        elif opcion == "6": # Si el usuario elige la opción 6
            submenu_estadisticas(datos) # Llama al submenú de estadísticas

        elif opcion == "0": # Si el usuario elige la opción 0
            print("¡Hasta luego!") 
            break # Sale del bucle y termina el programa

        else: # Si el usuario ingresa una opción inválida
            print("[ERROR] Opción inválida. Intente nuevamente.") # Informa al usuario que la opción es inválida
#==========================================================#

#======Sub menú para Estadísticas (Iteración 2)============#
def submenu_estadisticas(datos: List[Registro]) -> None:
    if not datos: # Verifica si hay datos cargados
        print("[INFO] No hay datos cargados. Use la opción 1 del menú principal.") # Informa al usuario que no hay datos cargados
        return # Sale de la función

    while True: # Bucle infinito hasta que el usuario decida volver
        print("\n--- Estadísticas ---") # Título del submenú de estadísticas
        print("1) País con mayor y menor población") # Opción para ver el país con mayor y menor población
        print("2) Promedio de población") # Opción para ver el promedio de población
        print("3) Promedio de superficie (km²)") # Opción para ver el promedio de superficie
        print("4) Cantidad de países por continente") # Opción para ver la cantidad de países por continente
        print("5) Mostrar TODO el resumen") # Opción para ver todas las estadísticas en un resumen
        print("0) Volver") # Opción para volver al menú principal
        op = input("Elija una opción: ").strip() # Solicita al usuario que elija una opción

        if op == "0": # Si el usuario elige la opción 0
            break # Sale del bucle y vuelve al menú principal

        elif op == "1": # Si el usuario elige la opción 1
            mayor, menor = pais_mayor_menor_poblacion(datos) # Obtiene el país con mayor y menor población
            if mayor and menor: # Si se encontraron países
                print("[OK] País con MAYOR población:") 
                mostrar_registro(mayor) # Muestra el país con mayor población
                print("[OK] País con MENOR población:")
                mostrar_registro(menor) # Muestra el país con menor población
            else:  # Si no se encontraron países
                print("[INFO] No hay datos suficientes.") # Informa al usuario que no hay datos suficientes

        elif op == "2": # Si el usuario elige la opción 2
            prom = promedio_poblacion(datos) # Calcula el promedio de población
            if prom is None: # Si no hay datos suficientes
                print("[INFO] No hay datos suficientes.") # Informa al usuario que no hay datos suficientes
            else: # Si se pudo calcular el promedio
                print(f"[OK] Promedio de población: {prom:,.2f}".replace(",", ".")) # Muestra el promedio de población

        elif op == "3": # Si el usuario elige la opción 3
            prom = promedio_superficie(datos) # Calcula el promedio de superficie
            if prom is None: # Si no hay datos suficientes
                print("[INFO] No hay datos suficientes.") # Informa al usuario que no hay datos suficientes
            else: # Si se pudo calcular el promedio
                print(f"[OK] Promedio de superficie (km²): {prom:,.2f}".replace(",", ".")) # Muestra el promedio de superficie

        elif op == "4": # Si el usuario elige la opción 4
            conteo = conteo_por_continente(datos) # Cuenta la cantidad de países por continente
            if not conteo: # Si no hay datos suficientes
                print("[INFO] No hay datos suficientes.") # Informa al usuario que no hay datos suficientes
            else: # Si se pudo contar los países por continente
                print("[OK] Cantidad de países por continente:") # Muestra la cantidad de países por continente
                for cont, cant in conteo.items(): # Itera sobre cada continente y su cantidad
                    print(f"- {cont}: {cant}") # Muestra el continente y la cantidad de países

        elif op == "5": # Si el usuario elige la opción 5
            mostrar_estadisticas_resumen(datos) # Muestra todas las estadísticas en un resumen

        else: # Si el usuario ingresa una opción inválida
            print("[ERROR] Opción inválida. Intente nuevamente.") # Informa al usuario que la opción es inválida
#==========================================================#

#======Sub menú para Ordenamientos (Iteración 2)===========# 
def submenu_ordenamientos(datos: List[Registro]) -> None:
    if not datos: # Verifica si hay datos cargados
        print("[INFO] No hay datos cargados. Use la opción 1 del menú principal.") # Informa al usuario que no hay datos cargados
        return # Sale de la función

    while True: # Bucle infinito hasta que el usuario decida volver
        print("\n--- Ordenamientos ---") # Título del submenú de ordenamientos
        print("1) Por nombre") # Opción para ordenar por nombre
        print("2) Por población") # Opción para ordenar por población
        print("3) Por superficie") # Opción para ordenar por superficie
        print("0) Volver") # Opción para volver al menú principal
        op = input("Elija una opción: ").strip() # Solicita al usuario que elija una opción

        if op == "0": # Si el usuario elige la opción 0
            break

        if op not in {"1", "2", "3"}: # Si la opción no es válida
            print("[ERROR] Opción inválida. Intente nuevamente.") # Informa al usuario que la opción es inválida
            continue

        # mapear opción a campo
        campo = {"1": "nombre", "2": "poblacion", "3": "superficie"}[op]  # campo a ordenar

        sentido = input("Orden (A = ascendente, D = descendente) [A/D]: ").strip().lower() # Solicita el sentido del ordenamiento
        descendente = True if sentido == "d" else False  # default ascendente

        ordenados = ordenar_paises(datos, campo, descendente) # Ordena los registros según el campo y el sentido especificados

        # Mostrar resultados (limitar para no inundar la consola)
        print(f"[OK] Mostrando primeros resultados ordenados por {campo} ({'desc' if descendente else 'asc'}):") # Informa el criterio de ordenamiento
        limite = 50 # Limita la cantidad de resultados a mostrar
        for r in ordenados[:limite]: # Itera sobre los primeros resultados ordenados
            mostrar_registro(r) # Muestra cada registro ordenado
        if len(ordenados) > limite: # Si hay más resultados que el límite
            print(f"[INFO] Mostrando {limite} de {len(ordenados)}. Refine con filtros o cambie el orden.") # Informa que solo se muestran los primeros resultados
#==========================================================#

#======Sub menú para Filtrado Avanzado (Iteración 2)=======#
def submenu_filtros(datos: List[Registro]) -> None:
    if not datos: # Verifica si hay datos cargados
        print("[INFO] No hay datos cargados. Use la opción 1 del menú principal.")
        return

    while True: # Bucle infinito hasta que el usuario decida volver
        print("\n--- Filtros ---") # Título del submenú de filtros
        print("1) Por continente (igualdad exacta)") # Opción para filtrar por continente
        print("2) Por rango de población") # Opción para filtrar por rango de población
        print("3) Por rango de superficie") # Opción para filtrar por rango de superficie
        print("0) Volver") # Opción para volver al menú principal
        op = input("Elija una opción: ").strip() # Solicita al usuario que elija una opción

        if op == "1": # Si el usuario elige la opción 1
            cont = input("Ingrese continente (ej: América, Europa, Asia, África, Oceanía): ").strip() # Solicita el continente a filtrar
            res = filtrar_por_continente(datos, cont) # Filtra los registros por continente
            if res: # Si se encontraron resultados
                print(f"[OK] {len(res)} resultado(s):") # Informa la cantidad de resultados encontrados
                for r in res[:50]:  # Limitar impresión por consola
                    mostrar_registro(r) # Muestra cada registro encontrado
                if len(res) > 50: # Si hay más de 50 resultados
                    print(f"[INFO] Mostrando 50 de {len(res)}. Refine el filtro para ver menos.") # Informa que solo se muestran los primeros 50 resultados
            else: # Si no se encontraron resultados
                print("[INFO] Sin resultados para ese continente.") # Informa al usuario que no se encontraron resultados

        elif op == "2": # Si el usuario elige la opción 2
            txt = input("Rango de población (ej: 1_000_000-5_000_000, >=2000000, <=800000, 3000000): ").strip() # Solicita el rango de población a filtrar
            rango = parsear_rango_num(txt) # Parsea el rango ingresado
            if not rango: # Si el rango no es válido
                print("[ERROR] Formato de rango inválido.") # Informa al usuario que el formato es inválido
                continue # Vuelve al inicio del bucle
            res = filtrar_por_poblacion(datos, rango) # Filtra los registros por rango de población
            if res: # Si se encontraron resultados
                print(f"[OK] {len(res)} resultado(s):") # Informa la cantidad de resultados encontrados
                for r in res[:50]: # Limitar impresión por consola
                    mostrar_registro(r) # Muestra cada registro encontrado
                if len(res) > 50: # Si hay más de 50 resultados
                    print(f"[INFO] Mostrando 50 de {len(res)}. Refine el filtro para ver menos.") # Informa que solo se muestran los primeros 50 resultados
            else: # Si no se encontraron resultados
                print("[INFO] Sin resultados para ese rango de población.") # Informa al usuario que no se encontraron resultados

        elif op == "3": # Si el usuario elige la opción 3
            txt = input("Rango de superficie en km² (ej: 500000-2000000, >=1000000, <=800000, 300000): ").strip() # Solicita el rango de superficie a filtrar
            rango = parsear_rango_num(txt) # Parsea el rango ingresado
            if not rango: # Si el rango no es válido
                print("[ERROR] Formato de rango inválido.") # Informa al usuario que el formato es inválido
                continue # Vuelve al inicio del bucle
            res = filtrar_por_superficie(datos, rango) # Filtra los registros por rango de superficie
            if res: # Si se encontraron resultados
                print(f"[OK] {len(res)} resultado(s):") # Informa la cantidad de resultados encontrados
                for r in res[:50]: # Limitar impresión por consola
                    mostrar_registro(r) # Muestra cada registro encontrado
                if len(res) > 50: # Si hay más de 50 resultados
                    print(f"[INFO] Mostrando 50 de {len(res)}. Refine el filtro para ver menos.") # Informa que solo se muestran los primeros 50 resultados
            else: # Si no se encontraron resultados
                print("[INFO] Sin resultados para ese rango de superficie.") # Informa al usuario que no se encontraron resultados

        elif op == "0": # Si el usuario elige la opción 0
            break # Sale del bucle y vuelve al menú principal
        else:  # Si el usuario ingresa una opción inválida
            print("[ERROR] Opción inválida. Intente nuevamente.") # Informa al usuario que la opción es inválida
#==========================================================#


#======Funciones para Rangos Numericos (Iteración 2)======#

#================# Función parsear_rango_num =================#
#     Convierte expresiones de rango a (min, max):
#       '1000-5000' -> (1000, 5000)
#       '>=2000'    -> (2000, None)
#       '<=8000'    -> (None, 8000)
#       '3000'      -> (3000, 3000)
#     Devuelve None si el formato no es válido.
#=============================================================#    
def parsear_rango_num(texto: str) -> tuple[int | None, int | None] | None: 
    
    if not texto: # Si el texto está vacío, devuelve None
        return None
    s = texto.strip().replace(" ", "") # Elimina espacios en blanco al inicio, final y entre números
    try: # Intenta parsear el rango
        if "-" in s: # rango 'min-max'
            a, b = s.split("-", 1) # Divide en dos partes
            mn, mx = int(a), int(b) # Convierte a enteros
            if mn > mx: # Valida que el mínimo no sea mayor que el máximo
                return None # Si es inválido, devuelve None
            return (mn, mx) # Devuelve el rango como tupla (min, max)
        if s.startswith(">="): # rango '>=min'
            return (int(s[2:]), None) # Devuelve (min, None)
        if s.startswith("<="): # rango '<=max'
            return (None, int(s[2:])) # Devuelve (None, max)
        # número exacto
        v = int(s) # Convierte a entero
        return (v, v) # Devuelve (v, v) para número exacto
    except Exception: # Captura cualquier error durante el parseo
        return None # Si hay un error, devuelve None
#=============================================================# 

#================# Función filtrar_por_continente =================#
#==filtra por igualdad de continente (case-insensitive, tolerando espacios)==#
def filtrar_por_continente(datos: List[Registro], continente: str) -> List[Registro]: 
    q = (continente or "").strip().lower() # Normaliza el continente para comparación
    if not q: # Si el continente está vacío, devuelve una lista vacía
        return [] 
    return [r for r in datos if (str(r["continente"]).strip().lower() == q)] # Filtra los registros por continente
#=================================================================#

#================# Función filtrar_por_poblacion =================#
#==filtra por rango de población (min, max) donde min o max pueden ser None==#
def filtrar_por_poblacion(datos: List[Registro], rango: tuple[int | None, int | None]) -> List[Registro]:
    mn, mx = rango # Desempaqueta el rango en min y max
    res: List[Registro] = [] # Lista para almacenar los registros que cumplen el criterio
    for r in datos: # Itera sobre cada registro en los datos
        p = int(r["poblacion"]) # Obtiene la población del registro
        if mn is not None and p < mn: # Si hay un mínimo y la población es menor, continúa al siguiente registro
            continue
        if mx is not None and p > mx: # Si hay un máximo y la población es mayor, continúa al siguiente registro
            continue
        res.append(r) # Si cumple los criterios, agrega el registro a la lista de resultados
    return res # Devuelve la lista de registros que cumplen el criterio
#=================================================================#

#================# Función filtrar_por_superficie =================#
#==filtra por rango de superficie (min, max) donde min o max pueden ser None==#
def filtrar_por_superficie(datos: List[Registro], rango: tuple[int | None, int | None]) -> List[Registro]:
    mn, mx = rango # Desempaqueta el rango en min y max
    res: List[Registro] = [] # Lista para almacenar los registros que cumplen el criterio
    for r in datos: # Itera sobre cada registro en los datos
        s = int(r["superficie"]) # Obtiene la superficie del registro
        if mn is not None and s < mn: # Si hay un mínimo y la superficie es menor, continúa al siguiente registro
            continue
        if mx is not None and s > mx: # Si hay un máximo y la superficie es mayor, continúa al siguiente registro
            continue
        res.append(r) # Si cumple los criterios, agrega el registro a la lista de resultados
    return res # Devuelve la lista de registros que cumplen el criterio
#=================================================================#

#================# Tipo para campos de ordenamiento =================#
#==========================================================#
CampoOrden = Literal["nombre", "poblacion", "superficie"] # Tipo para los campos de ordenamiento
#==========================================================#

#================# Función ordenar_paises =================#
# 
#     Ordena y devuelve una NUEVA lista, no modifica el original.
#     - campo: 'nombre' | 'poblacion' | 'superficie'
#     - descendente: False = ascendente, True = descendente
#==========================================================#
def ordenar_paises(datos: Iterable[Registro], campo: CampoOrden, descendente: bool = False) -> list[Registro]:
    return sorted(list(datos), key=lambda r: clave_orden(r, campo), reverse=descendente)
#==========================================================#

#================# Función clave_orden =================#
#  
#     Devuelve el valor comparable para ordenar:
#       - nombre: usa .casefold() para ignorar mayúsculas y acentos de forma robusta
#       - poblacion/superficie: asegura tipo int
#=======================================================#
def clave_orden(reg: Registro, campo: str):
    if campo == "nombre": # Si el campo es "nombre"
        return str(reg["nombre"]).casefold() # Devuelve el nombre en minúsculas para ordenamiento insensible a mayúsculas
    if campo == "poblacion": # Si el campo es "poblacion"
        return int(reg["poblacion"]) # Devuelve la población como entero para ordenamiento numérico
    if campo == "superficie": # Si el campo es "superficie"
        return int(reg["superficie"]) # Devuelve la superficie como entero para ordenamiento numérico
    raise ValueError("Campo de orden no válido (use: nombre, poblacion o superficie)") # Si el campo no es válido, lanza un error
#=======================================================#

#================# Función pais_mayor_menor_poblacion =======================#
#==Devuelve el país con mayor y menor población en una tupla (mayor, menor)==#
def pais_mayor_menor_poblacion(datos: List[Registro]) -> tuple[Registro | None, Registro | None]:
    if not datos: # Si no hay datos,
        return None, None # devuelve (None, None)
    mayor = max(datos, key=lambda r: int(r["poblacion"])) # Encuentra el país con mayor población
    menor = min(datos, key=lambda r: int(r["poblacion"])) # Encuentra el país con menor población
    return mayor, menor  # Devuelve una tupla con el país de mayor y menor población
#============================================================================#

#================# Función promedio_poblacion ======================#
#==Devuelve el promedio simple de población. None si no hay datos.==#
def promedio_poblacion(datos: List[Registro]) -> float | None:
    if not datos: # Si no hay datos,
        return None # devuelve None
    return sum(int(r["poblacion"]) for r in datos) / len(datos) # Calcula y devuelve el promedio de población
#===================================================================#

#================# Función promedio_superficie ===================#
#==Promedio simple de superficie (km²). None si no hay datos.==#
def promedio_superficie(datos: List[Registro]) -> float | None:
    if not datos: # Si no hay datos, devuelve None
        return None # Devuelve None si no hay datos
    return sum(int(r["superficie"]) for r in datos) / len(datos) # Calcula y devuelve el promedio de superficie
#=================================================================#

#================# Función conteo_por_continente =================#
#==Cantidad de países por continente (case-sensitive tal como vienen cargados).==#
def conteo_por_continente(datos: List[Registro]) -> dict[str, int]:
    conteo: dict[str, int] = {} # Diccionario para almacenar el conteo por continente
    for r in datos: # Itera sobre cada registro en los datos
        cont = str(r["continente"]) # Obtiene el continente del registro
        conteo[cont] = conteo.get(cont, 0) + 1 # Incrementa el conteo para el continente
    return conteo # Devuelve el diccionario con el conteo por continente
#=================================================================#

#================# Función mostrar_estadisticas_resumen =================#
#==Muestra todas las estadísticas pedidas por el TPI en un bloque compacto.==
def mostrar_estadisticas_resumen(datos: List[Registro]) -> None:
    mayor, menor = pais_mayor_menor_poblacion(datos) # Obtener país con mayor y menor población
    prom_pob = promedio_poblacion(datos) # Calcular promedio de población
    prom_sup = promedio_superficie(datos) # Calcular promedio de superficie
    conteo = conteo_por_continente(datos) # Contar países por continente

    if not datos: # Verifica si hay datos cargados
        print("[INFO] No hay datos cargados para calcular estadísticas.")  # Informa al usuario que no hay datos cargados
        return

    print("\n=== ESTADÍSTICAS ===") # Título de la sección de estadísticas
    if mayor and menor: # Si se encontraron países con mayor y menor población
        print("• País con MAYOR población:") # Mostrar país con mayor población
        mostrar_registro(mayor) # Muestra el país con mayor población
        print("• País con MENOR población:") # Mostrar país con menor población
        mostrar_registro(menor) # Muestra el país con menor población
    print(f"• Promedio de población: {prom_pob:,.2f}".replace(",", ".")) # Mostrar promedio de población
    print(f"• Promedio de superficie (km²): {prom_sup:,.2f}".replace(",", ".")) # Mostrar promedio de superficie
    print("• Cantidad de países por continente:") # Mostrar cantidad de países por continente
    for cont, cant in conteo.items(): # Itera sobre cada continente y su cantidad
        print(f"  - {cont}: {cant}") # Muestra el continente y la cantidad de países
#========================================================================#

















































#================# Punto de entrada principal =================#
if __name__ == "__main__": # Punto de entrada principal
    menu()  # Llama a la función del menú principal
#==============================================================#
