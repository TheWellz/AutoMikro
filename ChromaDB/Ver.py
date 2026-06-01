import chromadb

# 1. Conecta ao teu banco local
db = chromadb.PersistentClient(path="./meu_banco_local")

# 2. Acede à tua coleção
chroma_collection = db.get_collection("documentos_mikrotik")

# 3. O comando que "mostra tudo"
# Incluímos 'documents' e 'metadatas' para ver o conteúdo e a origem
resultado = chroma_collection.get(include=["documents", "metadatas"])

# 4. Exibe de forma organizada
print(f"\nTotal de fatias encontradas: {len(resultado['documents'])}\n")

for i in range(len(resultado['documents'])):
    print(f"--- FATIA {i+1} ---")
    print(f"CONTEÚDO: {resultado['documents'][i]}")
    print(f"METADADOS: {resultado['metadatas'][i]}")
    print("-" * 30)