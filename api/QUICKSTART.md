# 🚀 Guia Rápido - Zabbix API Tester

Comece em 5 minutos!

---

## 1️⃣ Instalação (2 minutos)

```bash
# Instalar dependências
pip install -r requirements.txt
```

---

## 2️⃣ Configuração (1 minuto)

Edite `zabbix_api_tester.py` na linha ~270:

```python
ZABBIX_URL = "http://localhost/zabbix"  # Sua URL do Zabbix
ZABBIX_USER = "Admin"                    # Seu usuário
ZABBIX_PASSWORD = "zabbix"               # Sua senha
```

---

## 3️⃣ Executar (1 minuto)

### Opção A: Teste Completo
```bash
python3 zabbix_api_tester.py
```

### Opção B: Exemplos Interativos
```bash
python3 exemplo_uso_basico.py
```

---

## 4️⃣ Ver Resultados no Zabbix

1. Abra: `http://localhost/zabbix`
2. Vá para: **Configuration → Hosts**
3. Procure por: `TestServer-001` (ou o host que criou)
4. Clique para ver **Items** e **Triggers**

---

## 📚 Estrutura dos Arquivos

| Arquivo | O que faz |
|---------|-----------|
| `zabbix_api_tester.py` | Classe principal com todas as funções |
| `exemplo_uso_basico.py` | 8 exemplos práticos prontos para copiar |
| `README_ZABBIX.md` | Documentação completa |
| `requirements.txt` | Dependências Python |

---

## 💡 Primeiros Passos Recomendados

### Passo 1: Entender os Conceitos
```
Host (Servidor) ─→ Item (Métrica) ─→ Trigger (Alerta)
```

### Passo 2: Criar seu Primeiro Host
```python
from zabbix_api_tester import ZabbixTester

tester = ZabbixTester("http://localhost/zabbix", "Admin", "zabbix")
tester.conectar()

host_id = tester.criar_host(
    hostname="MeuPrimeiroServidor",
    ip="192.168.1.100"
)
```

### Passo 3: Adicionar uma Métrica
```python
item_id = tester.criar_item(
    host_id=host_id,
    name="CPU Usage",
    key="system.cpu.load"
)
```

### Passo 4: Criar um Alerta
```python
trigger_id = tester.criar_trigger(
    name="CPU Alto",
    expression="last(/MeuPrimeiroServidor/system.cpu.load)>3",
    severity=3
)
```

---

## 🎯 Casos de Uso Comuns

### ✅ Criar múltiplos servidores de uma vez

```python
servidores = [
    ("WebServer01", "192.168.1.10"),
    ("WebServer02", "192.168.1.11"),
    ("WebServer03", "192.168.1.12"),
]

for hostname, ip in servidores:
    host_id = tester.criar_host(hostname, ip)
    # ... criar items e triggers
```

### ✅ Monitorar aplicação

```python
app_server = tester.criar_host("AppServer", "192.168.1.50")

metricas = [
    ("Memory", "vm.memory.size[pused]"),
    ("Disk Free", "vfs.fs.size[/,pfree]"),
    ("Processes", "proc.num[]"),
]

for name, key in metricas:
    tester.criar_item(app_server, name, key)
```

### ✅ Alertas em cascata

```python
# Aviso
tester.criar_trigger(
    name="CPU Warning",
    expression="last(/Server/cpu)>50",
    severity=2  # Warning
)

# Crítico
tester.criar_trigger(
    name="CPU Critical",
    expression="last(/Server/cpu)>80",
    severity=4  # High
)
```

---

## 🔥 Problemas Comuns e Soluções

### ❌ "Connection refused"
```
Solução: Certifique-se de que o Zabbix está rodando
sudo systemctl status zabbix-server
sudo systemctl start zabbix-server
```

### ❌ "Invalid authentication"
```
Solução: Verifique as credenciais
Padrão: Admin / zabbix (com A maiúsculo!)
```

### ❌ "Host already exists"
```
Solução: Use outro nome ou liste hosts existentes
hosts = tester.listar_hosts(limit=100)
```

### ❌ "Key does not exist"
```
Solução: Use chaves válidas do Zabbix
Exemplos válidos:
- system.uptime
- system.cpu.load
- vm.memory.size[pused]
- vfs.fs.size[/,free]
```

---

## 📖 Documentação Rápida

### Classes e Métodos

```python
from zabbix_api_tester import ZabbixTester

tester = ZabbixTester(url, user, password)

# Conectar/Desconectar
tester.conectar()           # Conectar ao Zabbix
tester.desconectar()        # Desconectar

# Criar Recursos
tester.criar_host()         # Criar host
tester.criar_item()         # Criar item/métrica
tester.criar_trigger()      # Criar trigger/alerta

# Listar Recursos
tester.listar_hosts()       # Listar todos os hosts
tester.listar_items(host_id) # Listar items de um host
tester.listar_triggers()    # Listar todos os triggers

# Auxiliar
tester.obter_grupo_id()     # Obter ID de um grupo
```

---

## 🎓 O Que Você Vai Aprender

✅ Como autenticar na API do Zabbix
✅ Criar hosts e gerenciá-los
✅ Adicionar métricas (items)
✅ Configurar alertas (triggers)
✅ Usar expressões de trigger
✅ Listar e filtrar recursos
✅ Tratamento de erros
✅ Boas práticas de segurança

---

## 📞 Precisa de Ajuda?

1. **Leia o README completo**: `README_ZABBIX.md`
2. **Veja os exemplos**: `exemplo_uso_basico.py`
3. **Consulte a documentação oficial**: https://www.zabbix.com/documentation
4. **Verifique a API reference**: https://www.zabbix.com/documentation/current/en/api

---

## 🎉 Próximos Passos

Após aprender o básico:

1. **Explore os 8 exemplos** em `exemplo_uso_basico.py`
2. **Crie um script personalizado** para seu caso de uso
3. **Integre com sua aplicação** Python
4. **Configure alertas reais** (email, Slack, etc)
5. **Automatize testes** com CI/CD

---

**Boa sorte e divirta-se aprendendo Zabbix! 🚀**

---

**Última atualização:** Agosto 2026
