#!/usr/bin/env python3
"""
Aplicação para Testar a API do Zabbix
======================================

Esta aplicação demonstra como usar a API do Zabbix para:
- Autenticar na API
- Criar hosts
- Criar items (métricas)
- Criar triggers (alertas)
- Listar e gerenciar recursos

Requisitos:
    pip install pyzabbix requests

Uso:
    python3 zabbix_api_tester.py

Autor: Felipe Gonçalves
Data: 2026
"""

import json
import sys
from typing import Dict, List, Any, Optional
from pyzabbix import ZabbixAPI
import requests
from datetime import datetime

# Desabilitar aviso de SSL para testes
requests.packages.urllib3.disable_warnings()


class ZabbixTester:
    """Classe para testar funcionalidades da API do Zabbix"""
    
    def __init__(self, url: str, username: str, password: str, verify_ssl: bool = False):
        """
        Inicializar conexão com Zabbix
        
        Args:
            url: URL do Zabbix (ex: http://localhost/zabbix ou https://zabbix.example.com)
            username: Usuário para autenticação
            password: Senha para autenticação
            verify_ssl: Verificar certificado SSL (padrão: False)
        """
        self.url = url
        self.username = username
        self.password = password
        self.zabbix = None
        self.verify_ssl = verify_ssl
        
    def conectar(self) -> bool:
        """
        Conectar e autenticar na API do Zabbix
        
        Returns:
            bool: True se conectado com sucesso
        """
        try:
            print(f"\n📡 Conectando ao Zabbix: {self.url}")
            
            self.zabbix = ZabbixAPI(
                self.url,
                user=self.username,
                password=self.password,
                ssl_verify=self.verify_ssl
            )
            
            # Testar conexão
            api_version = self.zabbix.api_version()
            print(f"✅ Conectado com sucesso!")
            print(f"   Versão da API: {api_version}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """Desconectar da API"""
        if self.zabbix:
            print("\n🔌 Desconectando...")
    
    def criar_host(self, hostname: str, ip: str, group_id: int = 4, 
                   description: str = "") -> Optional[str]:
        """
        Criar um novo host no Zabbix
        
        Args:
            hostname: Nome do host (ex: "Servidor Web 01")
            ip: Endereço IP do host
            group_id: ID do grupo (padrão: 4 = "Servers")
            description: Descrição do host
            
        Returns:
            str: ID do host criado, ou None se falhar
        """
        try:
            print(f"\n📝 Criando host: {hostname}")
            
            host_data = {
                "host": hostname,
                "name": hostname,
                "groups": [{"groupid": group_id}],
                "interfaces": [
                    {
                        "type": 1,  # 1 = Zabbix agent
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": "10050"
                    }
                ]
            }
            
            if description:
                host_data["description"] = description
            
            result = self.zabbix.host.create(**host_data)
            host_id = result.get('hostids', [None])[0]
            
            print(f"✅ Host criado com sucesso!")
            print(f"   ID: {host_id}")
            print(f"   Nome: {hostname}")
            print(f"   IP: {ip}")
            
            return host_id
            
        except Exception as e:
            print(f"❌ Erro ao criar host: {e}")
            return None
    
    def criar_item(self, host_id: str, name: str, key: str, 
                   item_type: int = 0, value_type: int = 3,
                   interval: int = 60) -> Optional[str]:
        """
        Criar um novo item (métrica) para um host
        
        Args:
            host_id: ID do host
            name: Nome do item (ex: "CPU Usage")
            key: Chave única do item (ex: "system.cpu.load")
            item_type: Tipo de item (0=Zabbix agent, 2=SNMP, 3=IPMI, etc)
            value_type: Tipo de valor (0=numeric, 1=string, 2=log, 3=unsigned int, 4=float)
            interval: Intervalo de coleta em segundos
            
        Returns:
            str: ID do item criado, ou None se falhar
        """
        try:
            print(f"\n📊 Criando item: {name}")
            
            item_data = {
                "hostid": host_id,
                "name": name,
                "key_": key,
                "type": item_type,
                "value_type": value_type,
                "delay": f"{interval}s",  # Interval em segundos
                "units": "",
                "history": "90d",  # Manter histórico por 90 dias
                "trends": "365d"   # Manter trends por 1 ano
            }
            
            result = self.zabbix.item.create(**item_data)
            item_id = result.get('itemids', [None])[0]
            
            print(f"✅ Item criado com sucesso!")
            print(f"   ID: {item_id}")
            print(f"   Nome: {name}")
            print(f"   Chave: {key}")
            print(f"   Intervalo: {interval}s")
            
            return item_id
            
        except Exception as e:
            print(f"❌ Erro ao criar item: {e}")
            return None
    
    def criar_trigger(self, name: str, expression: str, 
                     severity: int = 2, description: str = "") -> Optional[str]:
        """
        Criar um novo trigger (alerta)
        
        Args:
            name: Nome do trigger (ex: "High CPU Usage")
            expression: Expressão do trigger (ex: "{Host:item.last()}>80")
            severity: Severidade (0=Not classified, 1=Info, 2=Warning, 3=Average, 4=High, 5=Disaster)
            description: Descrição do trigger
            
        Returns:
            str: ID do trigger criado, ou None se falhar
        """
        try:
            print(f"\n⚠️  Criando trigger: {name}")
            
            trigger_data = {
                "description": name,
                "expression": expression,
                "priority": severity,  # 0-5
                "status": 0,  # 0 = enabled
                "type": 0     # 0 = problem/recovery
            }
            
            if description:
                trigger_data["comments"] = description
            
            result = self.zabbix.trigger.create(**trigger_data)
            trigger_id = result.get('triggerids', [None])[0]
            
            severities = ["Not classified", "Info", "Warning", "Average", "High", "Disaster"]
            
            print(f"✅ Trigger criado com sucesso!")
            print(f"   ID: {trigger_id}")
            print(f"   Nome: {name}")
            print(f"   Severidade: {severities[severity]}")
            print(f"   Expressão: {expression}")
            
            return trigger_id
            
        except Exception as e:
            print(f"❌ Erro ao criar trigger: {e}")
            return None
    
    def listar_hosts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Listar hosts
        
        Args:
            limit: Quantidade máxima de hosts a retornar
            
        Returns:
            List: Lista de hosts
        """
        try:
            print(f"\n📋 Listando hosts (limite: {limit})...")
            
            hosts = self.zabbix.host.get(
                limit=limit,
                output=['hostid', 'host', 'name', 'status'],
                sortfield='name'
            )
            
            if not hosts:
                print("   Nenhum host encontrado")
                return []
            
            print(f"✅ {len(hosts)} host(s) encontrado(s):\n")
            
            for host in hosts:
                status = "Ativo" if host['status'] == '0' else "Desabilitado"
                print(f"   ID: {host['hostid']:20} | {host['name']:30} | {status}")
            
            return hosts
            
        except Exception as e:
            print(f"❌ Erro ao listar hosts: {e}")
            return []
    
    def listar_items(self, host_id: str) -> List[Dict[str, Any]]:
        """
        Listar items de um host
        
        Args:
            host_id: ID do host
            
        Returns:
            List: Lista de items
        """
        try:
            print(f"\n📊 Listando items do host {host_id}...")
            
            items = self.zabbix.item.get(
                hostid=host_id,
                output=['itemid', 'name', 'key_', 'lastvalue', 'lastclock'],
                sortfield='name'
            )
            
            if not items:
                print("   Nenhum item encontrado")
                return []
            
            print(f"✅ {len(items)} item(ns) encontrado(s):\n")
            
            for item in items:
                print(f"   {item['name']:30} | Chave: {item['key_']:30}")
            
            return items
            
        except Exception as e:
            print(f"❌ Erro ao listar items: {e}")
            return []
    
    def listar_triggers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Listar triggers
        
        Args:
            limit: Quantidade máxima de triggers a retornar
            
        Returns:
            List: Lista de triggers
        """
        try:
            print(f"\n⚠️  Listando triggers (limite: {limit})...")
            
            triggers = self.zabbix.trigger.get(
                limit=limit,
                output=['triggerid', 'description', 'priority', 'status'],
                sortfield='description'
            )
            
            if not triggers:
                print("   Nenhum trigger encontrado")
                return []
            
            print(f"✅ {len(triggers)} trigger(s) encontrado(s):\n")
            
            severities = ["Not classified", "Info", "Warning", "Average", "High", "Disaster"]
            
            for trigger in triggers:
                priority = int(trigger['priority'])
                severity = severities[priority] if priority < len(severities) else "Unknown"
                print(f"   {trigger['description']:40} | {severity}")
            
            return triggers
            
        except Exception as e:
            print(f"❌ Erro ao listar triggers: {e}")
            return []
    
    def obter_grupo_id(self, group_name: str = "Servers") -> Optional[str]:
        """
        Obter ID de um grupo por nome
        
        Args:
            group_name: Nome do grupo (padrão: "Servers")
            
        Returns:
            str: ID do grupo, ou None se não encontrado
        """
        try:
            groups = self.zabbix.hostgroup.get(
                output=['groupid', 'name'],
                filter={'name': group_name}
            )
            
            if groups:
                return groups[0]['groupid']
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao obter grupo: {e}")
            return None


def exemplo_completo():
    """Executar um exemplo completo de testes"""
    
    print("=" * 70)
    print("  TESTE COMPLETO DA API DO ZABBIX".center(70))
    print("=" * 70)
    
    # Configuração (ajuste conforme seu ambiente)
    ZABBIX_URL = "http://localhost/zabbix"  # Mudar para seu URL do Zabbix
    ZABBIX_USER = "Admin"                    # Usuário padrão do Zabbix
    ZABBIX_PASSWORD = "zabbix"               # Senha padrão do Zabbix
    
    # Criar tester
    tester = ZabbixTester(ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD)
    
    # Conectar
    if not tester.conectar():
        print("\n❌ Não foi possível conectar ao Zabbix!")
        print("   Certifique-se de que:")
        print("   1. O Zabbix está rodando em:", ZABBIX_URL)
        print("   2. As credenciais estão corretas")
        print("   3. A URL está acessível")
        return
    
    # Listar hosts existentes
    tester.listar_hosts(limit=5)
    
    # Criar um novo host
    print("\n" + "=" * 70)
    print("  CRIANDO NOVO HOST".center(70))
    print("=" * 70)
    
    host_id = tester.criar_host(
        hostname="TestServer-001",
        ip="192.168.1.100",
        description="Servidor de teste para aprender Zabbix API"
    )
    
    if host_id:
        # Criar items
        print("\n" + "=" * 70)
        print("  CRIANDO ITEMS (MÉTRICAS)".center(70))
        print("=" * 70)
        
        item1_id = tester.criar_item(
            host_id=host_id,
            name="CPU Load Average",
            key="system.cpu.load[percpu,avg1]",
            value_type=0,  # numeric
            interval=60
        )
        
        item2_id = tester.criar_item(
            host_id=host_id,
            name="Memory Usage",
            key="vm.memory.size[pused]",
            value_type=0,  # numeric
            interval=60
        )
        
        item3_id = tester.criar_item(
            host_id=host_id,
            name="Disk Space Free",
            key="vfs.fs.size[/,pfree]",
            value_type=0,  # numeric
            interval=300
        )
        
        # Criar triggers
        print("\n" + "=" * 70)
        print("  CRIANDO TRIGGERS (ALERTAS)".center(70))
        print("=" * 70)
        
        if item1_id:
            tester.criar_trigger(
                name="High CPU Usage",
                expression=f"{{TestServer-001:system.cpu.load[percpu,avg1].last()}}>4",
                severity=3,  # Average
                description="CPU com uso alto (acima de 4)"
            )
        
        if item2_id:
            tester.criar_trigger(
                name="Low Memory Available",
                expression=f"{{TestServer-001:vm.memory.size[pused].last()}}>80",
                severity=4,  # High
                description="Pouca memória disponível (menos de 20%)"
            )
        
        # Listar items criados
        print("\n" + "=" * 70)
        print("  VERIFICANDO ITEMS CRIADOS".center(70))
        print("=" * 70)
        
        tester.listar_items(host_id)
    
    # Listar triggers
    print("\n" + "=" * 70)
    print("  VERIFICANDO TRIGGERS".center(70))
    print("=" * 70)
    
    tester.listar_triggers(limit=5)
    
    # Desconectar
    tester.desconectar()
    
    print("\n" + "=" * 70)
    print("  ✅ TESTE CONCLUÍDO COM SUCESSO!".center(70))
    print("=" * 70)
    print("\n📚 Próximos passos:")
    print("   1. Acesse a interface web do Zabbix")
    print("   2. Vá para Configuration → Hosts")
    print("   3. Encontre o host 'TestServer-001'")
    print("   4. Verifique os items e triggers criados")
    print("   5. Experimente editar e criar mais recursos via API")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        exemplo_completo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
