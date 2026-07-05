import os
import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Define o modelo de IA multi-linguagem para fazer os embeddings dos documentos.
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-m3"
)

Settings.llm = None

def buscar_com_query(pergunta):
    db = chromadb.PersistentClient(path="./Banco_vetorial") # Inicializa uma conexão local com o banco vetorial.
    mikrotik_collection = db.get_collection("documentos_mikrotik") # Obtém a coleção de documentos mikrotik do banco vetorial.
    
    vector_store = ChromaVectorStore(chroma_collection=mikrotik_collection) # Conecta a coleção do MikroTik ao framework para permitir buscas.
    index = VectorStoreIndex.from_vector_store(vector_store) # Cria um índice de busca a partir do banco vetorial.
    query_engine = index.as_query_engine(similarity_top_k=5) # Configura o motor para retornar os 5 melhores documentos por proximidade semântica.
    
    resposta = query_engine.query(pergunta) # Executa a consulta no índice.

    texto_formatado = ""
    for trecho_encontrado in resposta.source_nodes:
        caminho_completo = trecho_encontrado.node.metadata.get("file_path", "Arquivo não identificado") # 
        nome_arquivo = os.path.basename(caminho_completo) # Extrai apenas o nome do arquivo do caminho completo.
        conteudo_texto = trecho_encontrado.node.get_content() # Extrai apenas o conteúdo textual do trecho encontrado.
        
        texto_formatado += f"{nome_arquivo}\n{conteudo_texto}\n\n"
        
    return texto_formatado.strip()