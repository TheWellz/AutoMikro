import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Configuração do "Tradutor" (Embedding)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Configuração do "Cérebro" (LLM Local - Llama 3 via Ollama)
#Settings.llm = Ollama(model="qwen2.5:1.5b", request_timeout=300.0)
Settings.llm = None

def buscar_com_query(pergunta):
    # Conecta ao banco existente
    db = chromadb.PersistentClient(path="./meu_banco_local")
    chroma_collection = db.get_collection("documentos_mikrotik")
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Carrega o índice do banco
    index = VectorStoreIndex.from_vector_store(vector_store)
    
    # Cria o motor de consulta (Query Engine)
    # Aqui ele busca os pedaços E o Llama 3 lê para te dar a resposta final
    query_engine = index.as_query_engine(similarity_top_k=3)
    
    resposta = query_engine.query(pergunta)
    return resposta

p = input("Qual sua duvida? ")
print(f"\nConsultando o banco sobre: {p}")
    
resultado = buscar_com_query(p)
    
print("\n--- RESPOSTA FINAL ---")
print(resultado)