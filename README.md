# AutoMikro

O AutoMikro é um assistente técnico de IA baseado em LLM e RAG estruturado para apoiar a detecção de conflitos e tradução de intenções em comandos CLI para políticas de filtragem de tráfego no firewall do MikroTik RouterOS.
(Ainda em Execução)
---

## 🛠️ Ferramentas Utilizadas

| Ferramenta | Função no Projeto |
| :--- | :--- |
| **Python 3.10+** |  Linguagem base utilizada para estruturar a lógica do sistema |
| **Docker Desktop** | Plataforma de containerização que roda o ecossistema Ollama isolado no Windows. |
| **Ollama** | Motor local responsável pela execução e gerenciamento de LLMs. |
| **Qwen3:4b-instruct** | Modelo de IA especializado em seguir instruções e gerar os comandos técnicos. |
| **ChromaDB** | Banco de dados vetorial local utilizado para armazenar os manuais técnicos. |
| **LlamaIndex** | Framework de orquestração que conecta os manuais do ChromaDB ao Ollama (RAG). |
| **BAAI/bge-m3** | Modelo de embedding que converte os textos dos manuais em vetores matemáticos. |

---

## 📂 Estrutura do Projeto

```text
AutoMikro/
│
├── ChromaDB/
│   ├── ingestao.py           # Modulo que lê os manuais e alimenta o banco
│   └── busca.py              # Modulo de varredura e busca vetorial
│
├── Containers/
│   └── compose.yaml          # Configuração do container Docker (Ollama)
│
├── LLM/
│   └── ollama.py             # Modulo de integração com a API do Ollama e prompt do sistema
│
├── documentos_txt/           # Pasta com documentos RouterOS organizados em formato .txt
│
├── banco_vetorial/           # Banco local com os manuais indexados em vetores
│
├── main.py                   # Arquivo principal (Interface do Menu)
│
└── instalar_dependencias.ps1 # Script de instalação automatizada
```
## Passo a Passo para Execução

Siga a ordem dos blocos abaixo no seu terminal para preparar o ambiente e rodar o projeto:

### 1. Subir o Servidor Ollama no Docker
Certifique-se de que o Docker Desktop está aberto e execute o comando abaixo na pasta do arquivo `compose.yaml`:
```bash
docker compose up -d
```

### 2. Baixar o Modelo de IA para o Container
Com o container ativo, faça o download do modelo Qwen para dentro do ecossistema isolado:
```bash
docker exec -it ollama ollama run qwen3:4b-instruct
```

### 3. Instalar as Dependências do Python
Execute o script do PowerShell para automatizar a instalação de todas as bibliotecas necessárias:
```bash
./instalar_dependencias.ps1
```
### 4. Instalar as Dependências do Python
Após concluir as etapas anteriores, inicialize a aplicação e abra o menu principal do AutoMikro:
```bash
python main.py
```
