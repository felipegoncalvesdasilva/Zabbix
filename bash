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

# Versão ubuntu atual do sistema
if command -v lsb_release >/dev/null 2>&1; then
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
echo -e "${YELLOW}$url_final${NC}\n"
cd /tmp
wget $url_final
dpkg -i zabbix-release*
apt update -y
apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent -y

# Instalar MySQL Server
log "Instalando MySQL Server 8.0..."
apt install -y mysql-server mysql-client

# Configurar MySQL
log "Configurando MySQL..."
systemctl start mysql
systemctl enable mysql

######## AQUI
# Solicitar informações
echo
info "Configuração inicial:"
echo -n "Digite a senha para o usuário root do MySQL: "
read -s DB_PASSWORD
echo

echo -n "Digite a senha para o banco de dados do Zabbix: "
read -s ZABBIX_DB_PASSWORD
echo

echo -n "Digite o nome do servidor (ex: zabbix.empresa.com): "
read -r SERVER_NAME

# Configuração segura do MySQL
log "Configurando segurança do MySQL..."
mysql -uroot -e  "ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
mysql -e "DELETE FROM mysql.user WHERE User='';"
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
mysql -e "FLUSH PRIVILEGES;"

# Criando Database 
mysql -e "create database zabbix character set utf8mb4 collate utf8mb4_bin;"
mysql -e "create user zabbix@localhost identified by '${ZABBIX_DB_PASSWORD}';"
mysql -e "grant all privileges on zabbix.* to zabbix@localhost;"
mysql -e "set global log_bin_trust_function_creators = 1;"
mysql -uzabbix -p"${ZABBIX_DB_PASSWORD}" --default-character-set=utf8mb4 zabbix < <(zcat /usr/share/zabbix/sql-scripts/mysql/server.sql.gz)
#zcat /usr/share/zabbix/sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p f1a2a3a4g5
mysql -e "set global log_bin_trust_function_creators = 0;"

# Configurar zabbix_server.conf
ZBX_CONF="/etc/zabbix/zabbix_server.conf"
sed -i "s|^# DBPassword=.*$|DBPassword=${ZABBIX_DB_PASSWORD}|" "$ZBX_CONF"
sed -i "s|^# DBName=zabbix$|DBName=zabbix|" "$ZBX_CONF"
sed -i "s|^# DBUser=.*$|DBUser=zabbix|" "$ZBX_CONF"

# Ajustar timezone do PHP para Zabbix UI
PHP_CONF="/etc/zabbix/apache.conf"
if ! grep -q "date.timezone" "$PHP_CONF"; then
  echo 'php_value date.timezone America/Sao_Paulo' >> "$PHP_CONF"
fi

# Restart e enable zabbix
systemctl restart zabbix-server zabbix-agent apache2
systemctl enable zabbix-server zabbix-agent apache2
