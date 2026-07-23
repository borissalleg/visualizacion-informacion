# Visualización de Información

Sitio de documentación del curso **Visualización de Información**, perteneciente a la
**Especialización en Analítica y Big Data** de IUDigital de Antioquia. Construido con
[MkDocs](https://www.mkdocs.org/) y el tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

El material está organizado en tres unidades temáticas:

1. **Unidad 1 — Conceptos básicos sobre visualización**: fundamentos teóricos,
   percepción visual, tipos de visualización y visualización dinámica de datos.
2. **Unidad 2 — Herramientas de visualización**: cuadros de mando, publicación de
   visualizaciones, librerías de visualización y mapas.
3. **Unidad 3 — Geovisualización**: mapas coropléticos, mapas de densidad e
   interpolación espacial.

Cada subtema incluye objetivos de aprendizaje, explicación conceptual, ejemplos de
código ejecutables (Python), buenas prácticas, ejercicios propuestos y referencias.

## Estructura de carpetas

```text
visualizacion-informacion/
├── mkdocs.yml                  # Configuración del sitio (tema, nav, extensiones)
├── requirements.txt            # Dependencias de Python (sitio + ejemplos)
├── README.md
├── .gitignore
├── docs/                       # Contenido del sitio (Markdown)
│   ├── index.md
│   ├── assets/
│   │   ├── images/             # Imágenes usadas en el material
│   │   └── datasets/           # Datasets de ejemplo (CSV/GeoJSON)
│   ├── unidad-1-conceptos-basicos/
│   ├── unidad-2-herramientas/
│   └── unidad-3-geovisualizacion/
└── examples/                   # Scripts .py ejecutables de forma independiente
    ├── unidad-1/
    ├── unidad-2/
    └── unidad-3/
```

## Instalación de dependencias

Se recomienda usar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Levantar el sitio en modo local (con recarga en caliente)

```bash
mkdocs serve
```

El sitio quedará disponible en `http://127.0.0.1:8000/`. Cualquier cambio en los
archivos de `docs/` se reflejará automáticamente en el navegador.

## Compilar el sitio estático

```bash
mkdocs build
```

Esto genera la carpeta `site/` con los archivos HTML/CSS/JS listos para desplegar en
cualquier servidor estático (no se versiona, ver `.gitignore`).

## Ejecutar los ejemplos de código

Cada ejemplo embebido en los `.md` tiene su script equivalente en `examples/`,
organizado por unidad. Por ejemplo:

```bash
python examples/unidad-1/ejemplo_percepcion_visual.py
```

Algunos ejemplos (Dash, Streamlit) levantan un servidor local; revisa el
encabezado de cada script para instrucciones específicas de ejecución, por ejemplo:

```bash
streamlit run examples/unidad-1/dashboard_tiempo_real.py
```

## Publicar el sitio con GitHub Pages

Una vez configurado el repositorio remoto (ver instrucciones más abajo), el sitio se
puede publicar automáticamente con:

```bash
mkdocs gh-deploy
```

Este comando compila el sitio y lo publica en la rama `gh-pages` del repositorio,
dejándolo disponible en `https://<usuario-o-organizacion>.github.io/visualizacion-informacion/`.

## Licencia y autoría

Material desarrollado para fines académicos en el marco de la Especialización en
Analítica y Big Data de IUDigital de Antioquia.
