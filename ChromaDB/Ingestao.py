import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# Define o modelo de IA multi-linguagem para fazer os embeddings dos documentos.
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-m3"
)

def atualizar_banco():
    print("Iniciando Ingestão de documentos...")
    
    db = chromadb.PersistentClient(path="./Banco_vetorial")  # Inicializa uma conexão local com o banco vetorial.
    
    try:
        db.delete_collection("documentos_mikrotik")
        print("Coleção antiga removida para atualização limpa.")
    except Exception:
        pass
    
    mikrotik_collection = db.get_or_create_collection("documentos_mikrotik") # Cria ou obtém a coleção de documentos mikrotik.
    vector_store = ChromaVectorStore(chroma_collection=mikrotik_collection) # Conecta a coleção do MikroTik ao framework LhamaIndex.
    storage_context = StorageContext.from_defaults(vector_store=vector_store) # Define onde os índices e vetores serão salvos fisicamente no ChromaDB.

    documentos = []

    print("Processando manuais...")
    try:
        # Transforma os documentos em vetores e os armazena no banco vetorial.
        docs_explicacao = SimpleDirectoryReader("./Documentos_txt").load_data()
        documentos.extend(docs_explicacao)
    except Exception as e:
        print(f"Aviso ao ler documentos_txt: {e}")
        
    if not documentos:
        print("❌ Nenhum documento encontrado nas pastas para indexação!")
        return
    
    # Converte os documentos em vetores e os salva no banco.
    VectorStoreIndex.from_documents(
        documentos, 
        storage_context=storage_context,
        show_progress=True
    )
    
    print(f"Sucesso! O banco agora tem {mikrotik_collection.count()} fatias catalogadas.")