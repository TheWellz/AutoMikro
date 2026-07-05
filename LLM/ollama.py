import requests, time

# Envia o prompt ao modelo e retorna a resposta gerada.
def gerar(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {                       
        "model": "qwen3:4b-instruct",  # Modelo usado para gerar a resposta
        "prompt": f"""
            {prompt}                
                """,                   # Texto enviado ao modelo      
        "stream": False                
    }

    try:
        response = requests.post(url, json=payload)   
        response.raise_for_status()                    
        
        response_data = response.json()                

        return response_data.get('response', 'Nenhuma resposta recebida do modelo.')  
        
    except requests.exceptions.RequestException as e: 
        return f"[ERROR] Falha ao comunicar com Ollama: {e}"

# Envia requisições periódicas para manter o modelo carregado na memória
def manter_ativo(evento_parar):
    while not evento_parar.is_set():
        try:
            gerar("Responda apenas com: OK")
        except Exception:
            pass  

        for _ in range(120):
            if evento_parar.is_set():
                break
            time.sleep(1)

# Função para buscar a resposta do modelo com base na dúvida do usuário e no contexto técnico
def buscar_com_query_tecnica(pergunta_usuario, contexto_chromadb):
    prompt_sistema = f"""
Você é um especialista em redes MikroTik RouterOS. Sua tarefa é responder à dúvida do usuário utilizando APENAS as informações fornecidas no contexto abaixo. 
Filtre o contexto e use somente os comandos e opções que realmente resolvem o problema. Ignore informações irrelevantes.

--- CONTEXTO DO BANCO DE DADOS (MANUAIS DE EXPLICAÇÃO) ---
{contexto_chromadb}
---------------------------------------------------------

DÚVIDA DO USUÁRIO: {pergunta_usuario}

Instruções cruciais de resposta:
1. Seja altamente direto e objetivo, sem enrolações na introdução, mas entregue uma resposta técnica 100% COMPLETA com todos os parâmetros exigidos pelo RouterOS.
2. Mostre os comandos finais em LETRAS MAIÚSCULAS se baseando EXATAMENTE nos exemplos do contexto.
3. Garanta que todos os comandos gerados incluam os parâmetros estruturais obrigatórios da arquitetura do MikroTik (como cadeias de tráfego e ações), justificando brevemente a função de cada opção utilizada.
4. Organize as configurações propostas seguindo estritamente as boas práticas de ordenação lógica e precedência de regras de redes, explicando o impacto dessa estrutura no fluxo do tráfego.
"""

    return gerar(prompt_sistema)