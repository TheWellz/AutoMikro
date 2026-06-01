import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# --- 1. CONFIGURAÇÃO DO MODELO DE IA (O MAESTRO) ---
# Aqui definimos globalmente que o LlamaIndex usará o MiniLM-L12 para tudo
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# --- 2. INICIALIZAÇÃO DO CLIENTE E COLEÇÃO ---
print("Iniciando o ChromaDB Persistente...")
chroma_client = chromadb.PersistentClient(path="./meu_banco_local")

# Criamos/Carregamos a coleção específica para o MikroTik
chroma_collection = chroma_client.get_or_create_collection(name="documentos_mikrotik")

# --- 3. PREPARAÇÃO DA PONTE (STORAGE CONTEXT) ---
# Conectamos o LlamaIndex ao armazenamento do ChromaDB
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# --- 4. INGESTÃO AUTOMÁTICA DE ARQUIVOS ---
print("Lendo manuais da pasta './meus_manuais'...")
# O SimpleDirectoryReader lê PDFs, TXTs, etc., de uma vez só
documentos = SimpleDirectoryReader("./meus_manuais").load_data()

# --- 5. CRIAÇÃO DO ÍNDICE (TRANSFORMAÇÃO EM VETORES) ---
# O LlamaIndex pega os documentos, quebra em pedaços e salva no ChromaDB
index = VectorStoreIndex.from_documents(
    documentos, 
    storage_context=storage_context
)

# --- 6. GERENCIAMENTO E DIAGNÓSTICO ---
print(f"\nSucesso! {len(documentos)} arquivos foram indexados.")
print(f"Total de registros (pedaços de texto) no banco: {chroma_collection.count()}")

query_engine = index.as_query_engine()

pergunta = "O que é Connection Tracking e para que serve?"
print(f"\nConsultando: {pergunta}")

# A resposta buscará nos 554 pedaços e trará a melhor combinação
resposta = query_engine.query(pergunta)

print("\n--- RESPOSTA DA IA ---")
print(resposta)




# Exemplo: Se precisar apagar a coleção para começar do zero
# chroma_client.delete_collection(name="documentos_mikrotik")

# --- PROCESSO DE BUSCA ---
# Define a pergunta em linguagem natural e executa a busca semântica
#pergunta = "Como posso impedir que invasores acessem minha rede interna?"
#print(f"\nBuscando por: '{pergunta}'")

#resultados = collection.query(
 #   query_texts=[pergunta],
 #   n_results=1,
    #where={"setor": "infra"}
#)

# --- EXIBIÇÃO DE RESULTADOS ---
# Mostra o documento mais relevante encontrado pela IA
#print("\n--- Resultado mais próximo ---")
#print(f"Texto: {resultados['documents'][0][0]}") 
#print(f"ID: {resultados['ids'][0][0]}")

# Verifica se o banco de dados está ativo e respondendo
#print(f"\nStatus do Banco (Heartbeat): {chroma_client.heartbeat()}")