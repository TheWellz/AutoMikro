import os, sys, time, threading  

# Obtem o caminho do main.py e adiciona ao sys.path para permitir importações relativas.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ChromaDB.busca import buscar_com_query
from ChromaDB.ingestao import atualizar_banco
from LLM.ollama import buscar_com_query_tecnica, manter_ativo

# Inicia uma thread para manter o modelo Ollama ativo.
evento_parar_thread = threading.Event()
thread_manter_ativo = threading.Thread(
    target=manter_ativo,
    args=(evento_parar_thread,),
    daemon=True
)
thread_manter_ativo.start()


def menu_principal():
    while True:
        print("\n" + "="*50)
        print("         SISTEMA AUTOMIKRO - FILTRAGEM DE FIREWALL")
        print("="*50)
        print("[1] 🔄 Reindexar Manuais (Alimentar o Banco de Dados)")
        print("[2] 💬 Tradução de Intenção (Converter Linguagem Natural para CLI)")
        print("[3] ❌ Sair")
        print("-"*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        # Atualiza o banco de dados com os manuais técnicos.
        if opcao == "1":
            print("\n--- INICIANDO INGESTAO ---")
            atualizar_banco()
            print("--------------------------")

        # Consulta o modelo Ollama usando a dúvida e o contexto do RAG.    
        elif opcao == "2":
            pergunta = input("\nDigite sua dúvida sobre Firewall MikroTik: ").strip()
            if not pergunta:
                print("A pergunta não pode ser vazia.")
                continue
                
            tempo_inicial = time.time()
                
            print("\n[1/2] 🔍 Executando varredura padrão nos MANUAIS TÉCNICOS...")
            contexto = buscar_com_query(pergunta, contexto)
            
            if not contexto:
                print("⚠️ Nenhum manual correspondente foi encontrado no banco.")
                continue
                
            print("[2/2] 🧠 Analisando contexto técnico e gerando resposta com o Ollama...")
            resposta_ia = buscar_com_query_tecnica(pergunta, contexto)
            
            print("\n" + "="*50)
            print("🤖 RESPOSTA FINAL DO ASSISTENTE:")
            print("="*50)
            print(resposta_ia)
            print("="*50)

            tempo_final = time.time()
            tempo_total = tempo_final - tempo_inicial
            print(f"⏱️ Tempo total de processamento: {tempo_total:.2f} segundos")
            print("="*50)
            
        elif opcao == "3":
            print("\nEncerrando o AutoMikro. Até mais!")
            evento_parar_thread.set()
            thread_manter_ativo.join(timeout=2)
            break
        else:
            print("Opção inválida! Tente novamente.")
            
# Garante que o script seja executado a partir do diretório correto e inicia o menu principal.
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    menu_principal()