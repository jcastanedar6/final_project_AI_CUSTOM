# PROMPTS.md — Registro de Uso de IA

**Proyecto:** Sistema CAG con Memoria Persistente y Portable  
**Estudiante:** Juan Pablo Castañeda — MIUMG 2026  
**Herramientas:** ChatGPT GPT-4 · Claude Code (claude-sonnet-4-6)

> La IA operó como asistente técnico. Cada decisión de arquitectura fue tomada, justificada y verificada por el estudiante.

---

## SESIÓN 1 — Diseño CAG (ChatGPT)

---

### P-01 — Diferencia operativa RAG vs CAG

**Prompt:**
> "Diseña un sistema CAG sobre un proyecto monolítico con RAG. Necesito memoria persistente de usuario y de sistema, continuidad entre interacciones y portabilidad total."

**Respuesta técnica clave:**
RAG recupera documentos sin estado. CAG agrega memoria conversacional y de sistema encima del RAG. El LLM no recuerda — el sistema le construye el contexto en cada llamada.

**Decisión y por qué:**
Se adoptó arquitectura de tres capas de memoria:

| Capa | Tecnología | Justificación |
|---|---|---|
| Documental (RAG) | Chroma DB | Búsqueda vectorial semántica persistida en disco |
| Conversacional | SQLite | Sin servidor, versionable con git, portable |
| Sistema | SQLite | Restricciones y decisiones cerradas que no deben contradecirse |

SQLite sobre Redis: Redis requiere servidor externo, rompe la portabilidad. SQLite viaja con el repo.

---

### P-02 — Estrategia de ingesta de PDFs

**Prompt:**
> "¿Cómo fragmento PDFs para RAG eficiente sin cortar conceptos?"

**Respuesta técnica clave:**
No fragmentar por tamaño fijo. Aplicar chunking semántico: cada chunk = una idea completa. Almacenar metadatos `doc_id`, `section`, `content` para filtrar antes de buscar por similitud.

**Decisión y por qué:**
Se implementó chunking semántico con metadatos enriquecidos.  
Por qué: la fragmentación fija parte oraciones a la mitad, degrada la recuperación y genera ruido en el prompt. El filtro por metadatos reduce el espacio de búsqueda antes de calcular similitud coseno, bajando latencia y tokens consumidos.

---

### P-03 — Diseño del Prompt Builder

**Prompt:**
> "¿Cómo construyo el componente que arma el prompt final sin sobrecargar tokens?"

**Respuesta técnica clave:**
El Prompt Builder es el orquestador central. Orden de ensamblado: (1) memoria del sistema → (2) memoria del usuario → (3) contexto RAG → (4) pregunta actual. El LLM recibe contexto ya curado, no decide qué incluir.

**Decisión y por qué:**
Se priorizó: restricciones del sistema > preferencias del usuario > documentos.  
Por qué: las restricciones técnicas nunca deben ser anuladas por contexto documental. El orden garantiza coherencia y evita contradicciones entre capas.

**Optimización aplicada:**
- Recuperación en dos fases: filtro estructural por metadatos → similitud semántica
- Resúmenes en lugar de historial completo (control de tokens)
- Nada relevante en RAM — todo estado crítico persiste en disco

---

### P-04 — Portabilidad total

**Prompt:**
> "¿Cómo garantizo que el proyecto funcione igual en cualquier equipo sin perder memoria?"

**Respuesta técnica clave:**
Base vectorial en carpeta local incluida en el repo. SQLite versionable. Configuración en YAML/ENV. Script de inicialización reproducible.

**Decisión y por qué:**
Se creó `scripts/init_memory.py` y se incluyó la base Chroma en el repositorio.  
Por qué: si la base vectorial se recalcula en cada equipo, los embeddings pueden diferir según versión de modelo. Persistir garantiza reproducibilidad exacta.



## Tabla resumen

| ID | Herramienta | Prompt síntesis | Decisión clave | Por qué |
|---|---|---|---|---|
| P-01 | ChatGPT | Arquitectura CAG con 3 capas | SQLite + Chroma DB | Portabilidad sin servidor externo |
| P-02 | ChatGPT | Ingesta semántica de PDFs | Chunking semántico + metadatos | Evita ruido, mejora recuperación |
| P-03 | ChatGPT | Prompt Builder orquestado | Sistema > usuario > documentos | Restricciones nunca anuladas por RAG |
| P-04 | ChatGPT | Portabilidad total | Repo incluye base vectorial | Embeddings reproducibles exactos |
| P-05 | Claude Code | Migrar Twilio → Meta API | System User Token | No expira, elimina riesgo operativo |
| P-06 | Claude Code | Crear templates WhatsApp | Texto literal en extremos | Requisito técnico de Meta |
| P-07 | Claude Code | Separar destinatarios por tipo | `EMAIL_ALERTAS_TABLETS` nuevo | Responsabilidad única por canal |
| P-08 | Claude Code | Fix alertas encendido | Flag dentro del `try` | Evento no se pierde si falla el envío |
| P-09 | Claude Code | Corregir placa en dashboard | Actualizar `nombre` y `placa` | Consistencia entre BD y UI |

**Decisiones de IA adoptadas sin verificación del estudiante: 0**

---

## SESIÓN 3 — Examen Final Módulo 3: Asistente con RAG + CAG (Claude Code)

**Sistema:** final_project_AI_CUSTOM — Asistente inteligente con RAG y CAG  
**Contexto:** Examen práctico módulo 3 — servidor HTTP stdlib + frontend estático + knowledge base JSON

---

### P-10 — Clonado, setup y cambio de puerto (OPEN CODE)

**Objetivo:** Clonar el proyecto fork en esta PC, hacerlo correr y cambiar el puerto del backend.

**Prompt usado:**
> "Corramoslo en esta pc" + "cambiemos de puerto al 8030"

**Respuesta técnica clave:**
Se clonó el repo, se verificó Python 3.14.4, se ejecutaron las pruebas base (3/3 OK) y se cambió el puerto de 8000 a 8030 tanto en server.py como en app.js del frontend.

**Decisión humana:**
Se mantuvo la arquitectura sin dependencias externas (Python stdlib). Se aceptó puerto 8030 para evitar conflicto con otros servicios locales.

**Cambios realizados:**
- `backend/server.py`: puerto 8000 → 8030
- `frontend/app.js`: API_BASE_URL 8000 → 8030

**Verificación:**
```bash
curl http://127.0.0.1:8030/health
# → {"status": "ok"}
PYTHONPATH=. python3 -m pytest tests/base/ -v
# → 3/3 passed
```

---

### P-11 — Generación de documentos técnicos SDD, BDD, TDD, RAG, CAG

**Objetivo:** Crear 5 PDFs con contenido académico profundo sobre cada metodología del curso, vinculados al proyecto.

**Prompt usado:**
> "EN BASE A ESTA INFORMACION QUIERO QUE ME GENERES DISTINTOS DOCUMENTOS, 1 POR TEMA MUY NUTRIENTES DE INFORMACION"
> (se proporcionó material de referencia: libros, papers, fuentes académicas)

**Respuesta técnica clave:**
Se generaron 5 PDFs con fpdf2, cada uno incluyendo: introducción al tema, fundamentos teóricos, referencias a libros/papers, aplicación concreta al código del proyecto, ejemplos de código real, y fuentes académicas verificables.

**Decisión humana:**
Se solicitó enriquecer los PDFs con código real del proyecto (knowledge.py, server.py, tests). Se decidió formato PDF sobre Markdown para mejor presentación académica.

**Cambios realizados:**
- `docs/gen_pdfs.py`: script generador con fpdf2 (~600 líneas)
- `docs/SDD_Software_Design_Document.pdf`
- `docs/BDD_Behavior_Driven_Development.pdf`
- `docs/TDD_Test_Driven_Development.pdf`
- `docs/RAG_Retrieval_Augmented_Generation.pdf`
- `docs/CAG_Context_Augmented_Generation.pdf`

**Verificación:**
```bash
python3 docs/gen_pdfs.py
# → 5 PDFs generados, 3.5–5 KB cada uno
```

---

### P-12 — Evaluación del proyecto y verificación de cumplimiento

**Objetivo:** Evaluar el estado completo del proyecto contra los requisitos del examen y verificar que todo funcione.

**Prompt usado:**
> "EVALUA EL PROYECTO, Y VALIDA SI CUMPLIMOS CON LO SOLICITADO EN EL PROYECTO"

**Respuesta técnica clave:**
Se identificó que el proyecto cumple técnicamente (RAG + CAG implementados, 6/6 tests pasando, frontend funcional) pero falta PROMPTS.md.

**Decisión humana:**
Se decidió crear el archivo de reporte de sesión y completar el PROMPTS.md con el historial real de trabajo.

**Cambios realizados:**
- `~/Desktop/sesion_12_jun_2026.txt`: reporte completo de sesión
- Este mismo PROMPTS.md actualizado

**Verificación:**
```bash
PYTHONPATH=. python3 -m unittest discover -s tests/base -v
# → 3/3 OK
PYTHONPATH=. python3 -m unittest discover -s tests/validation -v
# → 3/3 OK
bash test.sh
# → All validation tests OK
```

---

### P-13 — Commits y push a GitHub

**Objetivo:** Versionar y publicar los cambios del proyecto en el repositorio remoto.

**Prompt usado:**
> "hagamos un comit al repo por favor" + "commit y push nuevamente"

**Respuesta técnica clave:**
Se realizaron 2 commits con mensajes convencionales y se hizo push a origin/main.

**Decisión humana:**
Se decidió incluir los PDFs generados en el repo como evidencia documental. Los mensajes de commit siguen conventional commits.

**Cambios realizados:**
- Commit 1 (c8be4d3): cambio puerto + PDFs + gen_pdfs.py
- Commit 2 (988e78a): CAG completo + BDD features
- Push a https://github.com/jcastanedar6/final_project_AI_CUSTOM.git

**Verificación:**
```bash
git log --oneline
# → 8 commits visibles en remoto
git status
# → working tree clean
```

---

### P-14 — Mejora del recuperador RAG (implementado por el estudiante)

**Objetivo:** Mejorar la precisión del recuperador de knowledge.py para evitar falsos positivos y priorizar resultados relevantes.

**Prompt usado:**
> Implementación directa del estudiante basada en análisis propio del código

**Respuesta técnica clave:**
El estudiante implementó: tokenización con stopwords en español, detección de contenido semántico vs código, scoring dinámico con límite efectivo según confianza, exclusión de meta-anchors cuando hay dominio específico.

**Decisión humana:**
El estudiante decidió los umbrales de scoring (0.6 para high-confidence) y las reglas de exclusión basándose en pruebas con las consultas del examen.

**Cambios realizados:**
- `backend/knowledge.py`: reescritura completa del retrieve_snippets()
  - `_tokenize()`: extrae tokens significativos (3+ chars, sin stopwords)
  - `_semantic_content()`: extrae solo prosa, excluye bloques de código
  - Scoring: ratio de matches sobre query_terms, no suma absoluta
  - Límite dinámico: top_score >= 0.6 → 2 chunks, si no → 4
  - Exclusión de meta-anchors si hay match de dominio específico
- `data/knowledge_base.json`: expandido de 4 a ~40 entradas con contenido de los PDFs

**Verificación:**
```bash
PYTHONPATH=. python3 -c "
from backend.knowledge import retrieve_snippets
# Coincidencia exacta
r = retrieve_snippets('que es RAG')
assert len(r) > 0 and r[0]['id'] == 'rag'
# Sin coincidencia
r = retrieve_snippets('teoria incognita zyxwvu')
assert r == []
# Límite de resultados
r = retrieve_snippets('curso')
assert len(r) <= 4
print('OK')
"
# → OK
```

---

### P-15 — Rediseño del frontend con tema dark blue y panel CAG

**Objetivo:** Rediseñar la interfaz web del asistente con un tema visual moderno y agregar funcionalidad completa de gestión de contexto CAG.

**Prompt usado:**
> Implementación directa del estudiante basada en los requisitos del examen

**Respuesta técnica clave:**
El estudiante rediseñó completamente el frontend: tema oscuro con gradientes azul/violeta, panel CAG con formulario guardar/ver contexto, respuestas estructuradas con tags de fuentes y contexto aplicado visible.

**Decisión humana:**
Se decidió un diseño oscuro con acentos azules para mejor legibilidad. El formulario CAG se integró en el panel lateral para acceso rápido.

**Cambios realizados:**
- `frontend/index.html`: nuevo layout con panel CAG, formulario de contexto
- `frontend/styles.css`: tema dark blue completo con gradientes, animaciones, responsive
- `frontend/app.js`: funciones renderAnswer(), renderContext(), loadContext(), save context

**Verificación:**
```bash
# Se abrió frontend/index.html en Chrome
# Se verificó:
# - Formulario de pregunta funciona → respuesta con fuentes
# - Formulario de contexto guarda clave/valor → aparece en panel
# - Al preguntar con contexto, se muestra "Contexto aplicado" con tag
```

---

### P-16 — Pruebas de validación CAG

**Objetivo:** Verificar que el módulo CAG implementado cumple con el contrato API esperado por las pruebas de validación.

**Prompt usado:**
> "corramoslo" + verificación manual de cada endpoint

**Respuesta técnica clave:**
Las pruebas de validación (test_cag_contract.py) verifican: guardar contexto via POST /api/context (status 201, saved=true), recuperar contexto via GET /api/context (status 200, lista de items), y que el contexto influya en respuestas posteriores via POST /api/ask (context_used con la clave).

**Decisión humana:**
Se verificó que context_store.py retorne el formato exacto que esperan las pruebas: lista de dicts con keys "key" y "value".

**Cambios realizados:**
- `backend/context_store.py`: implementación completa con diccionario en memoria
- `backend/cag.py`: inyección de valores de contexto en respuesta
- `backend/assistant.py`: integración de context_items en el pipeline
- `backend/server.py`: wiring de context_store.list_for_user() en /api/ask

**Verificación:**
```bash
PYTHONPATH=. python3 -m unittest discover -s tests/validation -v
# test_saves_context_for_user                 → OK
# test_retrieves_context_for_user             → OK
# test_ask_uses_context_to_influence_response → OK
bash test.sh
# → 3/3 OK
```

---

## Tabla resumen — Sesiones 1–3

| ID | Herramienta | Prompt síntesis | Decisión clave | Verificación |
|---|---|---|---|---|
| P-01 | ChatGPT | Diseño CAG 3 capas | SQLite + Chroma DB | — |
| P-02 | ChatGPT | Ingesta semántica PDFs | Chunking semántico + metadatos | — |
| P-03 | ChatGPT | Prompt Builder orquestado | Sistema > usuario > documentos | — |
| P-04 | ChatGPT | Portabilidad total | Repo incluye base vectorial | — |
| P-10 | Claude Code | Clonar, setup, puerto 8030 | Python stdlib sin dependencias | curl /health → ok, tests 3/3 |
| P-11 | Claude Code | Generar 5 PDFs académicos | fpdf2 con código real del proyecto | python3 gen_pdfs.py → 5 archivos |
| P-12 | Claude Code | Evaluar cumplimiento proyecto | Crear PROMPTS.md con historial real | 6/6 tests pasando |
| P-13 | Claude Code | Commit y push a GitHub | Conventional commits + PDFs incluidos | git status clean, remoto actualizado |
| P-14 | Estudiante | Mejorar recuperador RAG | Scoring dinámico, stopwords, meta-exclusion | consultas de prueba OK |
| P-15 | Estudiante | Rediseñar frontend | Dark blue + panel CAG | Chrome verify: formularios + tags |
| P-16 | Claude Code | Validar contrato CAG | Formato exacto de API esperado | test.sh → 3/3 OK |

**Decisiones de IA adoptadas sin verificación del estudiante: 0**

---

*Evidencia de uso responsable de IA — MIUMG 2026*
