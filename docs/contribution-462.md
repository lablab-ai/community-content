# 🎓 **Tutorial Completo de Vectara Chat**  
*Desarrollado por @mau16ro – Experto en IA Conversacional*  

---  

## 📚 Índice

1. [Introducción a Vectara Chat](#1-introducción-a-vectara-chat)  
2. [Requisitos Previos](#2-requisitos-previos)  
3. [Arquitectura y Conceptos Clave](#3-arquitectura-y-conceptos-clave)  
4. [Crear y Configurar tu Cuenta Vectara](#4-crear-y-configurar-tu-cuenta-vectara)  
5. [Instalación del SDK y Herramientas CLI](#5-instalación-del-sdk-y-herramientas-cli)  
6. [Preparación de los Datos](#6-preparación-de-los-datos)  
   - 6.1 [Formato de documentos](#61-formato-de-documentos)  
   - 6.2 [Limpieza y normalización](#62-limpieza-y-normalización)  
7. [Indexado de Contenido](#7-indexado-de‑contenido)  
   - 7.1 [Creación de un Corpus](#71-creación-de-un-corpus)  
   - 7.2 [Carga de documentos (Python, Node.js, cURL)](#72-carga-de-documentos)  
   - 7.3 [Configuración de embeddings y parámetros de indexación](#73-configuración-de-embeddings)  
8. [Construir tu Primer Bot Conversacional](#8-construir-tu-primer-bot-conversacional)  
   - 8.1 [Flujo de conversación básico](#81-flujo-de-conversación-básico)  
   - 8.2 [Uso del endpoint **/search** (retrieval) y **/chat** (generación) ](#82-uso-de-los-endpoints)  
9. [Integración en Aplicaciones Front‑End](#9-integración-en-aplicaciones-front‑end)  
   - 9.1 [React + Vectara Chat SDK](#91-react)  
   - 9.2 [Web Components (vanilla JS)](#92-web‑components)  
10. [Control de Contexto y Memoria a Largo Plazo](#10-control-de-contexto-y-memoria-a‑largo-plazo)  
11. [Seguridad y Gobernanza](#11-seguridad-y-gobernanza)  
12. [Escalado y Optimización de Costos](#12-escalado-y-optimización-de-costos)  
13. [Monitoreo, Logging y Métricas](#13-monitoreo-logging‑y-métricas)  
14. [Testing Automatizado y CI/CD](#14-testing‑automatizado‑y‑cicd)  
15. [Depuración y Manejo de Errores Comunes](#15-depuración-y-manejo-de‑errores‑comunes)  
16. [Mejores Prácticas y Tips Avanzados](#16-mejores‑prácticas‑y‑tips‑avanzados)  
17. [FAQ – Preguntas Frecuentes](#17-faq)  
18. [Recursos Adicionales](#18-recursos-adicionales)  

---  

## 1️⃣ Introducción a Vectara Chat  

Vectara Chat es una **plataforma de IA conversacional** basada en **retrieval‑augmented generation (RAG)**. Combina un motor de búsqueda semántica de alta velocidad con LLMs de última generación para ofrecer respuestas precisas y contextualmente relevantes, manteniendo bajo coste y alta latencia (< 100 ms en la mayoría de los casos).  

### Principales ventajas  

| Característica | Qué aporta | Por qué importa |
|----------------|------------|-----------------|
| **Búsqueda semántica en tiempo real** | Embeddings de alta calidad + HNSW index | Respuestas basadas en datos reales, no “alucina”. |
| **RAG integrado** | El motor llama a LLM solo cuando es necesario | Reduce consumo de tokens y coste. |
| **Multilingüe y dominio‑agnóstico** | Soporta > 100 idiomas, sin re‑entrenamiento | Ideal para productos globales. |
| **Control de filtro y políticas** | ACL, “ground‑truth” boosting, red‑teaming | Cumplimiento regulatorio. |
| **SDKs multi‑lenguaje** | Python, Node.js, Go, Java, cURL | Fácil integración en cualquier stack. |

---  

## 2️⃣ Requisitos Previos  

| Necesario | Versión mínima recomendada |
|-----------|----------------------------|
| **Cuenta Vectara** | Registro gratuito (plan de prueba) |
| **Python** | 3.9+ (virtualenv o conda) |
| **Node.js** | 18.x LTS |
| **cURL** | 7.68+ |
| **Git** | 2.30+ |
| **Docker** | 20.10+ (opcional, para despliegues) |
| **Conexión a Internet** | Permitir salida a `*.vectara.com` (puertos 443) |

> **Tip:** Usa un entorno virtual (`python -m venv venv && source venv/bin/activate`) para evitar conflictos de dependencias.

---  

## 3️⃣ Arquitectura y Conceptos Clave  

```
+----------------------+       +------------------------+
|  Cliente (Web/Mobile) | <---> |   Vectara API Gateway   |
+----------------------+       +-----------+------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
        +------v------+                                      +-----v------+
        |   Search    |   (HNSW, PQ, IVF)                     |   LLM      |
        |  Service    |  <--->  Index (Embeddings)  <--->     | Generator |
        +-------------+                                      +-----------+
```

- **Corpus**: conjunto lógico de documentos que se indexan.  
- **Index**: estructura HNSW (Hierarchical Navigable Small World) que permite búsquedas vectoriales O(log N).  
- **Retrieval**: consulta semántica que devuelve los *k* fragmentos más relevantes.  
- **RAG**: los fragmentos se envían a un LLM (OpenAI, Anthropic, Cohere, etc.) para generar una respuesta.  

---  

## 4️⃣ Crear y Configurar tu Cuenta Vectara  

1. Regístrate en <https://console.vectara.com>.  
2. En el **Dashboard**, crea un **Project** → *Nombre del proyecto* (ej. `vectara-chat-demo`).  
3. Dentro del proyecto, genera una **API Key** con permisos **Read/Write**. Copia el valor; lo necesitarás en los ejemplos.  
4. (Opcional) Configura un **Billing Alert** para no exceder el presupuesto de la cuenta de prueba.  

---  

## 5️⃣ Instalación del SDK y Herramientas CLI  

### 5.1 Python  

```bash
pip install vectara-client==0.12.0
```

### 5.2 Node.js  

```bash
npm i @vectara/client@0.12.0
```

### 5.3 CLI (cURL)  

No hay instalación; sólo necesitas `curl`.  

---  

## 6️⃣ Preparación de los Datos  

### 6.1 Formato de documentos  

Vectara acepta los siguientes formatos:

| Tipo | Extensión | Comentario |
|------|-----------|------------|
| Texto plano | `.txt` | UTF‑8 |
| Markdown | `.md` | Se preservan encabezados |
| HTML | `.html` | Se extrae el texto visible |
| JSON (array de objetos) | `.json` | Cada objeto debe contener `id` y `content` |

> **Ejemplo JSON**  

```json
[
  {
    "id": "doc-001",
    "title": "Introducción a Vectara",
    "content": "Vectara es una plataforma..."
  },
  {
    "id": "doc-002",
    "title": "Guía de instalación",
    "content": "Para instalar el SDK..."
  }
]
```

### 6.2 Limpieza y normalización  

```python
import re, unicodedata

def clean_text(txt: str) -> str:
    txt = unicodedata.normalize("NFKC", txt)          # Normaliza Unicode
    txt = re.sub(r"\s+", " ", txt)                    # Reduce espacios
    txt = txt.strip()
    return txt
```

- **Eliminar HTML tags** (si subes HTML): `BeautifulSoup(text, "html.parser").get_text()`.  
- **Chunking**: Vectara recomienda fragmentos de **300‑500 tokens**. Usa la utilidad `vectara-client.chunk_text(...)` o implementa tu propio splitter.

---  

## 7️⃣ Indexado de Contenido  

### 7.1 Creación de un Corpus  

```bash
curl -X POST "https://api.vectara.io/v1/corpora" \
 -H "Authorization: Bearer <API_KEY>" \
 -H "Content-Type: application/json" \
 -d '{
       "name": "demo-corpus",
       "description": "Corpus de demo para tutorial",
       "language": "es"
     }'
```

Guarda el `corpus_id` retornado (ej. `123456`).  

### 7.2 Carga de documentos  

#### Python  

```python
from vectara.client import VectaraClient

client = VectaraClient(api_key="YOUR_API_KEY", endpoint="api.vectara.io")
corpus_id = 123456

# Cargar varios documentos a la vez
docs = [
    {"id": "doc-001", "title": "Intro", "content": clean_text(open("intro.txt").read())},
    {"id": "doc-002", "title": "Instalación", "content": clean_text(open("install.md").read())}
]

response = client.index_documents(corpus_id=corpus_id, documents=docs)
print("Indexed:", response)
```

#### Node.js  

```javascript
const { VectaraClient } = require("@vectara/client");
const fs = require("fs");

const client = new VectaraClient({ apiKey: "YOUR_API_KEY", endpoint: "api.vectara.io" });
const corpusId = 123456;

const docs = [
  { id: "doc-001", title: "Intro", content: fs.readFileSync("./intro.txt","utf8").trim() },
  { id: "doc-002", title: "Instalación", content: fs.readFileSync("./install.md","utf8").trim() }
];

(async () => {
  const resp = await client.indexDocuments({ corpusId, documents: docs });
  console.log("Indexed:", resp);
})();
```

#### cURL (para un único documento)  

```bash
curl -X POST "https://api.vectara.io/v1/indexes/123456/documents" \
 -H "Authorization: Bearer <API_KEY>" \
 -H "Content-Type: application/json" \
 -d '{
       "documents": [
         {
           "id": "doc-003",
           "title": "FAQ",
           "content": "¿Cómo funciona Vectara?"
         }
       ]
     }'
```

### 7.3 Configuración de embeddings y parámetros de indexación  

| Parámetro | Valor por defecto | Recomendación |
|-----------|-------------------|---------------|
| `embedding_model` | `text-embedding-3-large` (OpenAI) | Cambia a `multilingual-e5-large` si trabajas con varios idiomas. |
| `distance_metric` | `cosine` | Usa `dot_product` si tu LLM está entrenado para ello. |
| `hnsw_m` | `32` | Aumenta a `64` para corpus > 10 M docs (mayor recall). |
| `ef_construction` | `200` | Mantén > 100 para mejor calidad de indexado. |

Ejemplo de actualización del corpus:

```bash
curl -X PATCH "https://api.vectara.io/v1/corpora/123456" \
 -H "Authorization: Bearer <API_KEY>" \
 -H "Content-Type: application/json" \
 -d '{
       "embedding_model": "multilingual-e5-large",
       "hnsw_m": 64,
       "ef_construction": 250
     }'
```

---  

## 8️⃣ Construir tu Primer Bot Conversacional  

### 8.1 Flujo de conversación básico  

1. **Usuario** envía una pregunta.  
2. **Cliente** llama a **/search** → recupera *k* fragmentos relevantes.  
3. Los fragmentos se concatenan con la pregunta y se envían a **/chat** (LLM).  
4. **Respuesta** se muestra al usuario y, opcionalmente, se guarda en el *session memory*.

### 8.2 Uso de los endpoints  

#### 8.2.1 Endpoint **/search** (retrieval)

```python
search_resp = client.search(
    corpus_id