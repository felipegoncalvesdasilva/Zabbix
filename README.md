# Criação de Servidor Zabbix via Bash

Script em Bash que cria rapidamente um ambiente **Zabbix** no **Ubuntu**. Você escolhe a versão do Ubuntu e a versão do Zabbix em um menu interativo, e o script cuida de toda a instalação e configuração (Zabbix Server, Frontend, Agent, Apache e MySQL).

Pensado para **ambientes de teste, laboratório e estudo**.

<img width="1337" height="661" alt="image" src="https://github.com/user-attachments/assets/13b9a785-7b6a-4d72-99c3-9248f864cfc1" />

## Sumário

- [Versões suportadas](#versões-suportadas)
- [O que o script faz](#o-que-o-script-faz)
- [Requisitos](#requisitos)
- [Como usar](#como-usar)
- [Acessando o Zabbix](#acessando-o-zabbix)
- [Observações importantes](#observações-importantes)
- [Solução de problemas](#solução-de-problemas)
- [Contribuindo](#contribuindo)

---

## Versões suportadas

| Ubuntu | Zabbix |
|--------|--------|
| 26.04 | 8.0 |
| 24.04 | 7.4 |
| 22.04 | 7.0 |
| 20.04 | 6.0 |

Você pode combinar qualquer versão do Ubuntu com qualquer versão do Zabbix pelo menu. Porém, **nem toda combinação existe no repositório oficial do Zabbix**. Quando o pacote não for encontrado, o script exibe um erro de download e encerra.

## O que o script faz

1. Verifica se está sendo executado como **root**
2. Detecta se o Zabbix Server já está instalado e pede confirmação antes de continuar
3. Detecta a versão do Ubuntu do sistema e avisa se ela for diferente da escolhida
4. Exibe os menus para escolha da versão do **Ubuntu** e do **Zabbix**
5. Monta a URL do repositório oficial e instala o pacote `zabbix-release`
6. Instala `zabbix-server-mysql`, `zabbix-frontend-php`, `zabbix-apache-conf`, `zabbix-sql-scripts` e `zabbix-agent`
7. Instala e habilita o **MySQL Server**
8. Solicita as senhas (root do MySQL e banco do Zabbix) e o nome do servidor
9. Aplica uma configuração básica de segurança no MySQL
10. Cria o banco `zabbix` (utf8mb4) e o usuário `zabbix`, e importa o schema inicial
11. Ajusta o `zabbix_server.conf`, o `Hostname` do agente e o fuso horário do PHP (`America/Sao_Paulo`)
12. Reinicia e habilita os serviços `zabbix-server`, `zabbix-agent` e `apache2`

## Requisitos

| Item | Detalhe |
|------|---------|
| Sistema operacional | Ubuntu 20.04, 22.04, 24.04 ou 26.04 |
| Acesso | Usuário `root` ou `sudo` |
| Rede | Acesso à internet (repositório do Zabbix e pacotes) |
| Recursos | Mínimo recomendado: 2 GB de RAM e 20 GB de disco |

## Como usar

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/Zabbix.git
cd Zabbix
```

Dê permissão de execução e rode como root:

```bash
chmod +x install_zabbix.sh
sudo ./install_zabbix.sh
```

Durante a execução, você vai:

1. Escolher a versão do **Ubuntu**
2. Escolher a versão do **Zabbix**
3. Informar a **senha do root do MySQL**
4. Informar a **senha do banco de dados do Zabbix**
5. Informar o **nome do servidor** (ex.: `zabbix.empresa.com`)

> As senhas são digitadas de forma oculta e não ficam gravadas no script.
