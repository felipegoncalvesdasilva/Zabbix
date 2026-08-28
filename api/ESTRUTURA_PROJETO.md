# 📁 Estrutura Recomendada para Projeto Zabbix

Como organizar um projeto profissional com a API do Zabbix

---

## Estrutura Básica

```
meu-projeto-zabbix/
├── README.md                 # Documentação principal
├── .env.example              # Template de variáveis de ambiente
├── .env                      # Variáveis locais (não commitar!)
├── .gitignore               # Ignorar arquivos sensíveis
├── requirements.txt         # Dependências Python
│
├── zabbix_api_tester.py     # Classe principal da API
├── exemplo_uso_basico.py    # Exemplos práticos
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações da aplicação
│
├── src/
│   ├── __init__.py
│   ├── zabbix_client.py     # Cliente personalizado
│   ├── host_manager.py      # Gerenciar hosts
│   ├── item_manager.py      # Gerenciar items
│   └── trigger_manager.py   # Gerenciar triggers
│
├── scripts/
│   ├── create_test_env.py   # Script para criar ambiente de testes
│   ├── backup_hosts.py      # Script para fazer backup
│   └── sync_hosts.py        # Sincronizar configurações
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # Testes unitários
│   ├── test_hosts.py
│   └── test_integration.py  # Testes de integração
│
├── data/
│   ├── templates.json       # Templates de hosts
│   ├── hosts_config.json    # Configuração de hosts
│   └── triggers_config.json # Configuração de triggers
│
├── docs/
│   ├── API.md              # Documentação da API
│   ├── SETUP.md            # Como fazer setup
│   └── TROUBLESHOOTING.md  # Resolução de problemas
│
└── logs/
    ├── app.log             # Logs da aplicação
    └── errors.log          # Logs de erros
```

---

## Arquivo `config/settings.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações Zabbix
ZABBIX_URL = os.getenv('ZABBIX_URL', 'http://localhost/zabbix')
ZABBIX_USER = os.getenv('ZABBIX_USER', 'Admin')
ZABBIX_PASSWORD = os.getenv('ZABBIX_PASSWORD', 'zabbix')
ZABBIX_VERIFY_SSL = os.getenv('ZABBIX_VERIFY_SSL', 'False') == 'True'

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

# Configurações gerais
DEBUG = os.getenv('DEBUG', 'False') == 'True'
TIMEOUT = int(os.getenv('TIMEOUT', '30'))
```

---

## Arquivo `src/zabbix_client.py`

```python
from zabbix_api_tester import ZabbixTester
import logging

logger = logging.getLogger(__name__)

class ZabbixClient:
    """Cliente customizado para Zabbix com logging e cache"""
    
    def __init__(self, url, username, password, verify_ssl=False):
        self.tester = ZabbixTester(url, username, password, verify_ssl)
        self._cache = {}
    
    def conectar(self):
        """Conectar com logging"""
        try:
            if self.tester.conectar():
                logger.info("Conectado ao Zabbix com sucesso")
                return True
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            return False
    
    def criar_host_com_cache(self, hostname, ip, **kwargs):
        """Criar host e armazenar em cache"""
        # Verificar cache
        if hostname in self._cache:
            logger.info(f"Host {hostname} encontrado em cache")
            return self._cache[hostname]
        
        # Criar
        host_id = self.tester.criar_host(hostname, ip, **kwargs)
        
        # Armazenar em cache
        if host_id:
            self._cache[hostname] = host_id
            logger.info(f"Host {hostname} criado e cacheado: {host_id}")
        
        return host_id
    
    def limpar_cache(self):
        """Limpar cache de hosts"""
        self._cache.clear()
```

---

## Arquivo `src/host_manager.py`

```python
import logging

logger = logging.getLogger(__name__)

class HostManager:
    """Gerenciador de hosts"""
    
    def __init__(self, zabbix_client):
        self.client = zabbix_client
    
    def criar_host_produção(self, hostname, ip):
        """Criar host com configurações de produção"""
        return self.client.tester.criar_host(
            hostname=hostname,
            ip=ip,
            group_id=4,  # Servers
            description=f"Host {hostname} - Produção"
        )
    
    def criar_host_teste(self, hostname, ip):
        """Criar host com configurações de teste"""
        return self.client.tester.criar_host(
            hostname=hostname,
            ip=ip,
            group_id=4,
            description=f"Host {hostname} - Teste"
        )
    
    def criar_multiplos_hosts(self, hosts_data):
        """Criar múltiplos hosts de uma vez
        
        Args:
            hosts_data: Lista de dicts com {hostname, ip, environment}
        """
        criados = []
        
        for host in hosts_data:
            hostname = host['hostname']
            ip = host['ip']
            env = host.get('environment', 'production')
            
            if env == 'production':
                host_id = self.criar_host_produção(hostname, ip)
            else:
                host_id = self.criar_host_teste(hostname, ip)
            
            if host_id:
                criados.append({
                    'hostname': hostname,
                    'host_id': host_id
                })
            
            logger.info(f"Host {hostname} criado: {host_id}")
        
        return criados
```

---

## Arquivo `src/item_manager.py`

```python
import logging

logger = logging.getLogger(__name__)

class ItemManager:
    """Gerenciador de items/métricas"""
    
    # Templates de items comuns
    TEMPLATES = {
        'cpu': {
            'name': 'CPU Usage',
            'key': 'system.cpu.load',
            'value_type': 0,
            'interval': 60
        },
        'memory': {
            'name': 'Memory Usage',
            'key': 'vm.memory.size[pused]',
            'value_type': 0,
            'interval': 60
        },
        'disk': {
            'name': 'Disk Free',
            'key': 'vfs.fs.size[/,pfree]',
            'value_type': 0,
            'interval': 300
        },
        'uptime': {
            'name': 'System Uptime',
            'key': 'system.uptime',
            'value_type': 0,
            'interval': 600
        }
    }
    
    def __init__(self, zabbix_client):
        self.client = zabbix_client
    
    def criar_item_template(self, host_id, template_name):
        """Criar item usando template"""
        if template_name not in self.TEMPLATES:
            logger.error(f"Template '{template_name}' não existe")
            return None
        
        template = self.TEMPLATES[template_name]
        
        return self.client.tester.criar_item(
            host_id=host_id,
            name=template['name'],
            key=template['key'],
            value_type=template['value_type'],
            interval=template['interval']
        )
    
    def criar_items_padrao(self, host_id):
        """Criar conjunto padrão de items"""
        padrao = ['cpu', 'memory', 'disk', 'uptime']
        criados = []
        
        for template_name in padrao:
            item_id = self.criar_item_template(host_id, template_name)
            if item_id:
                criados.append(template_name)
                logger.info(f"Item '{template_name}' criado para host {host_id}")
        
        return criados
```

---

## Arquivo `scripts/create_test_env.py`

```python
#!/usr/bin/env python3
"""Script para criar ambiente de testes no Zabbix"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import *
from src.zabbix_client import ZabbixClient
from src.host_manager import HostManager
from src.item_manager import ItemManager

def main():
    print("🚀 Criando ambiente de testes no Zabbix...")
    
    # Conectar
    client = ZabbixClient(ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD, ZABBIX_VERIFY_SSL)
    
    if not client.conectar():
        print("❌ Falha ao conectar!")
        return 1
    
    # Criar hosts de teste
    hosts_config = [
        {'hostname': 'TestWeb01', 'ip': '192.168.1.10', 'environment': 'test'},
        {'hostname': 'TestWeb02', 'ip': '192.168.1.11', 'environment': 'test'},
        {'hostname': 'TestDB01', 'ip': '192.168.1.20', 'environment': 'test'},
    ]
    
    host_manager = HostManager(client)
    criados = host_manager.criar_multiplos_hosts(hosts_config)
    
    print(f"\n✅ {len(criados)} host(s) criado(s)")
    
    # Criar items
    item_manager = ItemManager(client)
    
    for host_info in criados:
        print(f"\n📊 Criando items para {host_info['hostname']}...")
        items = item_manager.criar_items_padrao(host_info['host_id'])
        print(f"   ✅ {len(items)} item(ns) criado(s): {', '.join(items)}")
    
    print("\n✅ Ambiente de testes criado com sucesso!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

---

## Arquivo `tests/test_api.py`

```python
import unittest
from src.zabbix_client import ZabbixClient
from config.settings import ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD

class TestZabbixAPI(unittest.TestCase):
    
    def setUp(self):
        """Preparar testes"""
        self.client = ZabbixClient(ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD)
    
    def test_conectar(self):
        """Testar conexão"""
        self.assertTrue(self.client.conectar())
    
    def test_criar_host(self):
        """Testar criação de host"""
        host_id = self.client.tester.criar_host(
            "TestHost",
            "192.168.1.50"
        )
        self.assertIsNotNone(host_id)
    
    def test_listar_hosts(self):
        """Testar listagem de hosts"""
        hosts = self.client.tester.listar_hosts(limit=10)
        self.assertIsInstance(hosts, list)

if __name__ == '__main__':
    unittest.main()
```

---

## Arquivo `data/hosts_config.json`

```json
{
  "hosts": [
    {
      "hostname": "WebServer01",
      "ip": "192.168.1.10",
      "environment": "production",
      "group": "Servers",
      "description": "Web server principal",
      "items": ["cpu", "memory", "disk", "uptime"]
    },
    {
      "hostname": "DatabaseServer01",
      "ip": "192.168.1.20",
      "environment": "production",
      "group": "Servers",
      "description": "Servidor de banco de dados",
      "items": ["cpu", "memory"]
    }
  ]
}
```

---

## Arquivo `.gitignore`

```
# Variáveis de ambiente
.env
.env.local
.env.*.local

# Arquivos de log
*.log
logs/

# Cache Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Dados sensíveis
data/secrets.json
credentials.json

# OS
.DS_Store
Thumbs.db

# Testes
.pytest_cache/
htmlcov/

# Zabbix backups
backups/
*.bak
```

---

## Como Usar Esta Estrutura

### 1. Criar Estrutura
```bash
mkdir -p meu-projeto-zabbix/{config,src,scripts,tests,data,docs,logs}
cd meu-projeto-zabbix
```

### 2. Copiar Arquivos
```bash
cp zabbix_api_tester.py ./
cp exemplo_uso_basico.py ./
cp requirements.txt ./
cp .env.example ./
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar
```bash
cp .env.example .env
# Editar .env com suas credenciais
```

### 5. Rodar Testes
```bash
python3 -m pytest tests/
```

### 6. Executar Scripts
```bash
python3 scripts/create_test_env.py
```

---

## Próximas Melhorias

- 📊 Adicionar dashboard web
- 📈 Implementar histórico de alterações
- 🔔 Notificações via Slack/Email
- 📝 Geração de relatórios
- 🔐 Autenticação OAuth2
- 🚀 Deploy com Docker

---

**Última atualização:** Agosto 2026
