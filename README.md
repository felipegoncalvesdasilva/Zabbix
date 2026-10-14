# Criação de Servidor Zabbix via Bash

Script em Bash para instalar e configurar de forma automatizada um servidor **Zabbix ** (Server + Frontend + Agent), com banco de dados e servidor web, sem a necessidade de executar cada passo manualmente.

<img width="1337" height="661" alt="image" src="https://github.com/user-attachments/assets/13b9a785-7b6a-4d72-99c3-9248f864cfc1" />


---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [O que o script faz](#o-que-o-script-faz)
- [Requisitos](#requisitos)

---

## Sobre o projeto

O [Zabbix](https://www.zabbix.com/) é uma plataforma open source de monitoramento de redes, servidores, aplicações e serviços. A instalação manual envolve vários passos (repositório, pacotes, banco de dados, importação do schema, configuração do servidor e do frontend). Este projeto reúne todos eles em um script Bash para acelerar e padronizar o processo.

## O que o script faz

1. Atualiza o sistema operacional
2. Adiciona o repositório oficial do Zabbix
3. Instala o Zabbix Server, Frontend, Agent e dependências
4. Instala e configura o banco de dados
5. Cria o banco e o usuário do Zabbix
6. Importa o schema inicial
7. Ajusta os arquivos de configuração (`zabbix_server.conf`, PHP/Apache ou Nginx)
8. Habilita e inicia os serviços

## Requisitos

| Item | Recomendado |
|------|-------------|
| Sistema operacional | Ubuntu (ajuste conforme a sua distribuição) |
| Acesso | Usuário `root` ou com `sudo` |
| Memória RAM | 2 GB ou mais |
| Disco | 20 GB ou mais |
| Rede | Acesso à internet para baixar os pacotes |
