# pyteambook

**pyteambook** es una herramienta de línea de comandos (CLI) diseñada para automatizar la creación de **Team Reference Documents (Teambooks)** utilizados en competencias de programación competitiva como **ICPC**.

El objetivo es transformar una carpeta de algoritmos (`.cpp`, `.java`, `.py`) en un PDF limpio, compacto y bien indexado, listo para imprimir y usar en competencia.

## Instalación

### Requisitos Previos
- Python 3.9+
- Una distribución de LaTeX (TeXLive, MikTeX) instalada y en el PATH
- Pygments (se instala automáticamente con pyteambook)

### Instalar con pipx (Recomendado)

```bash
pipx install git+https://github.com/profetaRecursivo/pyteambook.git
```

### Instalar desde código fuente

```bash
git clone https://github.com/profetaRecursivo/pyteambook.git
cd pyteambook
source .venv/bin/activate
pipx install -e .
```
De momento es necesario estar en el entorno virtual para usar pyteambook como comando, en futuras versiones se agregara una instalacion limpia

## Uso

### Comando básico

```bash
pyteambook build ./codes -o teambook.tex
```

### Opciones completas

```bash
pyteambook build ./codes \
  -o teambook.tex \
  -t "Team ICPC" \
  -u "Universidad Nacional" \
  -c 2 \
  -p a4 \
  -i logo.png
```

**Opciones disponibles:**
- `-o, --output`: Archivo LaTeX de salida (default: `output.tex`)
- `-t, --team-name`: Nombre del equipo
- `-u, --university`: Nombre de la universidad
- `-c, --columns`: Número de columnas (1-3, default: 2)
  - 1 columna = orientación vertical
  - 2-3 columnas = orientación horizontal
- `-p, --paper`: Tamaño de papel (`a4`, `letter`, `legal`, default: `a4`)
- `-i, --image`: Imagen de portada (solo JPG/PNG)

### Compilar el PDF

Después de generar el archivo `.tex`, compílalo con:

```bash
pdflatex -shell-escape teambook.tex
# o
xelatex -shell-escape teambook.tex
```

**Nota:** El flag `-shell-escape` es necesario para que Minted funcione correctamente.

**Importante:** A veces puede ser necesario recompilar el .tex mas de una vez, ya que minted necesita archivos temporales que surgen despues de la primera compilacion.

## Estructura de Carpetas

Organiza tus códigos en la siguiente estructura:

```
codes/
├── Grafos/
│   ├── DFS/
│   │   ├── dfs_basico.cpp
│   │   └── dfs_colores.cpp
│   └── dijkstra.cpp
├── Matematica/
│   ├── numeros_primos.py
│   └── gcd.java
└── Strings/
    └── kmp.cpp
```

- **Nivel 1**: Sección (ej: Grafos, Matemática)
- **Nivel 2**: Subsección (ej: DFS, BFS)
- **Nivel 3+**: Archivos de código

## Características

- Soporte para C++, Python, Java y Bash
- Resaltado de sintaxis con Minted (estilo Emacs)
- Tabla de contenidos con todos los archivos indexados
- Portada personalizable con logo
- Múltiples formatos de papel (A4, Letter, Legal)
- Configuración flexible de columnas (1-3)
- Escape automático de caracteres especiales de LaTeX

## Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

Este es un proyecto personal con fines educativos para profundizar en arquitectura de software y uso general de pythoncito.