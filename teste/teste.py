import re
import os

def separar_arquivos(nome_arquivo_origem):
    # Lê o conteúdo do arquivo original
    with open(nome_arquivo_origem, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Expressão regular para encontrar os blocos: 
    # Busca por "**Arquivo X: Título**" e captura o conteúdo até o próximo arquivo ou fim do texto
    padrao = r"\*\*Arquivo (\d+): (.*?)\*\*\n(.*?)(?=\n\*\*Arquivo \d+:|$)"
    blocos = re.findall(padrao, conteudo, re.DOTALL)

    for num, titulo, texto in blocos:
        # Formata o número com zero à esquerda (ex: 01, 02)
        num_formatado = num.zfill(2)
        
        # Define o nome do novo arquivo conforme o padrão solicitado
        nome_saida = f"Filtragem de Firewall - ({num_formatado} {titulo.strip()}).txt"
        
        # Limpa o texto (remove marcações de fonte como se desejar manter originalidade pura)
        texto_limpo = re.sub(r"\\s*", "", texto).strip()
        
        # Cria e escreve no novo arquivo .txt
        with open(nome_saida, 'w', encoding='utf-8') as f_out:
            f_out.write(texto_limpo)
        
        print(f"Arquivo criado: {nome_saida}")

# Executa a função
if __name__ == "__main__":
    # Certifique-se de que o arquivo "Filtragem de Firewall.txt" está na mesma pasta
    separar_arquivos('Filtragem de Firewall.txt')