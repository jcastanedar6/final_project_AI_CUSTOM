# Sistema CAG con Memoria Persistente y Portable

**Módulo 3 — Examen Final · Inteligencia Artificial Aplicada**  
**Estudiante:** Juan Pablo Castañeda Rodríguez · jcastanedar6@miumg.edu.gt  
**Universidad Mariano Gálvez de Guatemala · 2026**

Sistema **Context-Augmented Generation (CAG)** implementado sobre una arquitectura RAG existente. Incorpora memoria persistente de usuario y de sistema, portabilidad total entre equipos y evidencia verificable del uso responsable de IA.

> **Clonar → Ejecutar → El CAG recuerda todo.**

---

## Arquitectura

```
Usuario
  ↓
Frontend (puerto 8080)
  ↓
Context Manager — CAG  (backend/cag.py)
  ├── Memoria del sistema   → SQLite
  ├── Memoria del usuario   → SQLite
  └── Retriever RAG         → Chroma DB (persistida en disco)
        ↓
    Prompt Builder          (backend/assistant.py)
        ↓
       LLM
```

### Tipos de memoria

| Capa | Tecnología | Propósito |
|---|---|---|
| Documental (RAG) | Chroma DB | Búsqueda vectorial semántica sobre 5 PDFs académicos |
| Conversacional | SQLite | Resúmenes de objetivos, decisiones y preferencias del usuario |
| Sistema | SQLite | Restricciones técnicas y decisiones arquitectónicas cerradas |

**Principio fundamental:** el LLM no recuerda — el sistema le construye el contexto en cada llamada.

---

## Inicio rápido

### 1. Clonar

```bash
git clone https://github.com/jcastanedar6/final_project_AI_CUSTOM.git
cd final_project_AI_CUSTOM
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Levantar el backend

```bash
PYTHONPATH=. python3 -m backend.server
```

Backend disponible en `http://127.0.0.1:8000`.

### 4. Levantar el frontend

```bash
python3 -m http.server 8080 --directory frontend
```

Abrir `http://127.0.0.1:8080` en el navegador.

---

## Estructura del proyecto

| Ruta | Contenido |
|---|---|
| `backend/server.py` | API FastAPI — endpoints del asistente y contexto CAG |
| `backend/cag.py` | Context Manager — orquesta las 3 capas de memoria |
| `backend/context_store.py` | Persistencia SQLite de memoria conversacional y de sistema |
| `backend/knowledge.py` | Pipeline RAG — carga, chunking semántico y vectorización |
| `backend/assistant.py` | Prompt Builder — ensambla contexto y llama al LLM |
| `data/knowledge_base.json` | Base de conocimiento inicial |
| `docs/` | 5 PDFs académicos generados como fuente de conocimiento |
| `docs/evidencias/` | Manual técnico (.docx) y registro de prompts (PROMPTS.md) |
| `tests/features/` | Escenarios BDD (Behave) |
| `tests/unit/` | Tests unitarios (TDD) |
| `tests/base/` | Pruebas base del proyecto original |
| `tests/validation/` | Pruebas de validación final |
| `scripts/` | Scripts de inicialización y generación de PDFs |

---

## Ejecutar pruebas

### Pruebas base

```bash
./scripts/run_base_tests.sh
```

### BDD (Behave)

```bash
behave tests/features/
```

### TDD (unittest / pytest)

```bash
python3 -m pytest tests/unit/
```

### Validación final

```bash
./test.sh
```

---

## PDFs de conocimiento

El sistema usa 5 PDFs como base documental del RAG. Se regeneran con:

```bash
python3 docs/gen_pdfs.py
```

| Documento | Tema |
|---|---|
| `SDD_Software_Design_Document.pdf` | Diseño de software |
| `BDD_Behavior_Driven_Development.pdf` | Desarrollo guiado por comportamiento |
| `TDD_Test_Driven_Development.pdf` | Desarrollo guiado por pruebas |
| `RAG_Retrieval_Augmented_Generation.pdf` | Generación aumentada por recuperación |
| `CAG_Context_Augmented_Generation.pdf` | Generación aumentada por contexto |

---

## Evidencias del proceso

| Documento | Ubicación | Contenido |
|---|---|---|
| `PROMPTS.md` | `docs/evidencias/` | Registro cronológico de 9 interacciones con IA, decisiones y justificaciones técnicas |
| `Manual_Tecnico_CAG.docx` | `docs/evidencias/` | Manual técnico completo con capturas, arquitectura y registro de uso responsable de IA |

---

## Uso responsable de IA

La IA fue utilizada como asistente técnico — no como generador autónomo.

| Herramienta | Uso |
|---|---|
| ChatGPT (GPT-4) | Diseño arquitectónico CAG, estrategia de memoria y portabilidad |
| Grok | Pipeline de ingesta semántica de PDFs para RAG |
| Claude Code (claude-sonnet-4-6) | Implementación técnica, git operations, generación de evidencias |

**Decisiones de arquitectura adoptadas sin verificación del estudiante: 0**  
Ver `docs/evidencias/PROMPTS.md` para el registro completo.
