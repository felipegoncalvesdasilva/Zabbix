#!/bin/bash

# Script de Instalação do Zabbix Server
# Ubuntu 20 - 26

# Configurações
DB_PASSWORD=""
ZABBIX_DB_PASSWORD=""
SERVER_NAME=""

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================================================
# FUNÇÕES
# ==================================================

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Lê uma senha do usuário, repetindo até que não esteja vazia
ler_senha() {
    local prompt="$1"
    local __resultvar="$2"
    local senha=""
    while [[ -z "$senha" ]]; do
        echo -n "$prompt"
        read -s senha
        echo
        if [[ -z "$senha" ]]; then
            warning "A senha não pode ficar em branco. Tente novamente."
        fi
    done
    printf -v "$__resultvar" '%s' "$senha"
}

gerar_url_zabbix() {
    local zabbix_ver="$1"
    local ubuntu_ver="$2"
    local url_final=""

    # 1. Compara se a versão é MENOR que 7.1
    # Se o menor valor entre a versão digitada e 7.1 for a própria versão, entra no bloco.
    if [[ "$(echo -e "${zabbix_ver}\n7.1" | sort -V | head -n1)" == "$zabbix_ver" && "$zabbix_ver" != "7.1" ]]; then

        # Estrutura antiga: Para versões como 5.0, 6.0, 7.0...
        url_final="https://repo.zabbix.com/zabbix/${zabbix_ver}/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_${zabbix_ver}+ubuntu${ubuntu_ver}_all.deb"

    else

        # Estrutura nova: Para versões 7.1, 7.4, 8.0... (repare a palavra '/release/' na URL)
        url_final="https://repo.zabbix.com/zabbix/${zabbix_ver}/release/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_${zabbix_ver}+ubuntu${ubuntu_ver}_all.deb"

    fi

    echo "$url_final"
}

# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================

# Banner (Corrigido: Aspas fechadas)
echo -e "${BLUE}"
echo "=================================================="
echo "         INSTALADOR ZABBIX - UBUNTU"
echo "=================================================="
echo -e "${NC}"

# Verificar se é executado como root
if [[ $EUID -ne 0 ]]; then
   error "Este script deve ser executado como root (sudo)"
fi

# Verificar se o Zabbix já está instalado (evita reinstalação acidental)
if systemctl list-unit-files 2>/dev/null | grep -q '^zabbix-server'; then
    warning "Parece que o Zabbix Server já está instalado neste sistema."
    read -p "Deseja continuar mesmo assim? [s/N]: " continuar
    if [[ ! "$continuar" =~ ^[sS]$ ]]; then
        echo "Instalação cancelada."
        exit 0
    fi
fi

# Versão ubuntu atual do sistema
sistema_ver=""
if command -v lsb_release >/dev/null 2>&1; then
  sistema_ver="$(lsb_release -sr)"
  info "Sua versão atual do sistema é: $(lsb_release -sd)"
else
  warning "Não foi encontrada a versão atual do Ubuntu via lsb_release."
fi

# Menu Ubuntu (Corrigido: Adicionado 'break' e 'done')
while true; do
  echo "--------------------------------------------------"
  echo "Escolha a versão do Ubuntu para o repositório:"
  echo " 1: Ubuntu 26.04"
  echo " 2: Ubuntu 24.04"
  echo " 3: Ubuntu 22.04"
  echo " 4: Ubuntu 20.04"
  echo " 5: Sair"
  echo "--------------------------------------------------"
  read -sn1 -p "Opção [1-5]: " escolha
  echo
  case "$escolha" in
    1) ubuntu_ver="26.04" ; break ;;
    2) ubuntu_ver="24.04" ; break ;;
    3) ubuntu_ver="22.04" ; break ;;
    4) ubuntu_ver="20.04" ; break ;;
    5) echo "Saindo..."; exit 0 ;;
    *) echo "Opção inválida: $escolha"; sleep 1; clear; continue ;;
  esac
done
log "Você escolheu Ubuntu $ubuntu_ver"

# Avisa se a versão escolhida não bate com a detectada no sistema
if [[ -n "$sistema_ver" && "$sistema_ver" != "$ubuntu_ver" ]]; then
    warning "Você escolheu Ubuntu ${ubuntu_ver}, mas o sistema roda ${sistema_ver}."
    read -p "Deseja continuar mesmo assim? [s/N]: " continuar
    if [[ ! "$continuar" =~ ^[sS]$ ]]; then
        echo "Instalação cancelada."
        exit 0
    fi
fi
sleep 1
clear

# Menu Zabbix (Corrigido: Texto ajustado, adicionado 'break' e 'done')
while true; do
  echo "--------------------------------------------------"
  echo "Escolha a versão do Zabbix:"
  echo " 1: Zabbix 8.0"
  echo " 2: Zabbix 7.4"
  echo " 3: Zabbix 7.0"
  echo " 4: Zabbix 6.0"
  echo " 5: Sair"
  echo "--------------------------------------------------"
  read -sn1 -p "Opção [1-5]: " escolha
  echo
  case "$escolha" in
    1) zabbix_ver="8.0" ; break ;;
    2) zabbix_ver="7.4" ; break ;;
    3) zabbix_ver="7.0" ; break ;;
    4) zabbix_ver="6.0" ; break ;;
    5) echo "Saindo..."; exit 0 ;;
    *) echo "Opção inválida: $escolha"; sleep 1; clear; continue ;;
  esac
done
log "Você escolheu Zabbix $zabbix_ver"
sleep 1
clear

# --- TESTANDO RECURSO OU PROSSEGUINDO ---

echo "=== Resultado da sua seleção ==="
url_final=$(gerar_url_zabbix "$zabbix_ver" "$ubuntu_ver")
info "URL gerada para download:"
echo -e "${YELLOW}${url_final}${NC}\n"

cd /tmp
log "Baixando pacote de repositório do Zabbix..."
wget -q "$url_final" -O zabbix-release_latest.deb || error "Falha ao baixar $url_final"

log "Instalando pacote de repositório..."
dpkg -i zabbix-release_latest.deb || { warning "Corrigindo dependências..."; apt-get install -f -y; }

apt update -y
apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent

# Instalar MySQL Server
log "Instalando MySQL Server 8.0..."
apt install -y mysql-server mysql-client

# Configurar MySQL
log "Configurando MySQL..."
systemctl start mysql
systemctl enable mysql

# Solicitar informações
echo
info "Configuração inicial:"
ler_senha "Digite a senha para o usuário root do MySQL: " DB_PASSWORD
ler_senha "Digite a senha para o banco de dados do Zabbix: " ZABBIX_DB_PASSWORD

echo -n "Digite o nome do servidor (ex: zabbix.empresa.com): "
read -r SERVER_NAME

# Configuração segura do MySQL
# A partir daqui o root passa a exigir senha (ALTER USER troca o método de
# autenticação de auth_socket para senha), então todos os comandos seguintes
# precisam informar usuário e senha explicitamente.
log "Configurando segurança do MySQL..."
mysql -uroot -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"

export MYSQL_PWD="${DB_PASSWORD}"
mysql -uroot -e "DELETE FROM mysql.user WHERE User='';"
mysql -uroot -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -uroot -e "DROP DATABASE IF EXISTS test;"
mysql -uroot -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
mysql -uroot -e "FLUSH PRIVILEGES;"

# Criando Database
log "Criando banco de dados do Zabbix..."
mysql -uroot -e "CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"
mysql -uroot -e "CREATE USER zabbix@localhost IDENTIFIED BY '${ZABBIX_DB_PASSWORD}';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON zabbix.* TO zabbix@localhost;"
mysql -uroot -e "SET GLOBAL log_bin_trust_function_creators = 1;"

log "Importando schema inicial do Zabbix (isso pode demorar alguns minutos)..."
MYSQL_PWD="${ZABBIX_DB_PASSWORD}" mysql -uzabbix --default-character-set=utf8mb4 zabbix < <(zcat /usr/share/zabbix/sql-scripts/mysql/server.sql.gz)

mysql -uroot -e "SET GLOBAL log_bin_trust_function_creators = 0;"
unset MYSQL_PWD

# Configurar zabbix_server.conf
ZBX_CONF="/etc/zabbix/zabbix_server.conf"
sed -i "s|^# DBPassword=.*$|DBPassword=${ZABBIX_DB_PASSWORD}|" "$ZBX_CONF"
sed -i "s|^# DBName=zabbix$|DBName=zabbix|" "$ZBX_CONF"
sed -i "s|^# DBUser=.*$|DBUser=zabbix|" "$ZBX_CONF"

# Define o Hostname do agente com base no nome informado (se houver)
ZBX_AGENT_CONF="/etc/zabbix/zabbix_agentd.conf"
if [[ -n "$SERVER_NAME" && -f "$ZBX_AGENT_CONF" ]]; then
    sed -i "s|^Hostname=.*$|Hostname=${SERVER_NAME}|" "$ZBX_AGENT_CONF"
fi

# Ajustar timezone do PHP para Zabbix UI
PHP_CONF="/etc/zabbix/apache.conf"
if ! grep -q "date.timezone" "$PHP_CONF"; then
  echo 'php_value date.timezone America/Sao_Paulo' >> "$PHP_CONF"
fi

# Restart e enable zabbix
log "Reiniciando serviços..."
systemctl restart zabbix-server zabbix-agent apache2
systemctl enable zabbix-server zabbix-agent apache2

echo
log "Instalação concluída!"
info "Acesse a interface web em: http://<IP-do-servidor>/zabbix"
warning "Login padrão: Admin / zabbix — troque essa senha assim que possível."
