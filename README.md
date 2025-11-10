Gestión de Países — Consola (Python)

Aplicación de consola para gestionar un listado de países a partir de un archivo CSV: cargar, buscar, filtrar, ordenar, calcular estadísticas, agregar y actualizar registros, y guardar cambios.

Tabla de contenido

Requisitos

Instalación

Ejecución

Estructura del CSV

Menú y funcionalidades

Validaciones y mensajes

Diagrama general (Mermaid)

Casos de uso rápidos

Solución de problemas

Estructura del proyecto

Roadmap

Licencia

Requisitos

Python 3.10+ (recomendado 3.12)

No requiere dependencias externas (usa librerías estándar).

Opcional: usar un entorno virtual para aislar dependencias.

python -V
python -m venv .venv
# Activar
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

Instalación

Cloná este repositorio y, si querés, activá tu entorno virtual:

git clone <TU_REPO_URL>
cd <TU_REPO>
# (opcional) activar venv


No hay paquetes extra que instalar.

Ejecución
# Windows
python main.py

# Linux / macOS
python3 main.py


Al iniciar verás el menú principal con las opciones 0..9.

Estructura del CSV

El archivo CSV debe incluir encabezados exactamente con estos nombres:

nombre,poblacion,superficie,continente


nombre: texto no vacío (único para agregar).

poblacion: entero > 0.

superficie: entero > 0.

continente: texto no vacío (ej.: America, Europa, Asia, Africa, Oceania, Antartida).

Ejemplo de data/paises.csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,America
Chile,19116209,756102,America
Espana,47351567,505990,Europa
Japon,125360000,377975,Asia
Australia,25687041,7692024,Oceania


El programa valida encabezados y filas. Las filas inválidas se omiten durante la carga y se informa un resumen.

Menú y funcionalidades

0) Salir
Termina la aplicación.

1) Cargar CSV

Pide ruta (Enter usa data/paises.csv por defecto).

Valida encabezados y recorre filas.

Omite filas inválidas e informa un resumen.

2) Buscar país por nombre

Modo exacta o parcial (case-insensitive).

Muestra coincidencias.

3) Ver total

Muestra len(datos) (cantidad de países cargados).

4) Filtros
Submenú:

1: por continente

2: por rango de población (min-max)

3: por rango de superficie (min-max)

0: volver
Valida rangos, lista resultados o informa “sin resultados”.

5) Ordenamientos

Elegir campo (nombre, poblacion, superficie) y sentido (A asc / D desc).

Muestra primeros N (según el programa).

6) Estadísticas
Métricas típicas (ajustables):

Máximo / Mínimo de población

Promedio de población

Densidad promedio (poblacion/superficie)
Muestra resultados y vuelve al menú.

7) Agregar país

Pide nombre, población (>0), superficie (>0), continente.

Valida duplicado por nombre (case-insensitive).

Si hay una ruta asociada (CSV cargado), permite guardar.

8) Guardar cambios

Valida que exista una ruta válida y que haya datos.

Revalida registros antes de escribir.

Escribe encabezados y filas.

9) Actualizar país

Búsqueda parcial del nombre.

Si hay varias coincidencias, el usuario elige índice.

Pide nueva población/superficie (Enter mantiene).

Valida y aplica cambios.

Validaciones y mensajes

Encabezados inválidos (en Cargar CSV): error y volver al menú.

Fila inválida (Cargar CSV): se omite y el proceso continúa.

Sin datos (p.ej., Buscar/Filtrar/Ordenar/Estadísticas): se informa y vuelve al menú.

Rangos inválidos (parsear_rango_num): error y permanece en el submenú de filtros.

Guardar con datos inválidos: cancela el guardado y avisa.

Actualizar país: selección de índice inválida o valores no válidos → error y volver al menú (no reintenta).

El programa usa mensajes tipo [OK], [INFO], [AVISO], [ERROR] para comunicar estados.

Diagrama general (Mermaid)

Podés visualizarlo en https://mermaid.live
 o integrarlo en tu documentación.

Menú principal
flowchart TD
    A0([Inicio]) --> A1[Inicializar variables]
    A1 --> A2[Vuelve al menu]
    A2 --> A3[Leer opcion del usuario]
    A3 --> A4{Opcion elegida}

    A4 -->|0| F0([Fin])

    A4 -->|1| F1[Llamar funcion cargar_csv] --> A2
    A4 -->|2| F2[Llamar funcion buscar_pais] --> A2
    A4 -->|3| F3[Llamar funcion ver_total] --> A2
    A4 -->|4| F4[Llamar funcion submenu_filtros] --> A2
    A4 -->|5| F5[Llamar funcion submenu_ordenamientos] --> A2
    A4 -->|6| F6[Llamar funcion submenu_estadisticas] --> A2
    A4 -->|7| F7[Llamar funcion agregar_pais] --> A2
    A4 -->|8| F8[Llamar funcion guardar_csv] --> A2
    A4 -->|9| F9[Llamar funcion actualizar_pais] --> A2
    A4 -->|Otro| ERR[[Opcion invalida]] --> A2


En la carpeta docs/ podés incluir diagramas adicionales por función (cargar_csv, filtros, etc.).

Casos de uso rápidos

Cargar y listar total

Menú → 1 → Enter (usa CSV por defecto) → ver resumen

Menú → 3 → ver total

Buscar por nombre (parcial)

Menú → 2 → arg (por “argentina”) → parcial

Filtrar por continente

Menú → 4 → 1 → America

Ordenar por población descendente

Menú → 5 → campo poblacion → sentido D

Agregar país y guardar

Menú → 7 → completar datos

Menú → 8 → guarda en la misma ruta cargada

Solución de problemas

“No se encontró el archivo” al cargar
Verificá la ruta o usá Enter para el CSV por defecto (data/paises.csv).

“Encabezados inválidos”
Confirmá que el CSV tenga exactamente:
nombre,poblacion,superficie,continente

“Rango inválido” en filtros
Formato esperado: min-max (ej.: 1000000-5000000).
No uses espacios ni letras.

No se guarda el CSV

Asegurate de haber cargado primero un archivo (para tener ruta_actual).

Si detecta registros inválidos, cancela el guardado: corregí los datos.

Estructura del proyecto
.
├─ main.py                # Programa principal (menu y logica)
├─ data/
│  └─ paises.csv          # CSV de ejemplo (opcional)
├─ docs/
│  ├─ diagramas.md        # Mermaid de los flujos (opcional)
│  └─ diagramas/*.png     # Exportaciones (opcional)
└─ README.md

Roadmap

Exportar a JSON además de CSV.

Soporte de idioma configurable.

Pruebas unitarias de helpers (parseo de rango, filtros, ordenamiento).

Métricas adicionales (p. ej., top-N por densidad).

Licencia

Este proyecto se distribuye bajo la licencia MIT (o la que prefieras). Agregá el archivo LICENSE si corresponde.

Autor: Matías Luis Yacob