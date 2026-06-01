import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter

# Configuração do Modelo
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def atualizar_banco():
    print("Iniciando Ingestão de documentos...")
    
    # Conecta ao Chroma
    db = chromadb.PersistentClient(path="./meu_banco_local")
    chroma_collection = db.get_or_create_collection("documentos_mikrotik")
    
    # Configura o armazenamento
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Lê os arquivos (PDF, TXT, DOCX)
    documentos = SimpleDirectoryReader("./meus_manuais").load_data()
    
    # Cria o índice e SALVA no banco
    VectorStoreIndex.from_documents(
        documentos, 
        storage_context=storage_context,
        show_progress=True
    )
    
    print(f"Sucesso! O banco agora tem {chroma_collection.count()} fatias.")

if __name__ == "__main__":
    atualizar_banco()