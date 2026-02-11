# Documentação do Notebook `rag/notebooks/rag_demo.ipynb`

## Objetivo
Este notebook demonstra um pipeline mínimo de Retrieval-Augmented Generation (RAG) usando:
- LangChain para orquestração
- ChromaDB como vector store local
- Embeddings `sentence-transformers`
- LLM via OpenAI ou Ollama

## Fluxo do notebook
O fluxo implementado é:
1. Carregar documento texto
2. Fazer chunking com sobreposição
3. Gerar embeddings e indexar no Chroma
4. Recuperar chunks semanticamente relevantes
5. Gerar resposta com contexto recuperado

## Estrutura por etapas

### 1) Setup de LLM
Arquivo/célula helper define `get_llm(provider="openai")` com suporte a:
- `openai` (`ChatOpenAI`, exige `OPENAI_API_KEY`)
- `ollama` (`ChatOllama`, para execução local)

Também carrega variáveis de ambiente com `load_dotenv()`.

### 2) Imports principais
O notebook usa:
- `TextLoader` para ingestão de documento
- `RecursiveCharacterTextSplitter` para chunking
- `HuggingFaceEmbeddings` para vetorizar texto
- `Chroma` para indexação e busca vetorial
- `ChatPromptTemplate` para template de prompt

### 3) Carga de documento de exemplo
Cria um arquivo `data/sample_doc.txt` com texto curto e carrega em `docs` via `TextLoader`.

Formato de `docs`:
- tipo: `list[Document]`
- cada `Document` possui:
  - `page_content` (conteúdo textual)
  - `metadata` (metadados como `source`)

### 4) Chunking
Usa:
- `chunk_size=180`
- `chunk_overlap=20`

Resultado em `chunks` (`list[Document]`), pronto para embedding.

### 5) Embeddings e indexação
Instancia `HuggingFaceEmbeddings` com:
- modelo: `sentence-transformers/all-MiniLM-L6-v2`
- dispositivo: CPU

Depois cria o vector store:
- `Chroma.from_documents(...)`
- persistência local em `data/chroma_store`

### 6) Retrieval
Configura retriever por similaridade:
- `search_type="similarity"`
- `k=2`

Executa consulta semântica (`get_relevant_documents`) e imprime os chunks retornados.

### 7) Geração (RAG)
Monta prompt com contexto recuperado e pergunta do usuário.
A função `rag_pipeline(question: str)`:
1. recupera documentos relevantes
2. concatena contexto
3. invoca a cadeia `prompt_template | llm`
4. retorna `.content` da resposta

## Arquivos e pastas gerados
Durante execução, o notebook cria/usa:
- `rag/notebooks/data/sample_doc.txt`
- `rag/notebooks/data/chroma_store/` (índice vetorial persistido)

Observação: se executar o notebook a partir da raiz do projeto, os paths relativos podem ser criados em `./data/...`.

## Dependências necessárias
No ambiente Python do notebook, garantir:
- `langchain`
- `langchain-openai`
- `langchain-ollama`
- `langchain-community`
- `langchain-text-splitters`
- `sentence-transformers`
- `python-dotenv`
- `chromadb` (normalmente instalado como dependência do `langchain-community`, mas pode ser instalado explicitamente)

## Variáveis de ambiente
Para usar OpenAI:
- `OPENAI_API_KEY` no `.env`

Exemplo (`.env`):

```env
OPENAI_API_KEY=sk-...
```

## Problemas comuns

### `ModuleNotFoundError: No module named 'langchain.text_splitter'`
Use:
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

### `ModuleNotFoundError: No module named 'langchain.schema'`
Use:
```python
from langchain_core.messages import HumanMessage
```

### `Could not import sentence_transformers`
Instale:
```bash
pip install -U sentence-transformers
```

### Aviso do `tqdm` (`IProgress not found`)
Instale widgets do Jupyter:
```bash
conda install -c conda-forge ipywidgets jupyterlab notebook
```

## Como executar
1. Ative o ambiente (`ailab311` ou equivalente)
2. Instale dependências do `requirements.txt`
3. Abra `rag/notebooks/rag_demo.ipynb`
4. Execute células em ordem
5. Valide respostas de `rag_pipeline(...)`

## Extensões sugeridas
- Trocar `TextLoader` por `PyPDFLoader`
- Testar chunk sizes diferentes
- Comparar modelos de embedding
- Reabrir índice persistido do Chroma em nova sessão
