# 🔍 Aplicação para Testar a API do Zabbix

Uma aplicação Python completa para aprender e testar as funcionalidades da **API do Zabbix**, com exemplos práticos de:

- ✅ Autenticação na API
- ✅ Criar hosts
- ✅ Criar items (métricas)
- ✅ Criar triggers (alertas)
- ✅ Listar recursos
- ✅ Gerenciar configurações

---

## 📋 Requisitos

### Sistema
- Python 3.7+
- Zabbix Server 4.0+ (instalado e rodando)
- Acesso à API do Zabbix

### Python
```bash
pip install pyzabbix requests
```

---

## 🚀 Instalação

### 1. Clonar ou Copiar o Repositório
```bash
cd seu-projeto-zabbix
git clone https://github.com/felipegoncalvesdasilva/Zabbix.git
cd Zabbix
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install pyzabbix requests
```

### 3. Configurar Conexão com Zabbix

Edite o arquivo `zabbix_api_tester.py` e ajuste as credenciais:

```python
# Linha ~270 - função exemplo_completo()
ZABBIX_URL = "http://localhost/zabbix"  # URL do seu Zabbix
ZABBIX_USER = "Admin"                    # Usuário (padrão)
ZABBIX_PASSWORD = "zabbix"               # Senha (alterar!)
```

---

## 💻 Como Usar

### Execução Básica
```bash
python3 zabbix_api_tester.py
```

### Saída Esperada
```
======================================================================
  TESTE COMPLETO DA API DO ZABBIX
======================================================================

📡 Conectando ao Zabbix: http://localhost/zabbix
✅ Conectado com sucesso!
   Versão da API: 6.0.0

📋 Listando hosts (limite: 5)...
✅ 2 host(s) encontrado(s):

   ID: 10001              | Zabbix Server                 | Ativo
   ID: 10049              | TestServer-001                | Ativo

... [mais operações] ...

✅ TESTE CONCLUÍDO COM SUCESSO!
======================================================================
```

---

## 🔧 Usar em Seu Próprio Código

### Exemplo 1: Criar Host
```python
from zabbix_api_tester import ZabbixTester

# Conectar
tester = ZabbixTester(
    url="http://localhost/zabbix",
    username="Admin",
    password="zabbix"
)

if tester.conectar():
    # Criar host
    host_id = tester.criar_host(
        hostname="MeuServidor",
        ip="192.168.1.50",
        description="Meu servidor de teste"
    )
```

### Exemplo 2: Criar Item
```python
if host_id:
    item_id = tester.criar_item(
        host_id=host_id,
        name="CPU Usage",
        key="system.cpu.load",
        value_type=0,  # numeric
        interval=60
    )
```

### Exemplo 3: Criar Trigger
```python
trigger_id = tester.criar_trigger(
    name="High CPU Alert",
    expression="{MeuServidor:system.cpu.load.last()}>3",
    severity=3,  # Average
    description="CPU acima de 3"
)
```

### Exemplo 4: Listar Recursos
```python
# Listar todos os hosts
hosts = tester.listar_hosts(limit=20)

# Listar items de um host
items = tester.listar_items(host_id="10001")

# Listar triggers
triggers = tester.listar_triggers(limit=15)
```

---

## 📚 Entendendo a API do Zabbix

### O que são Hosts?
**Hosts** são dispositivos ou servidores que você quer monitorar (servidores web, bancos de dados, roteadores, etc).

```python
host = tester.criar_host(
    hostname="Servidor Web 01",      # Nome único
    ip="192.168.1.10",              # IP para conexão
    description="Web server produção"
)
```

### O que são Items?
**Items** são as métricas que você quer coletar de um host (CPU, memória, disco, etc).

Tipos de valor:
- `0` = Numeric (inteiro)
- `1` = Character (string)
- `2` = Log (logs)
- `3` = Unsigned int (inteiro positivo)
- `4` = Float (decimal)

```python
item = tester.criar_item(
    host_id="10001",
    name="CPU Load",
    key="system.cpu.load",          # Chave pré-definida
    value_type=0,                    # Numérico
    interval=60                      # Coletar a cada 60s
)
```

### O que são Triggers?
**Triggers** são alertas que disparam quando uma condição é atendida.

Severidades:
- `0` = Not classified (não classificado)
- `1` = Info (informação)
- `2` = Warning (aviso)
- `3` = Average (médio)
- `4` = High (alto)
- `5` = Disaster (desastre)

```python
trigger = tester.criar_trigger(
    name="High Memory Usage",
    expression="{Servidor Web 01:vm.memory.size[pused].last()}>80",
    severity=4,                      # High
    description="Memória acima de 80%"
)
```

---

## 🔑 Expressões de Trigger

As expressões definem **quando** um trigger deve disparar:

### Operadores
- `.last()` - Último valor coletado
- `.avg()` - Média dos valores
- `.max()` - Valor máximo
- `.min()` - Valor mínimo
- `.count()` - Contagem de valores

### Exemplos

**CPU alta:**
```
{Servidor:system.cpu.load.last()}>4
```

**Memória baixa:**
```
{Servidor:vm.memory.size[pused].last()}>85
```

**Múltiplas condições:**
```
({Server1:cpu.last()}>80) and ({Server2:memory.last()}>80)
```

---

## 🔐 Segurança

### Boas Práticas
1. **Mude a senha padrão do Zabbix:**
   ```
   Padrão: Admin / zabbix
   ```

2. **Use variáveis de ambiente:**
   ```python
   import os
   
   ZABBIX_URL = os.getenv('ZABBIX_URL', 'http://localhost/zabbix')
   ZABBIX_USER = os.getenv('ZABBIX_USER', 'Admin')
   ZABBIX_PASSWORD = os.getenv('ZABBIX_PASSWORD', 'zabbix')
   ```

3. **Para produção, use SSL/TLS:**
   ```python
   tester = ZabbixTester(
       url="https://zabbix.empresa.com",
       username="zabbix_api",
       password="senha_forte",
       verify_ssl=True  # Ativar verificação SSL
   )
   ```

---

## 🆘 Troubleshooting

### Erro: "ConnectionError: Connection refused"
**Solução:** Certifique-se de que o Zabbix está rodando
```bash
# Verificar status do Zabbix
sudo systemctl status zabbix-server

# Iniciar Zabbix (se parado)
sudo systemctl start zabbix-server
```

### Erro: "Invalid authentication string"
**Solução:** Verifique as credenciais (usuário/senha)
```python
# Credenciais padrão
username = "Admin"  # Com A maiúsculo!
password = "zabbix"
```

### Erro: "Group does not exist"
**Solução:** O grupo não foi encontrado. Verificar grupos disponíveis:
```python
# Listar grupos
groups = tester.zabbix.hostgroup.get(output=['groupid', 'name'])
for group in groups:
    print(f"ID: {group['groupid']}, Nome: {group['name']}")
```

---

## 📖 Recursos Adicionais

- 📘 [Documentação Oficial do Zabbix](https://www.zabbix.com/documentation)
- 🔗 [API Reference do Zabbix](https://www.zabbix.com/documentation/current/en/api)
- 🐍 [pyzabbix GitHub](https://github.com/lukecyca/pyzabbix)
- 📺 [Tutoriais de Zabbix](https://www.zabbix.com/videos)

---

## 📝 Estrutura do Projeto

```
projeto-zabbix/
├── zabbix_api_tester.py      # Aplicação principal
├── README_ZABBIX.md           # Este arquivo
├── requirements.txt           # Dependências Python
├── examples/
│   ├── criar_host.py
│   ├── criar_item.py
│   └── criar_trigger.py
└── tests/
    └── test_api.py
```

---

## 🤝 Contribuir

Para melhorar esta aplicação:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcao`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova função'`)
4. Push para a branch (`git push origin feature/nova-funcao`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é de código aberto sob a licença MIT.

---

## 👤 Autor

**Felipe Gonçalves da Silva**

- GitHub: [@felipegoncalvesdasilva](https://github.com/felipegoncalvesdasilva)
- Email: felipe@example.com

---

## ✨ Dicas Importantes

1. **Comece simples:** Primeiro entenda como criar hosts, depois items, depois triggers
2. **Use a interface web:** Veja em tempo real o que está acontecendo
3. **Leia a documentação:** A API do Zabbix é muito completa
4. **Exporte seus testes:** Guarde os IDs dos recursos criados
5. **Teste em desenvolvimento:** Não use em produção sem testes

---

**Última atualização:** Agosto 2026

Divirta-se aprendendo Zabbix! 🚀
