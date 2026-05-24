import chromadb

print("Iniciando o ChromaDB Persistente...")
# Agora os dados serão salvos em uma pasta chamada 'meu_banco_local' na sua Desktop
chroma_client = chromadb.PersistentClient(path="./meu_banco_local")

# Abre a coleção existente ou cria se for a primeira vez
collection = chroma_client.get_or_create_collection(name="my_collection")

# Insere ou atualiza os dados
collection.upsert(
    ids=["id1", "id2"],
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ]
)

# Faz a busca
results = collection.query(
    query_texts=["This is a query document about hawaii"],
    n_results=2
)

print("\n--- Resultado da Busca ---")
print(results['documents'])

# Testando o Heartbeat (Pulsação)
print(f"\nStatus do Banco (Heartbeat): {chroma_client.heartbeat()}")