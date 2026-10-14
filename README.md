Criação de Servidor Zabbix via Bash

Script em Bash para instalar e configurar de forma automatizada um servidor Zabbix 7.4 (Server + Frontend + Agent), com banco de dados e servidor web, sem a necessidade de executar cada passo manualmente.

Sumário
Sobre o projeto
O que o script faz
Requisitos
Como usar
Acessando o Zabbix
Estrutura do repositório
Solução de problemas
Contribuindo
Licença
Sobre o projeto

O Zabbix é uma plataforma open source de monitoramento de redes, servidores, aplicações e serviços. A instalação manual envolve vários passos (repositório, pacotes, banco de dados, importação do schema, configuração do servidor e do frontend). Este projeto reúne todos eles em um script Bash para acelerar e padronizar o processo.

O que o script faz
Atualiza o sistema operacional
Adiciona o repositório oficial do Zabbix
Instala o Zabbix Server, Frontend, Agent e dependências
Instala e configura o banco de dados
Cria o banco e o usuário do Zabbix
Importa o schema inicial
Ajusta os arquivos de configuração (zabbix_server.conf, PHP/Apache ou Nginx)
Habilita e inicia os serviços
Requisitos
Item	Recomendado
Sistema operacional	Debian / Ubuntu (ajuste conforme a sua distribuição)
Acesso	Usuário root ou com sudo
Memória RAM	2 GB ou mais
Disco	20 GB ou mais
Rede	Acesso à internet para baixar os pacotes



<img width="1345" height="662" alt="image" src="https://github.com/user-attachments/assets/9abb3afd-b961-4afc-aee9-d5c54fe6f1d4" />
