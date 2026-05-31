# AutoMikro

## Ferramentas

### Containerlab

* **O que é?** Uma ferramenta leve que cria laboratórios de redes usando contêineres.
* **Como funciona?** Ele monta toda a sua rede automaticamente através de um "mapa" escrito em um arquivo YAML.
* **Do que preciso?** Privilégios de administrador (sudo), Docker instalado e servidor/VM Linux.
* **Como instalar?** `curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"`

#### Guia de Aplicação

**1. Como criar a rede? (.clab.yml)**

* **Name:** Nome do laboratório (sem espaços).
* **Nodes:** Os aparelhos da rede (roteadores, switches ou servidores).
* **Kind:** O "modelo" do aparelho (ex: `mikrotik_routeros`).
* **Image:** A versão do sistema que será instalada no aparelho.
* **Links:** A lista de quais portas estão ligadas entre si (os cabos virtuais).

**2. Como rodar e gerenciar?**

* **Para ligar tudo:** `sudo containerlab deploy -t [nome-do-arquivo].clab.yml`
* **Para entrar no roteador:** Use o comando **SSH** ou o terminal do **Docker**.
* **Para desligar tudo:** `sudo containerlab destroy -t [nome-do-arquivo].clab.yml`

---
