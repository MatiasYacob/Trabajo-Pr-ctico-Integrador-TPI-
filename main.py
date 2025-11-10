

# ████████╗██████╗░░█████╗░██████╗░░█████╗░░░░░░██╗░█████╗░
# ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗░░░░░██║██╔══██╗
# ░░░██║░░░██████╔╝███████║██████╦╝███████║░░░░░██║██║░░██║
# ░░░██║░░░██╔══██╗██╔══██║██╔══██╗██╔══██║██╗░░██║██║░░██║
# ░░░██║░░░██║░░██║██║░░██║██████╦╝██║░░██║╚█████╔╝╚█████╔╝
# ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░

# ██╗███╗░░██╗████████╗███████╗░██████╗░██████╗░░█████╗░██████╗░░█████╗░██████╗░
# ██║████╗░██║╚══██╔══╝██╔════╝██╔════╝░██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
# ██║██╔██╗██║░░░██║░░░█████╗░░██║░░██╗░██████╔╝███████║██║░░██║██║░░██║██████╔╝
# ██║██║╚████║░░░██║░░░██╔══╝░░██║░░╚██╗██╔══██╗██╔══██║██║░░██║██║░░██║██╔══██╗
# ██║██║░╚███║░░░██║░░░███████╗╚██████╔╝██║░░██║██║░░██║██████╔╝╚█████╔╝██║░░██║
# ╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝


#========# Importaciones ========#

import csv # Módulo para manejar archivos CSV
import os # Módulo para operaciones del sistema operativo

#================================#


#==============================#
#==Helpers==#
def es_entero(texto: object) -> bool:
    """
    True si texto representa un entero válido sin usar excepciones.
    Acepta signo opcional (+/-). Ignora espacios alrededor.
    """
    s = str(texto).strip()
    if s == "":
        return False
    if s[0] in "+-":
        s = s[1:]
    return s.isdigit()
#================# Funcion normalizar_texto=================#
#==Normaliza texto para comparación insensible a mayúsculas/minúsculas y espacios==#
def normalizar_texto(s: str) -> str:

    return (s or "").strip().lower()
#===========================================================#
#================# Función parsear_rango_num =================# 
def _entero_sin_sep(s: str) -> tuple[bool, int]:
    if s == "":
        return (False, 0)
    t = s.replace("_", "").replace(" ", "")
    if t[0] in "+-":
        signo = t[0]
        t = t[1:]
        if not t.isdigit():
            return (False, 0)
        v = int(t)
        return (True, v if signo != "-" else -v)
    if t.isdigit():
        return (True, int(t))
    return (False, 0)


#================# Función clave_orden =================#

def clave_orden(reg: dict[str, object], campo: str):
    if campo not in campos_orden_validos():
        # Si se llama directo sin validar
        return ""  # valor neutro para no romper
    if campo == "nombre":
        return str(reg.get("nombre", "")).casefold()
    if campo == "poblacion":
        return int(str(reg.get("poblacion", "0")).replace("_","").replace(" ","") or "0")
    return int(str(reg.get("superficie", "0")).replace("_","").replace(" ","") or "0")

def campos_csv() -> list[str]:
    # Encabezados válidos del archivo CSV
    return ["nombre", "poblacion", "superficie", "continente"]

def campos_orden_validos() -> tuple[str, ...]:
    # Campos permitidos para ordenar (sin usar globals)
    return ("nombre", "poblacion", "superficie")













#=========================================================================#
#=========Funcion cargar_csv (con validaciones)===========================#
#==Recibe la ruta al archivo y devuelve una lista de diccionarios (dict[str, object])==#
#==============================================#
# Cargar CSV 
#==============================================#
def cargar_csv(ruta: str) -> list[dict[str, object]]:
    datos: list[dict[str, object]] = []
    errores = 0

    # 1) Validar existencia del archivo
    if not isinstance(ruta, str) or ruta.strip() == "":
        print("[ERROR] Ruta inválida.")
        return datos
    if not os.path.exists(ruta):
        print(f"[ERROR] No se encontró el archivo: {ruta}")
        return datos

    # 2) Abrir archivo (asumimos sistema en condiciones; si falla, no usamos excepciones)
    f = open(ruta, "r", encoding="utf-8-sig", newline="")  # evitar BOM en encabezados
    lector = csv.DictReader(f)

    # 3) Validar encabezados requeridos
    fieldnames = lector.fieldnames if lector.fieldnames is not None else []
    faltantes = [c for c in campos_csv() if c not in fieldnames]

    if len(faltantes) > 0:
        print(f"[ERROR] Encabezados faltantes: {faltantes}. Se esperaban: {campos_csv()}")
        return datos

    # 4) Procesar filas con validaciones sin excepciones
    fila_nro = 1  # encabezados
    for fila in lector:
        fila_nro += 1
        # a) Campos de texto requeridos
        nombre = str(fila.get("nombre", "")).strip()
        continente = str(fila.get("continente", "")).strip()
        if nombre == "" or continente == "":
            errores += 1
            print(f"[AVISO] Fila {fila_nro} inválida: nombre/continente vacío. Se omite.")
            continue

        # b) Normalizar números (quitar guiones bajos y espacios internos)
        poblacion_txt = str(fila.get("poblacion", "")).replace("_", "").replace(" ", "").strip()
        superficie_txt = str(fila.get("superficie", "")).replace("_", "").replace(" ", "").strip()

        # c) Validar formato numérico sin excepciones
        if not es_entero(poblacion_txt) or not es_entero(superficie_txt):
            errores += 1
            print(f"[AVISO] Fila {fila_nro} inválida: población/superficie no numérica. Se omite.")
            continue

        poblacion = int(poblacion_txt)
        superficie = int(superficie_txt)

        # d) Reglas de negocio (rangos)
        if poblacion < 0:
            errores += 1
            print(f"[AVISO] Fila {fila_nro} inválida: población negativa. Se omite.")
            continue
        if superficie <= 0:
            errores += 1
            print(f"[AVISO] Fila {fila_nro} inválida: superficie <= 0. Se omite.")
            continue

        # e) Si todo está bien, agregar dict[str, object]
        datos.append({
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente,
        })

    # 5) Cerrar archivo y reportar
    f.close()
    print(f"[OK] registros cargados: {len(datos)}. Filas con error omitidas: {errores}.")
    return datos

#========================================#
# Guardar CSV
#========================================#
def guardar_csv(ruta: str, datos: list[dict[str, object]]) -> None:
    """
    Sobrescribe el archivo CSV 'ruta' con el contenido de 'datos',
    respetando los encabezados: nombre,poblacion,superficie,continente.
    No usa try/except: valida precondiciones antes de escribir.
    """
    # 1) Validar ruta
    if not isinstance(ruta, str) or ruta.strip() == "":
        print("[ERROR] Ruta inválida.")
        return
    ruta = ruta.strip()
    dirpath = os.path.dirname(ruta) or "."
    if not os.path.isdir(dirpath):
        print(f"[ERROR] La carpeta de destino no existe: {dirpath}")
        return

    # 2) Validar datos y tipos antes de escribir
    if not isinstance(datos, list) or len(datos) == 0:
        print("[INFO] No hay datos para guardar.")
        return

    # Validar que cada dict[str, object] tenga las claves y tipos correctos
    for idx, r in enumerate(datos, start=1):
        if not isinstance(r, dict):
            print(f"[ERROR] registro {idx} no es un dict. Cancelando guardado.")
            return
        for k in ("nombre", "poblacion", "superficie", "continente"):
            if k not in r:
                print(f"[ERROR] registro {idx} sin campo requerido: {k}. Cancelando guardado.")
                return

        # Coerción defensiva sin excepciones
        nombre = str(r.get("nombre", "")).strip()
        continente = str(r.get("continente", "")).strip()
        pob_txt = str(r.get("poblacion", "")).strip()
        sup_txt = str(r.get("superficie", "")).strip()

        if nombre == "" or continente == "":
            print(f"[ERROR] registro {idx} con nombre/continente vacío. Cancelando guardado.")
            return
        # permitir 1_000_000 y espacios internos
        pob_txt = pob_txt.replace("_", "").replace(" ", "")
        sup_txt = sup_txt.replace("_", "").replace(" ", "")

        if not es_entero(pob_txt) or not es_entero(sup_txt):
            print(f"[ERROR] registro {idx} con población/superficie no numérica. Cancelando guardado.")
            return
        if int(pob_txt) < 0 or int(sup_txt) <= 0:
            print(f"[ERROR] registro {idx} con valores fuera de rango. Cancelando guardado.")
            return

    # 3) Escritura (asumimos que el sistema permitirá abrir y escribir el archivo)
    f = open(ruta, "w", encoding="utf-8", newline="")
    writer = csv.DictWriter(f, fieldnames=campos_csv())
    writer.writeheader()
    for r in datos:
        writer.writerow({
            "nombre": str(r.get("nombre", "")).strip(),
            "poblacion": int(str(r.get("poblacion", "")).replace("_","").replace(" ","") or "0"),
            "superficie": int(str(r.get("superficie", "")).replace("_","").replace(" ","") or "0"),
            "continente": str(r.get("continente", "")).strip(),
        })
    print(f"[OK] Cambios guardados en: {ruta}")
#========================================#







#=========================#
# Continentes (opciones)
#=========================#
def _canon_continentes(datos: list[dict[str, object]]) -> list[str]:
    """
    Devuelve una lista de continentes 'canonizados' a partir de los datos ya cargados,
    respetando mayúsculas/acentos según aparecen en el CSV.
    Si hay variantes (ej. 'América', 'america'), usa la primera que encuentre.
    """
    vistos: dict[str, str] = {}
    for r in datos:
        raw = str(r.get("continente", "")).strip()
        if not raw:
            continue
        key = raw.lower()
        if key not in vistos:
            vistos[key] = raw
    # ordenar por forma mostrada (estética; no afecta la “canonicidad”)
    return sorted(vistos.values(), key=lambda s: s.casefold())

def elegir_continente(datos: list[dict[str, object]]) -> str:
    """
    Muestra un menú con continentes existentes y permite elegir uno.
    Incluye la opción 'Otro' para escribir manualmente.
    """
    opciones = _canon_continentes(datos)
    if not opciones:
        # fallback: si no hay datos, pedir texto libre
        cont = input("Continente: ").strip()
        return cont

    print("\nSeleccione continente:")
    for i, c in enumerate(opciones, start=1):
        print(f"{i}) {c}")
    print(f"{len(opciones)+1}) Otro (ingresar manualmente)")

    while True:
        sel = input(f"Opción [1-{len(opciones)+1}]: ").strip()
        if sel.isdigit():
            n = int(sel)
            if 1 <= n <= len(opciones):
                return opciones[n-1]
            if n == len(opciones) + 1:
                cont = elegir_continente(datos).strip()
                return cont
        print("[ERROR] Opción inválida. Intente nuevamente.")





#================# Función mostrar_registro[str, object] =================#
#==Imprime un país en una línea legible==#
def mostrar_registro(r: dict[str, object]) -> None:
    print(
        f"- {r['nombre']} | Población: {r['poblacion']:,} | "
        f"Superficie: {r['superficie']:,} km² | Continente: {r['continente']}"
        .replace(",", ".")
    )

#==========================================================#






#======================MENU================================#
#================# Función menú principal =================#
#==========================================================#
#========== Menú principal (Iteración 1):==================#
def menu() -> None:
 
    datos: list[dict[str, object]] = [] # Lista para almacenar los dict[str, object]s cargados
    ruta_csv_por_defecto = "data/paises.csv" # Ruta por defecto del archivo CSV
    ruta_actual = None  # Variable para almacenar la ruta actual del CSV cargado

    while True: # Bucle infinito hasta que el usuario decida salir
        print("\n=== GESTIÓN DE PAÍSES (Iteración 1) ===") # Título del menú
        print("1) Cargar CSV") # Opción para cargar el archivo CSV
        print("2) Buscar país por nombre (parcial o exacta)") # Opción para buscar un país por nombre
        print("3) Ver total de registros cargados") # Opción para ver el total de dict[str, object]s cargados
        print("4) Filtros") # Opción para acceder al submenú de filtros
        print("5) Ordenamientos") # Opción para acceder al submenú de ordenamientos
        print("6) Estadísticas") # Opción para acceder al submenú de estadísticas
        print("7) Agregar país")  
        print("8) Guardar cambios en CSV")  # debajo del "7) Agregar país"
        print("9) Actualizar país (población y superficie)")

        print("0) Salir") # Opción para salir del programa
        opcion = input("Elija una opción: ").strip() # Solicita al usuario que elija una opción

        if opcion == "1": # Si el usuario elige la opción 1
            ruta = input(f"Ingrese ruta CSV [Enter para '{ruta_csv_por_defecto}']: ").strip() # Solicita la ruta del archivo CSV
            if not ruta: # Si no se ingresa una ruta, usa la ruta por defecto
                ruta = ruta_csv_por_defecto # Usa la ruta por defecto
            datos = cargar_csv(ruta) # Carga los datos del archivo CSV
            ruta_actual = ruta  # Actualiza la ruta actual del CSV cargado

        elif opcion == "2": # Si el usuario elige la opción 2
            if not datos:   # Verifica si hay datos cargados
                print("[INFO] No hay datos cargados. Use la opción 1 primero.") # Informa al usuario que no hay datos cargados
                continue
            q = input("Nombre a buscar (parcial o exacto): ").strip() # Solicita el nombre a buscar
            modo = input("Modo (P=parcial / E=exacta) [P/E]: ").strip().lower()
            modo_final = "exacta" if modo == "e" else "parcial"
            resultados = buscar_por_nombre(datos, q, modo_final) # Busca los países que coinciden con el nombre ingresado
            if resultados: # Si se encontraron resultados
                print(f"[OK] Se encontraron {len(resultados)} coincidencia(s):") # Informa la cantidad de coincidencias encontradas
                for r in resultados: # Itera sobre los resultados encontrados
                    mostrar_registro(r) # Muestra cada dict[str, object] encontrado
            else: # Si no se encontraron resultados
                print("[INFO] No se encontraron países para esa búsqueda.") # Informa al usuario que no se encontraron países

        elif opcion == "3": # Si el usuario elige la opción 3
            print(f"[INFO] Total de registros cargados: {len(datos)}") # Muestra el total de dict[str, object]s cargados

        elif opcion == "4": # Si el usuario elige la opción 4
            submenu_filtros(datos) # Llama al submenú de filtros

        elif opcion == "5": # Si el usuario elige la opción 5
            submenu_ordenamientos(datos) # Llama al submenú de ordenamientos

        elif opcion == "6": # Si el usuario elige la opción 6
            submenu_estadisticas(datos) # Llama al submenú de estadísticas

        elif opcion == "7": # Si el usuario elige la opción 7
            if not datos:   # Verifica si hay datos cargados
                print("[INFO] No hay datos cargados. Use la opción 1 primero.") # Informa al usuario que no hay datos cargados
                continue
            agregar_pais(datos) # Llama a la función para agregar un país
            if ruta_actual:
                guardar_csv(ruta_actual, datos)  # Guarda los cambios automáticamente si hay una ruta actual
            else:
                print("[INFO] No hay ruta de CSV asociada aún. Use la opción 8 o cargue primero con la opción 1.")
        elif opcion == "8":  # Si el usuario elige la opción 8
            if not datos:   # Verifica si hay datos cargados
                print("[INFO] No hay datos cargados. Use la opción 1 primero.") # Informa al usuario que no hay datos cargados
            elif not ruta_actual:  # Verifica si hay una ruta actual
                print("[INFO] No hay ruta de CSV asociada. Use la opción 1 para cargar un archivo primero.") # Informa al usuario que no hay una ruta actual
            else:
                guardar_csv(ruta_actual, datos) # Guarda los cambios en el archivo CSV
        elif opcion == "9":  # Si el usuario elige la opción 9
            if not datos:   # Verifica si hay datos cargados
                print("[INFO] No hay datos cargados. Use la opción 1 primero.") # Informa al usuario que no hay datos cargados
                continue
            actualizar_pais(datos)  # Llama a la función para actualizar un país
            if ruta_actual:
                guardar_csv(ruta_actual, datos)  # Guarda los cambios automáticamente si hay una ruta actual
            else:
                print("[INFO] No hay ruta de CSV asociada aún. Use la opción 8 o cargue primero con la opción 1.")  


        elif opcion == "0": # Si el usuario elige la opción 0
            print("¡Hasta luego!") 
            break # Sale del bucle y termina el programa
        
        else: # Si el usuario ingresa una opción inválida
            print("[ERROR] Opción inválida. Intente nuevamente.") # Informa al usuario que la opción es inválida
#==========================================================#
#======Sub menú para Estadísticas (Iteración 2)============#
def submenu_estadisticas(datos: list[dict[str, object]]) -> None:
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
def submenu_ordenamientos(datos: list[dict[str, object]]) -> None:
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

        ordenados = ordenar_paises(datos, campo, descendente) # Ordena los dict[str, object]s según el campo y el sentido especificados

        # Mostrar resultados (limitar para no inundar la consola)
        print(f"[OK] Mostrando primeros resultados ordenados por {campo} ({'desc' if descendente else 'asc'}):") # Informa el criterio de ordenamiento
        limite = 50 # Limita la cantidad de resultados a mostrar
        for r in ordenados[:limite]: # Itera sobre los primeros resultados ordenados
            mostrar_registro(r) # Muestra cada dict[str, object] ordenado
        if len(ordenados) > limite: # Si hay más resultados que el límite
            print(f"[INFO] Mostrando {limite} de {len(ordenados)}. Refine con filtros o cambie el orden.") # Informa que solo se muestran los primeros resultados
#==========================================================#
#======Sub menú para Filtrado Avanzado (Iteración 2)=======#
def submenu_filtros(datos: list[dict[str, object]]) -> None:
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
            cont =elegir_continente(datos).strip() # Solicita el continente a filtrar
            res = filtrar_por_continente(datos, cont) # Filtra los dict[str, object]s por continente
            if res: # Si se encontraron resultados
                print(f"[OK] {len(res)} resultado(s):") # Informa la cantidad de resultados encontrados
                for r in res[:50]:  # Limitar impresión por consola
                    mostrar_registro(r) # Muestra cada dict[str, object] encontrado
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
            res = filtrar_por_poblacion(datos, rango) # Filtra los dict[str, object]s por rango de población
            if res: # Si se encontraron resultados
                print(f"[OK] {len(res)} resultado(s):") # Informa la cantidad de resultados encontrados
                for r in res[:50]: # Limitar impresión por consola
                    mostrar_registro(r) # Muestra cada dict[str, object] encontrado
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
            res = filtrar_por_superficie(datos, rango) # Filtra los dict[str, object]s por rango de superficie
            if res: # Si se encontraron resultados
                print(f"[OK] {len(res)} resultado(s):") # Informa la cantidad de resultados encontrados
                for r in res[:50]: # Limitar impresión por consola
                    mostrar_registro(r) # Muestra cada dict[str, object] encontrado
                if len(res) > 50: # Si hay más de 50 resultados
                    print(f"[INFO] Mostrando 50 de {len(res)}. Refine el filtro para ver menos.") # Informa que solo se muestran los primeros 50 resultados
            else: # Si no se encontraron resultados
                print("[INFO] Sin resultados para ese rango de superficie.") # Informa al usuario que no se encontraron resultados

        elif op == "0": # Si el usuario elige la opción 0
            break # Sale del bucle y vuelve al menú principal
        else:  # Si el usuario ingresa una opción inválida
            print("[ERROR] Opción inválida. Intente nuevamente.") # Informa al usuario que la opción es inválida
#==========================================================#









#======Funciones para Rangos Numericos ======#

#================# Función filtrar_por_continente =================#
#==filtra por igualdad de continente (case-insensitive, tolerando espacios)==#
def filtrar_por_continente(datos: list[dict[str, object]], continente: str) -> list[dict[str, object]]: 
    q = (continente or "").strip().lower() # Normaliza el continente para comparación
    if not q: # Si el continente está vacío, devuelve una lista vacía
        return [] 
    return [r for r in datos if (str(r["continente"]).strip().lower() == q)] # Filtra los dict[str, object]s por continente
#=================================================================#

#================# Función filtrar_por_poblacion =================#
#==filtra por rango de población (min, max) donde min o max pueden ser None==#
def filtrar_por_poblacion(datos: list[dict[str, object]], rango: tuple[int | None, int | None]) -> list[dict[str, object]]:
    mn, mx = rango # Desempaqueta el rango en min y max
    res: list[dict[str, object]] = [] # Lista para almacenar los dict[str, object]s que cumplen el criterio
    for r in datos: # Itera sobre cada dict[str, object] en los datos
        p = int(r["poblacion"]) # Obtiene la población del dict[str, object]
        if mn is not None and p < mn: # Si hay un mínimo y la población es menor, continúa al siguiente dict[str, object]
            continue
        if mx is not None and p > mx: # Si hay un máximo y la población es mayor, continúa al siguiente dict[str, object]
            continue
        res.append(r) # Si cumple los criterios, agrega el dict[str, object] a la lista de resultados
    return res # Devuelve la lista de dict[str, object]s que cumplen el criterio
#=================================================================#

#================# Función filtrar_por_superficie =================#
#==filtra por rango de superficie (min, max) donde min o max pueden ser None==#
def filtrar_por_superficie(datos: list[dict[str, object]], rango: tuple[int | None, int | None]) -> list[dict[str, object]]:
    mn, mx = rango # Desempaqueta el rango en min y max
    res: list[dict[str, object]] = [] # Lista para almacenar los dict[str, object]s que cumplen el criterio
    for r in datos: # Itera sobre cada dict[str, object] en los datos
        s = int(r["superficie"]) # Obtiene la superficie del dict[str, object]
        if mn is not None and s < mn: # Si hay un mínimo y la superficie es menor, continúa al siguiente dict[str, object]
            continue
        if mx is not None and s > mx: # Si hay un máximo y la superficie es mayor, continúa al siguiente dict[str, object]
            continue
        res.append(r) # Si cumple los criterios, agrega el dict[str, object] a la lista de resultados
    return res # Devuelve la lista de dict[str, object]s que cumplen el criterio
#=================================================================#

#================# Función ordenar_paises =================#
#     Ordena y devuelve una NUEVA lista, no modifica el original.
#==========================================================#
def ordenar_paises(datos: list[dict[str, object]], campo: str, descendente: bool = False) -> list[dict[str, object]]:
    """
    Devuelve una NUEVA lista ordenada por 'campo' si es válido.
    Campos válidos: nombre, poblacion, superficie.
    """
    if campo not in campos_orden_validos():
        print(f"[ERROR] Campo de orden no válido. Use uno de: {list(campos_orden_validos())}")
        return []
    # Claves robustas por tipo
    def _clave(reg: dict[str, object]):
        if campo == "nombre":
            return str(reg.get("nombre", "")).casefold()
        if campo == "poblacion":
            return int(str(reg.get("poblacion", "0")).replace("_","").replace(" ","") or "0")
        # campo == "superficie"
        return int(str(reg.get("superficie", "0")).replace("_","").replace(" ","") or "0")

    return sorted(list(datos), key=_clave, reverse=descendente)

#================# Función clave_orden =================#
#   Devuelve la clave de ordenamiento según el campo.
def parsear_rango_num(texto: str) -> tuple[int | None, int | None] | None:
    if not texto:
        return None
    s = texto.strip().replace(" ", "")
    # min-max
    if "-" in s:
        a, b = s.split("-", 1)
        ok_a, va = _entero_sin_sep(a)
        ok_b, vb = _entero_sin_sep(b)
        if not ok_a or not ok_b or va > vb:
            return None
        return (va, vb)
    # >=min
    if s.startswith(">="):
        ok, v = _entero_sin_sep(s[2:])
        return (v, None) if ok else None
    # <=max
    if s.startswith("<="):
        ok, v = _entero_sin_sep(s[2:])
        return (None, v) if ok else None
    # exacto
    ok, v = _entero_sin_sep(s)
    return (v, v) if ok else None
#=============================================================# 





#================# Función pais_mayor_menor_poblacion =======================#
#==Devuelve el país con mayor y menor población en una tupla (mayor, menor)==#
def pais_mayor_menor_poblacion(datos: list[dict[str, object]]) -> tuple[dict[str, object] | None, dict[str, object] | None]:
    if not datos: # Si no hay datos,
        return None, None # devuelve (None, None)
    mayor = max(datos, key=lambda r: int(r["poblacion"])) # Encuentra el país con mayor población
    menor = min(datos, key=lambda r: int(r["poblacion"])) # Encuentra el país con menor población
    return mayor, menor  # Devuelve una tupla con el país de mayor y menor población
#============================================================================#

#================# Función promedio_poblacion ======================#
#==Devuelve el promedio simple de población. None si no hay datos.==#
def promedio_poblacion(datos: list[dict[str, object]]) -> float | None:
    if not datos: # Si no hay datos,
        return None # devuelve None
    return sum(int(r["poblacion"]) for r in datos) / len(datos) # Calcula y devuelve el promedio de población
#===================================================================#

#================# Función promedio_superficie ===================#
#==Promedio simple de superficie (km²). None si no hay datos.==#
def promedio_superficie(datos: list[dict[str, object]]) -> float | None:
    if not datos: # Si no hay datos, devuelve None
        return None # Devuelve None si no hay datos
    return sum(int(r["superficie"]) for r in datos) / len(datos) # Calcula y devuelve el promedio de superficie
#=================================================================#

#================# Función conteo_por_continente =================#
#==Cantidad de países por continente (case-sensitive tal como vienen cargados).==#
def conteo_por_continente(datos: list[dict[str, object]]) -> dict[str, int]:
    conteo: dict[str, int] = {} # Diccionario para almacenar el conteo por continente
    for r in datos: # Itera sobre cada dict[str, object] en los datos
        cont = str(r["continente"]) # Obtiene el continente del dict[str, object]
        conteo[cont] = conteo.get(cont, 0) + 1 # Incrementa el conteo para el continente
    return conteo # Devuelve el diccionario con el conteo por continente
#=================================================================#

#================# Función mostrar_estadisticas_resumen =================#
#==Muestra todas las estadísticas pedidas por el TPI en un bloque compacto.==
def mostrar_estadisticas_resumen(datos: list[dict[str, object]]) -> None:
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






#=========================#
#  Gestión de países (CRUD principal)
#  - Búsqueda por nombre (parcial) y selección si hay múltiples
#=========================#
def _indices_coinciden_nombre(datos: list[dict[str, object]], consulta: str) -> list[int]:
    """
    Devuelve los índices de los registros cuyo nombre contiene la consulta (case-insensitive).
    """
    q = normalizar_texto(consulta)
    if q == "":
        return []
    idxs: list[int] = []
    for i, r in enumerate(datos):
        if q in normalizar_texto(str(r.get("nombre", ""))):
            idxs.append(i)
    return idxs

def actualizar_pais(datos: list[dict[str, object]]) -> None:
    if not datos:
        print("[INFO] No hay datos cargados. Use la opción 1 primero.")
        return

    print("\n--- Actualizar país ---")
    q = input("Nombre a buscar (parcial o exacto): ").strip()
    if q == "":
        print("[ERROR] La búsqueda no puede estar vacía.")
        return

    coincidencias = _indices_coinciden_nombre(datos, q)
    if len(coincidencias) == 0:
        print("[INFO] No se encontraron países para esa búsqueda.")
        return

    # Elegir país si hay múltiples
    if len(coincidencias) == 1:
        idx = coincidencias[0]
    else:
        print(f"[OK] Se encontraron {len(coincidencias)} coincidencia(s):")
        for orden, i in enumerate(coincidencias, start=1):
            r = datos[i]
            print(f"{orden}) {r['nombre']} | Pob: {r['poblacion']:,} | Sup: {r['superficie']:,} km² | Cont: {r['continente']}".replace(",", "."))
        sel = input(f"Elija número [1-{len(coincidencias)}]: ").strip()
        if not sel.isdigit():
            print("[ERROR] Debe elegir un número válido.")
            return
        n = int(sel)
        if n < 1 or n > len(coincidencias):
            print("[ERROR] Opción fuera de rango.")
            return
        idx = coincidencias[n-1]

    # Mostrar actual y pedir nuevos valores (Enter = mantener)
    actual = datos[idx]
    print("\nValores actuales:")
    mostrar_registro(actual)

    pob_txt = input("Nueva población (Enter = mantener actual): ").strip().replace("_", "").replace(" ", "")
    if pob_txt != "":
        if not es_entero(pob_txt):
            print("[ERROR] Población debe ser un entero válido.")
            return
        nueva_pob = int(pob_txt)
        if nueva_pob <= 0:
            print("[ERROR] Población debe ser un entero positivo.")
            return
    else:
        nueva_pob = int(actual["poblacion"])

    sup_txt = input("Nueva superficie en km² (Enter = mantener actual): ").strip().replace("_", "").replace(" ", "")
    if sup_txt != "":
        if not es_entero(sup_txt):
            print("[ERROR] Superficie debe ser un entero válido.")
            return
        nueva_sup = int(sup_txt)
        if nueva_sup <= 0:
            print("[ERROR] Superficie debe ser un entero positivo.")
            return
    else:
        nueva_sup = int(actual["superficie"])

    # Aplicar cambios
    actual["poblacion"] = nueva_pob
    actual["superficie"] = nueva_sup

    print("\n[OK] País actualizado:")
    mostrar_registro(actual)

#=========================#
# Agregar país 
#=========================#
def agregar_pais(datos: list[dict[str, object]]) -> None:
    print("\n--- Agregar país ---")

    # Nombre
    nombre = input("Nombre: ").strip()
    if nombre == "":
        print("[ERROR] No se permiten campos vacíos (nombre).")
        return

    # Población (permite 1_000_000 y espacios)
    poblacion_txt = input("Población (entero > 0): ").strip().replace("_", "").replace(" ", "")
    if not es_entero(poblacion_txt):
        print("[ERROR] Población debe ser un entero válido.")
        return
    poblacion = int(poblacion_txt)
    if poblacion <= 0:
        print("[ERROR] Población debe ser un entero positivo.")
        return

    # Superficie (permite 1_000_000 y espacios)
    superficie_txt = input("Superficie en km² (entero > 0): ").strip().replace("_", "").replace(" ", "")
    if not es_entero(superficie_txt):
        print("[ERROR] Superficie debe ser un entero válido.")
        return
    superficie = int(superficie_txt)
    if superficie <= 0:
        print("[ERROR] Superficie debe ser un entero positivo.")
        return

    # Continente (elegir de lista — respeta capitalización/acentos existentes)
    continente = elegir_continente(datos).strip()
    if continente == "":
        print("[ERROR] No se permiten campos vacíos (continente).")
        return

    # Duplicados por nombre (case-insensitive)
    nombre_norm = normalizar_texto(nombre)
    existe = False
    for r in datos:
        if normalizar_texto(str(r.get("nombre", ""))) == nombre_norm:
            existe = True
            break
    if existe:
        print("[INFO] Ya existe un país con ese nombre. No se agregó.")
        return

    # Alta
    datos.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })
    print(f"[OK] País agregado: {nombre} (Continente: {continente})")
#==========================================================#

#================# Funcion buscar_por_nombre=================#
def buscar_por_nombre(datos: list[dict[str, object]], consulta: str, modo: str = "parcial") -> list[dict[str, object]]:
    q = normalizar_texto(consulta)
    if not q:
        return []
    if modo == "exacta":
        return [r for r in datos if normalizar_texto(str(r.get("nombre",""))) == q]
    # parcial (default)
    return [r for r in datos if q in normalizar_texto(str(r.get("nombre","")))]

#============================================================#



#================# Punto de entrada principal =================#
if __name__ == "__main__": # Punto de entrada principal
    menu()  # Llama a la función del menú principal
#==============================================================#
