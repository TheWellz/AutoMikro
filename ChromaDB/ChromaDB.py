import chromadb
from chromadb.utils import embedding_functions

# --- CONFIGURAÇÃO DO MODELO DE IA ---
# Define o modelo que entende português para transformar texto em números (vetores)
modelo_portugues = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# --- INICIALIZAÇÃO DO CLIENTE ---
# Configura o banco para salvar os dados permanentemente na pasta local especificada
print("Iniciando o ChromaDB Persistente...")
chroma_client = chromadb.PersistentClient(path="./meu_banco_local")

# --- GERENCIAMENTO DE COLEÇÃO ---
# Cria a pasta 'documentos' ou a carrega se já existir, incluindo os metadados descritivos
collection = chroma_client.get_or_create_collection(
    name="documentos",
    embedding_function=modelo_portugues,
    metadata={"description": "Banco de dados sobre receitas, mecânica e saúde", "prioridade": "alta"}
)

# --- INGESTÃO DE DADOS ---
# Adiciona os textos ao banco. O 'upsert' evita duplicatas se o ID já existir
collection.upsert(
    ids=["doc_rota", "doc_subrede", "doc_firewall"],
    documents=[
        "Para configurar uma rota estática, você deve definir o IP de destino, a máscara de sub-rede e o endereço do próximo salto (gateway) para que o roteador saiba para onde enviar o tráfego.",
        "A criação de sub-redes (subnetting) envolve a divisão de uma rede IP principal em segmentos menores, utilizando a máscara de rede para otimizar o tráfego e melhorar a organização dos endereços.",
        "A configuração do Firewall no roteador é essencial para a segurança, permitindo criar regras que filtram pacotes de entrada e saída para impedir acessos não autorizados e ataques externos."
    ],
    metadatas=[
        {"setor": "infra", "dificuldade": "media", "tipo": "roteamento"},
        {"setor": "infra", "dificuldade": "alta", "tipo": "endereçamento"},
        {"setor": "seguranca", "dificuldade": "media", "tipo": "protecao"}
    ]
)

# --- PROCESSO DE BUSCA ---
# Define a pergunta em linguagem natural e executa a busca semântica
pergunta = "Como posso impedir que invasores acessem minha rede interna?"
print(f"\nBuscando por: '{pergunta}'")

resultados = collection.query(
    query_texts=[pergunta],
    n_results=1,
    #where={"setor": "infra"}
)

# --- EXIBIÇÃO DE RESULTADOS ---
# Mostra o documento mais relevante encontrado pela IA
print("\n--- Resultado mais próximo ---")
print(f"Texto: {resultados['documents'][0][0]}") 
print(f"ID: {resultados['ids'][0][0]}")

# --- GERENCIAMENTO E LISTAGEM ---
# Lista todas as coleções presentes no banco de dados atual
todas_colecoes = chroma_client.list_collections()
print(f"Eu tenho {len(todas_colecoes)} coleções cadastradas.")
for col in todas_colecoes:
    print(f"Nome: {col.name}")

# --- INSPEÇÃO E DIAGNÓSTICO ---
# Mostra a quantidade de itens e uma amostra dos dados armazenados
print(f"Total de registros na coleção: {collection.count()}")
print("Dando uma espiadinha nos primeiros dados:")
print(collection.peek()) 

# Verifica se o banco de dados está ativo e respondendo
print(f"\nStatus do Banco (Heartbeat): {chroma_client.heartbeat()}")