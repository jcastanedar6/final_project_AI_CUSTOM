from fpdf import FPDF
import os

OUTPUT_DIR = "/Users/jcastaneda/final_project_AI_CUSTOM/docs"


class DocPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 6, self.title_text, align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, t):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, t, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def section(self, t):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 76, 153)
        self.cell(0, 8, t, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def sub(self, t):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(51, 51, 51)
        self.cell(0, 7, t, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def body(self, t):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, t)
        self.ln(2)

    def bullet(self, t):
        self.set_font("Helvetica", "", 10)
        self.cell(5, 5, "-")
        self.multi_cell(0, 5, t)
        self.ln(1)

    def code_block(self, code, lang=""):
        self.set_font("Courier", "", 8)
        self.set_fill_color(240, 240, 240)
        self.set_draw_color(200, 200, 200)
        lines = code.split("\n")
        for line in lines:
            self.cell(0, 4.5, "  " + line, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(3)
        self.set_font("Helvetica", "", 10)

    def ref(self, t):
        self.set_font("Courier", "", 9)
        self.set_text_color(0, 102, 51)
        self.cell(0, 5, t, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def note(self, t):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(102, 102, 102)
        self.multi_cell(0, 4.5, t)
        self.ln(2)
        self.set_text_color(0, 0, 0)


# ──────────────────────────────────────────
# 1. SDD
# ──────────────────────────────────────────
def make_sdd():
    p = DocPDF()
    p.alias_nb_pages()
    p.title_text = "SDD - Software Design Document"
    p.set_title(p.title_text)
    p.add_page()

    p.chapter_title("1. Introduccion")
    p.body(
        "El Software Design Document (SDD) documenta la arquitectura, componentes, interfaces "
        "y datos del sistema antes de implementar. Su proposito es garantizar vision compartida, "
        "reducir ambiguedad y habilitar trazabilidad entre requisitos y solucion tecnica."
    )
    p.body(
        "Referencias fundacionales: 'Software Architecture in Practice' (Bass, Clements, Kazman) "
        "y 'Documenting Software Architectures' (Clements et al.). Estas obras establecen el "
        "modelo de vistas multiples (modulos, componente-conector, asignacion) que permite a "
        "cada stakeholder obtener la informacion relevante sin saturarse."
    )

    p.section("1.1 Vistas Arquitectonicas")
    p.bullet("Vista de Modulos: descomposicion en paquetes y modulos con responsabilidades claras.")
    p.bullet("Vista de Componentes y Conectores: interacciones en tiempo de ejecucion (HTTP, llamadas a funciones).")
    p.bullet("Vista de Asignacion: despliegue, mapeo a infraestructura, restricciones fisicas.")

    p.section("1.2 Arquitectura del Proyecto")
    p.body("El asistente inteligente sigue una arquitectura de capas simple:")
    p.code_block(
        "final_project_AI_CUSTOM/\n"
        "  backend/               # Capa de servidor\n"
        "    server.py            # HTTP server (API REST)\n"
        "    assistant.py         # Orquestador pregunta->respuesta\n"
        "    knowledge.py         # Recuperacion RAG (scoring por terminos)\n"
        "    context_store.py     # Almacen de contexto CAG (pendiente)\n"
        "    cag.py               # Integracion contexto en respuesta (pendiente)\n"
        "  frontend/              # Interfaz web estatica\n"
        "    index.html\n"
        "    app.js               # Cliente HTTP contra backend\n"
        "    styles.css\n"
        "  data/\n"
        "    knowledge_base.json  # Base de conocimiento (4 documentos)\n"
        "  tests/\n"
        "    base/                # Pruebas base (deben pasar siempre)\n"
        "    validation/          # Pruebas de validacion (CAG contract)"
    )

    p.section("1.3 Decisiones Arquitectonicas Clave")
    p.sub("ADR-01: Sin dependencias externas")
    p.body(
        "El servidor usa la biblioteca estandar de Python (http.server, json, urllib) para "
        "eliminar la necesidad de pip install o entornos virtuales. Decision driven by "
        "simplicidad y portabilidad."
    )
    p.sub("ADR-02: API REST sobre HTTP")
    p.body(
        "Endpoints: GET /health, POST /api/ask, GET /api/context, POST /api/context. "
        "Formato JSON con CORS habilitado para el frontend."
    )
    p.sub("ADR-03: Separacion RAG / CAG")
    p.body(
        "knowledge.py maneja recuperacion de conocimiento general (RAG). context_store.py + "
        "cag.py manejan contexto persistente del usuario (CAG). Separacion limpia de "
        "responsabilidades."
    )

    p.add_page()
    p.chapter_title("2. Atributos de Calidad")
    p.bullet("Mantenibilidad: modulos con una unica responsabilidad (server, assistant, knowledge, context_store).")
    p.bullet("Testeabilidad: servidor con puerto dinamico (port=0) para tests aislados.")
    p.bullet("Extensibilidad: nueva logica CAG se agrega sin tocar server.py mas que conectar los handlers.")
    p.bullet("Portabilidad: Python stdlib solo -> corre en cualquier SO con Python 3.8+.")

    p.chapter_title("3. Flujo de Datos: /api/ask")
    p.code_block(
        "Frontend  --POST /api/ask {user_id, question}-->  server.py\n"
        "  -> ExamRequestHandler.do_POST()\n"
        "    -> assistant.answer_question(user_id, question)\n"
        "      -> knowledge.retrieve_snippets(question)     # RAG\n"
        "        -> load_knowledge_base()                    # Lee JSON\n"
        "        -> scoring por terminos, top-2\n"
        "      -> assistant arma respuesta con sources\n"
        "    -> devuelve JSON {answer, sources, context_used}\n"
        "  <- JSON response  -->  Frontend renderiza"
    )

    p.chapter_title("4. Referencias")
    p.ref("Software Architecture in Practice (Bass, Clements, Kazman) - Addison-Wesley")
    p.ref("Documenting Software Architectures (Clements et al.) - Addison-Wesley")
    p.ref("SEI - Carnegie Mellon: Software Architecture Resources")
    p.ref("ISO/IEC 42010: Systems and software engineering - Architecture description")
    p.ref("ACM Digital Library - 'software architecture' 'architectural decisions'")
    p.note("Nota: El SDD debe actualizarse cuando se implemente CAG completamente, agregando "
           "las nuevas vistas y decisiones asociadas al almacen de contexto.")

    p.output(OUTPUT_DIR + "/SDD_Software_Design_Document.pdf")


# ──────────────────────────────────────────
# 2. BDD
# ──────────────────────────────────────────
def make_bdd():
    p = DocPDF()
    p.alias_nb_pages()
    p.title_text = "BDD - Behavior Driven Development"
    p.set_title(p.title_text)
    p.add_page()

    p.chapter_title("1. Introduccion")
    p.body(
        "Behavior Driven Development (BDD) es una metodologia agil que describe el comportamiento "
        "esperado del software en lenguaje natural estructurado. Creada por Dan North (2006), "
        "responde '?que deberia hacer el sistema?' antes de '?como implementarlo?'."
    )
    p.body(
        "Referencia principal: 'Specification by Example' (Gojko Adzic) demuestra que los ejemplos "
        "concretos son la mejor manera de comunicar comportamiento entre negocio y desarrollo. "
        "'BDD in Action' (John Ferguson Smart) es la guia practica de implementacion."
    )

    p.section("1.1 Estructura Given-When-Then")
    p.bullet("Given: contexto inicial (precondiciones del escenario).")
    p.bullet("When: accion que dispara el comportamiento a probar.")
    p.bullet("Then: resultado esperado y verificable.")
    p.body(
        "Esta estructura fuerza a pensar en comportamiento observable, no implementacion interna. "
        "Un escenario BDD bien escrito es entendible por negocio y ejecutable como prueba."
    )

    p.section("1.2 BDD en el Proyecto")
    p.body("Escenarios Gherkin del asistente inteligente:")
    p.code_block(
        "Feature: Asistente Inteligente\n"
        "\n"
        "  Scenario: Pregunta con respuesta en knowledge base\n"
        "    Given el usuario \"student-01\" esta registrado\n"
        "    When pregunta \"Que es RAG?\"\n"
        "    Then el sistema responde con contenido de knowledge_base.json\n"
        "    And la respuesta incluye la fuente \"rag\"\n"
        "    And context_used es una lista vacia\n"
        "\n"
        "  Scenario: Pregunta sin coincidencia\n"
        "    Given el usuario \"student-01\" esta registrado\n"
        "    When pregunta \"Que es la teoria de cuerdas?\"\n"
        "    Then el sistema responde que no encontro informacion\n"
        "\n"
        "  Scenario: Guardar contexto de usuario (CAG)\n"
        "    Given el usuario \"ana\" tiene sesion activa\n"
        "    When guarda contexto con key \"preferred_style\"\n"
        "    Then el sistema responde 201 con saved=true"
    )

    p.add_page()
    p.chapter_title("2. Cobertura de Pruebas Base")
    p.body("Las pruebas base del proyecto validan tres escenarios fundamentales:")
    p.code_block(
        "# test_base_api.py\n"
        "class BaseApiTest(unittest.TestCase):\n"
        "\n"
        "    def test_health_returns_ok(self):\n"
        "        # GET /health -> 200 {\"status\": \"ok\"}\n"
        "        status, body = self.get_json(\"/health\")\n"
        "        self.assertEqual(status, 200)\n"
        "        self.assertEqual(body[\"status\"], \"ok\")\n"
        "\n"
        "    def test_ask_answers_from_knowledge_base(self):\n"
        "        # POST /api/ask -> respuesta con sources\n"
        "        status, body = self.post_json(\"/api/ask\",\n"
        "            {\"user_id\": \"base-user\", \"question\": \"Que es RAG en el curso?\"})\n"
        "        self.assertEqual(status, 200)\n"
        "        self.assertIn(\"RAG recupera\", body[\"answer\"])\n"
        "        self.assertIn(\"rag\", body[\"sources\"])\n"
        "\n"
        "    def test_ask_requires_user_and_question(self):\n"
        "        # Sin question -> 400\n"
        "        with self.assertRaises(HTTPError) as error:\n"
        "            self.post_json(\"/api/ask\", {\"user_id\": \"base-user\"})\n"
        "        self.assertEqual(error.exception.code, 400)"
    )
    p.body(
        "Estas pruebas validan el comportamiento completo del endpoint /api/ask: caso "
        "feliz y caso error. Escribirlas ANTES de implementar el endpoint seria el enfoque "
        "BDD clasico (outside-in)."
    )

    p.chapter_title("3. Pruebas de Validacion CAG")
    p.body("Las pruebas de validacion verifican que el comportamiento CAG funcione:")
    p.code_block(
        "# test_cag_contract.py\n"
        "class CagContractTest(unittest.TestCase):\n"
        "\n"
        "    def test_saves_context_for_user(self):\n"
        "        # POST /api/context -> 201 {\"saved\": true}\n"
        "        status, body = self.post_json(\"/api/context\",\n"
        "            {\"user_id\": \"ana\", \"key\": \"preferred_style\",\n"
        "             \"value\": \"explicaciones con analogias\"})\n"
        "        self.assertEqual(status, 201)\n"
        "        self.assertTrue(body[\"saved\"])\n"
        "\n"
        "    def test_retrieves_context_for_user(self):\n"
        "        # GET /api/context?user_id=ana -> contexto guardado\n"
        "        status, body = self.get_json(\"/api/context?user_id=ana\")\n"
        "        self.assertEqual(status, 200)\n"
        "        self.assertIn({\"key\": \"project\", \"value\": ...}, body[\"context\"])\n"
        "\n"
        "    def test_ask_uses_context_to_influence_response(self):\n"
        "        # Pregunta con contexto -> respuesta personalizada\n"
        "        self.assertIn(\"principiante\", body[\"answer\"].lower())\n"
        "        self.assertIn(\"audience\", body[\"context_used\"])"
    )

    p.chapter_title("4. Referencias")
    p.ref("Specification by Example (Gojko Adzic) - Manning Publications")
    p.ref("BDD in Action (John Ferguson Smart) - Manning Publications")
    p.ref("Cucumber Documentation - cucumber.io")
    p.ref("Behave (Python BDD) - behave.readthedocs.io")
    p.ref("Gherkin Reference - cucumber.io/docs/gherkin")

    p.output(OUTPUT_DIR + "/BDD_Behavior_Driven_Development.pdf")


# ──────────────────────────────────────────
# 3. TDD
# ──────────────────────────────────────────
def make_tdd():
    p = DocPDF()
    p.alias_nb_pages()
    p.title_text = "TDD - Test Driven Development"
    p.set_title(p.title_text)
    p.add_page()

    p.chapter_title("1. Introduccion")
    p.body(
        "Test Driven Development (TDD) es una tecnica donde las pruebas se escriben antes del "
        "codigo de produccion. Ciclo Red-Green-Refactor (Kent Beck, 'Test Driven Development: "
        "By Example', 2002): escribir prueba que falla (RED), codigo minimo para que pase "
        "(GREEN), refactorizar (REFACTOR)."
    )
    p.body(
        "'Growing Object-Oriented Software, Guided by Tests' (Freeman & Pryce) extiende TDD "
        "a nivel de sistemas: el software crece organicamente guiado por pruebas, en lugar "
        "de diseno upfront."
    )

    p.section("1.1 El Ciclo TDD")
    p.bullet("RED: prueba que falla para funcionalidad aun no implementada.")
    p.bullet("GREEN: codigo minimo para que la prueba pase (sin optimizar).")
    p.bullet("REFACTOR: mejorar el codigo manteniendo todas las pruebas verdes.")

    p.section("1.2 Beneficios Medibles")
    p.bullet("40-80% menos bugs en produccion (estudios empiricos, Nagappan et al., 2008).")
    p.bullet("Diseno mas modular y desacoplado (el testing force a interfaces limpias).")
    p.bullet("Documentacion viva: las pruebas describen comportamiento esperado.")
    p.bullet("Refactoring seguro: cualquier cambio verificado al instante.")

    p.add_page()
    p.chapter_title("2. TDD Aplicado al Proyecto")

    p.sub("2.1 Testeo de knowledge.py (algoritmo de scoring)")
    p.body("El corazon del RAG es el scoring por terminos. TDD exige probar los casos limite:")
    p.code_block(
        "class KnowledgeTest(unittest.TestCase):\n"
        "    def test_retrieve_encuentra_coincidencia_parcial(self):\n"
        "        resultado = retrieve_snippets(\"que es RAG\")\n"
        "        self.assertTrue(len(resultado) > 0)\n"
        "        self.assertIn(\"rag\", [r[\"id\"] for r in resultado])\n"
        "\n"
        "    def test_retrieve_sin_coincidencia_retorna_vacio(self):\n"
        "        resultado = retrieve_snippets(\"zyxwvu teoria incognita\")\n"
        "        self.assertEqual(resultado, [])\n"
        "\n"
        "    def test_retrieve_respeta_limite_de_resultados(self):\n"
        "        resultado = retrieve_snippets(\"curso\")\n"
        "        self.assertLessEqual(len(resultado), 2)"
    )

    p.sub("2.2 Testeo de server.py (API REST)")
    p.code_block(
        "class BaseApiTest(unittest.TestCase):\n"
        "    # Ver ejemplos en BDD (seccion 2)\n"
        "    # Los tests base ya cubren: health, ask exitoso, ask con error"
    )

    p.sub("2.3 Testeo de context_store.py (CAG)")
    p.body("Para implementar CAG, TDD dicta escribir estas pruebas primero:")
    p.code_block(
        "class ContextStoreTest(unittest.TestCase):\n"
        "    def test_save_persiste_clave_valor(self):\n"
        "        store = ContextStore()\n"
        "        store.save(\"ana\", \"style\", \"analogias\")\n"
        "        ctx = store.list_for_user(\"ana\")\n"
        "        self.assertIn({\"key\": \"style\", \"value\": \"analogias\"}, ctx)\n"
        "\n"
        "    def test_contexto_aislado_por_usuario(self):\n"
        "        store = ContextStore()\n"
        "        store.save(\"ana\", \"x\", \"1\")\n"
        "        ctx_luis = store.list_for_user(\"luis\")\n"
        "        self.assertEqual(ctx_luis, [])\n"
        "\n"
        "    def test_sobrescribe_misma_clave(self):\n"
        "        store = ContextStore()\n"
        "        store.save(\"ana\", \"tema\", \"SDD\")\n"
        "        store.save(\"ana\", \"tema\", \"BDD\")\n"
        "        ctx = store.list_for_user(\"ana\")\n"
        "        self.assertEqual(len(ctx), 1)\n"
        "        self.assertEqual(ctx[0][\"value\"], \"BDD\")"
    )

    p.chapter_title("3. Pir amide de Testing")
    p.body("Proyecto sigue la piramide clasica:")
    p.bullet("Base: tests unitarios (knowledge, context_store) - rapidos, aislados.")
    p.bullet("Medio: tests de integracion (server con puerto real).")
    p.bullet("Tope: tests de validacion (CAG contract) - cobertura de requisitos del examen.")

    p.chapter_title("4. Referencias")
    p.ref("Test Driven Development: By Example (Kent Beck) - Addison-Wesley")
    p.ref("Growing Object-Oriented Software, Guided by Tests (Freeman & Pryce) - Addison-Wesley")
    p.ref("xUnit Test Patterns (Gerard Meszaros) - Addison-Wesley")
    p.ref("Pytest Documentation - pytest.org")
    p.ref("Nagappan et al., 'Realizing quality improvement through test driven development' (2008)")

    p.output(OUTPUT_DIR + "/TDD_Test_Driven_Development.pdf")


# ──────────────────────────────────────────
# 4. RAG
# ──────────────────────────────────────────
def make_rag():
    p = DocPDF()
    p.alias_nb_pages()
    p.title_text = "RAG - Retrieval-Augmented Generation"
    p.set_title(p.title_text)
    p.add_page()

    p.chapter_title("1. Introduccion")
    p.body(
        "Retrieval-Augmented Generation (RAG) combina recuperacion de informacion con "
        "generacion de lenguaje. En lugar de depender solo del conocimiento interno del "
        "modelo (parametros), RAG recupera fragmentos relevantes de una base documental "
        "externa y los incorpora como contexto."
    )
    p.body(
        "Paper fundacional: 'Retrieval-Augmented Generation for Knowledge-Intensive NLP "
        "Tasks' (Lewis et al., Facebook AI Research, 2020, arXiv:2005.11401). Demostro "
        "que RAG supera a modelos puramente generativos en tasks que requieren conocimiento "
        "factual: QA, verificacion de hechos, traduccion especializada."
    )

    p.section("1.1 Arquitectura RAG")
    p.body("Tres componentes:")
    p.bullet("Indexador: procesa y almacena documentos en formato buscable.")
    p.bullet("Recuperador (Retriever): selecciona fragmentos relevantes dada una consulta.")
    p.bullet("Generador (Generator): LLM que recibe consulta + fragmentos y produce respuesta.")

    p.section("1.2 Implementacion en el Proyecto")
    p.body("knowledge.py implementa un recuperador por coincidencia de terminos (bag-of-words):")
    p.code_block(
        "def retrieve_snippets(question, knowledge_base=None, limit=2):\n"
        "    knowledge_base = knowledge_base or load_knowledge_base()\n"
        "    terms = set(question.lower()\n"
        "                .replace(\"?\", \"\").replace(\",\", \"\").split())\n"
        "    scored = []\n"
        "    for item in knowledge_base:\n"
        "        haystack = f\"{item['title']} {item['content']}\".lower()\n"
        "        score = sum(1 for term in terms if term in haystack)\n"
        "        if score > 0:\n"
        "            scored.append((score, item))\n"
        "    scored.sort(key=lambda pair: pair[0], reverse=True)\n"
        "    return [item for _, item in scored[:limit]]"
    )
    p.body("Base de conocimiento actual (knowledge_base.json):")
    p.code_block(
        '[\n'
        '  {"id": "sdd-bdd-tdd", "title": "SDD, BDD y TDD",\n'
        '   "content": "El curso usa SDD para disenar antes de construir..."},\n'
        '  {"id": "rag", "title": "RAG",\n'
        '   "content": "RAG recupera fragmentos de una base documental..."},\n'
        '  {"id": "cag", "title": "CAG",\n'
        '   "content": "CAG usa contexto persistente..."},\n'
        '  {"id": "jarvis", "title": "Tony Stark y Jarvis",\n'
        '   "content": "La IA debe funcionar como Jarvis..."}\n'
        ']'
    )

    p.add_page()
    p.chapter_title("2. Variantes de RAG")
    p.bullet("RAG Secuencial: recuperar primero, generar despues (enfoque clasico, usado en el proyecto).")
    p.bullet("RAG Iterativo: multiples ciclos recuperacion-generacion para preguntas complejas.")
    p.bullet("RAG con Memoria: incorpora historial de conversacion en la consulta de recuperacion.")
    p.bullet("RAG Hibrido: combina busqueda semantica (vectores/embeddings) con busqueda lexica (BM25).")
    p.note("El proyecto implementa RAG secuencial. Para RAG hibrido se podria integrar "
           "Ollama con embeddings (nomic-embed-text) en el recuperador.")

    p.chapter_title("3. Evaluacion de RAG")
    p.bullet("Exact Match (EM): porcentaje de respuestas que coinciden exactamente con el gold standard.")
    p.bullet("F1 Score: promedio ponderado de precision y recall a nivel de tokens.")
    p.bullet("Faithfulness: que tan fiel es la respuesta a los fragmentos recuperados (evita alucinaciones).")
    p.bullet("Answer Relevance: que tan relevante es la respuesta para la pregunta original.")
    p.body(
        "Para este proyecto, las pruebas base verifican que la respuesta CONTENGA el "
        "fragmento esperado (assertIn), validando faithfulness implicita."
    )

    p.chapter_title("4. Referencias")
    p.ref("RAG Paper: Lewis et al. (2020) - arXiv:2005.11401")
    p.ref("Designing Machine Learning Systems (Chip Huyen) - O'Reilly")
    p.ref("LangChain RAG Documentation - python.langchain.com")
    p.ref("Google Scholar - Retrieval-Augmented Generation")
    p.ref("RAGAS (RAG Assessment) - docs.ragas.io")

    p.output(OUTPUT_DIR + "/RAG_Retrieval_Augmented_Generation.pdf")


# ──────────────────────────────────────────
# 5. CAG
# ──────────────────────────────────────────
def make_cag():
    p = DocPDF()
    p.alias_nb_pages()
    p.title_text = "CAG - Context-Augmented Generation"
    p.set_title(p.title_text)
    p.add_page()

    p.chapter_title("1. Introduccion")
    p.body(
        "Context-Augmented Generation (CAG) es la evolucion conceptual de RAG que enfatiza "
        "contexto persistente y estructurado del USUARIO (no conocimiento general). "
        "Mientras RAG recupera de una base documental general, CAG incorpora preferencias, "
        "historial y decisiones del usuario para personalizar respuestas."
    )
    p.body(
        "CAG no tiene un paper fundacional unico. Su fundamento teorico se encuentra en "
        "'Building LLM Powered Applications' (Valentina Alto, O'Reilly) y 'Design Patterns "
        "for Large Language Models' (O'Reilly). Estas obras documentan patrones de memoria: "
        "episodica (conversaciones pasadas), semantica (perfil del usuario) y de trabajo "
        "(estado actual de la sesion)."
    )

    p.section("1.1 RAG vs CAG")
    p.bullet("RAG: conocimiento publico/general desde base documental estatica.")
    p.bullet("CAG: contexto privado/especifico del usuario, dinamico durante la interaccion.")
    p.bullet("RAG responde factualmente; CAG personaliza segun el usuario.")

    p.add_page()
    p.chapter_title("2. Estado Actual en el Proyecto")

    p.body("context_store.py (placeholder - PENDIENTE de implementar):")
    p.code_block(
        "class ContextStore:\n"
        "    def save(self, user_id, key, value):\n"
        "        raise NotImplementedError(\"CAG context storage is not implemented yet\")\n"
        "\n"
        "    def list_for_user(self, user_id):\n"
        "        raise NotImplementedError(\"CAG context retrieval is not implemented yet\")"
    )
    p.body("cag.py (placeholder - PENDIENTE de implementar):")
    p.code_block(
        "def apply_context(user_id, question, base_answer, context_items):\n"
        "    return base_answer"
    )

    p.section("2.1 Lo Que el Examen Pide Implementar")
    p.body("Segun las pruebas de validacion (test_cag_contract.py), CAG debe:")
    p.bullet("POST /api/context -> guardar clave-valor por usuario (status 201, saved=true).")
    p.bullet("GET /api/context?user_id=X -> recuperar contexto (status 200, lista de items).")
    p.bullet("POST /api/ask con contexto previo -> respuesta influenciada por contexto (context_used con la clave).")

    p.section("2.2 Estrategia de Implementacion Sugerida")
    p.sub("Paso 1: context_store.py - almacen en memoria")
    p.code_block(
        "class ContextStore:\n"
        "    def __init__(self):\n"
        "        self._data = {}  # {user_id: {key: value}}\n"
        "\n"
        "    def save(self, user_id, key, value):\n"
        "        if user_id not in self._data:\n"
        "            self._data[user_id] = {}\n"
        "        self._data[user_id][key] = value\n"
        "        return True\n"
        "\n"
        "    def list_for_user(self, user_id):\n"
        "        items = self._data.get(user_id, {})\n"
        "        return [{\"key\": k, \"value\": v} for k, v in items.items()]"
    )
    p.sub("Paso 2: cag.py - inyectar contexto en respuesta")
    p.code_block(
        "def apply_context(user_id, question, base_answer, context_items):\n"
        "    if not context_items:\n"
        "        return base_answer\n"
        "    ctx_str = \"; \".join(\n"
        "        f\"{c['key']}: {c['value']}\" for c in context_items)\n"
        "    return f\"{base_answer} [Contexto: {ctx_str}]\""
    )

    p.chapter_title("3. Patrones de Memoria para CAG")
    p.bullet("Memoria Episodica: historial de preguntas y respuestas anteriores del usuario.")
    p.bullet("Memoria Semantica: preferencias del usuario (nivel, formato, temas de interes).")
    p.bullet("Memoria de Trabajo: estado transitorio de la sesion actual.")
    p.note("Para una implementacion completa, context_store podria persistir a disco "
           "(JSON/ SQLite) en lugar de solo memoria volatil.")

    p.chapter_title("4. Referencias")
    p.ref("Building LLM Powered Applications (Valentina Alto) - O'Reilly")
    p.ref("Design Patterns for Large Language Models - O'Reilly")
    p.ref("ACM Digital Library - 'context aware systems', 'software traceability'")
    p.ref("arXiv - LLM Context & Memory")
    p.ref("O'Reilly - LLM Architecture and Design Patterns")

    p.output(OUTPUT_DIR + "/CAG_Context_Augmented_Generation.pdf")


# ──────────────────────────────────────────
# Run all
# ──────────────────────────────────────────
if __name__ == "__main__":
    for name, fn in [("SDD", make_sdd), ("BDD", make_bdd), ("TDD", make_tdd),
                      ("RAG", make_rag), ("CAG", make_cag)]:
        print(f"Generando {name}...")
        fn()
    print(f"\nCompletado. PDFs en: {OUTPUT_DIR}")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith(".pdf"):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  -> {f} ({sz:,} bytes)")
