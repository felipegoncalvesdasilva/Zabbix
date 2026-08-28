#!/usr/bin/env python3
"""
Exemplos Práticos de Uso da API Zabbix
=======================================

Este arquivo contém exemplos práticos e simples de como usar a API do Zabbix
para diferentes tarefas comuns.

Copie e adapte os exemplos conforme sua necessidade!
"""

from zabbix_api_tester import ZabbixTester


def exemplo_1_conectar_basico():
    """
    EXEMPLO 1: Conectar ao Zabbix de forma básica
    """
    print("\n" + "="*70)
    print("EXEMPLO 1: Conectar ao Zabbix".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    if tester.conectar():
        print("✅ Conexão estabelecida com sucesso!")
    else:
        print("❌ Falha na conexão!")


def exemplo_2_criar_host_simples():
    """
    EXEMPLO 2: Criar um host simples
    """
    print("\n" + "="*70)
    print("EXEMPLO 2: Criar Host".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    if tester.conectar():
        host_id = tester.criar_host(
            hostname="DatabaseServer",
            ip="192.168.1.20",
            description="Servidor de banco de dados MySQL"
        )
        
        if host_id:
            print(f"\n✅ Host criado! ID: {host_id}")


def exemplo_3_criar_multiplos_items():
    """
    EXEMPLO 3: Criar múltiplos items para um host
    """
    print("\n" + "="*70)
    print("EXEMPLO 3: Criar Múltiplos Items".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    if tester.conectar():
        # Criar host
        host_id = tester.criar_host(
            hostname="AppServer",
            ip="192.168.1.30"
        )
        
        if host_id:
            # Criar vários items de uma vez
            metrics = [
                ("CPU Usage", "system.cpu.load", 0),
                ("Memory Usage", "vm.memory.size[pused]", 0),
                ("Disk Usage", "vfs.fs.size[/,pfree]", 0),
                ("Network In", "net.if.in[eth0]", 0),
                ("Network Out", "net.if.out[eth0]", 0),
            ]
            
            for name, key, value_type in metrics:
                tester.criar_item(
                    host_id=host_id,
                    name=name,
                    key=key,
                    value_type=value_type
                )


def exemplo_4_criar_triggers_completo():
    """
    EXEMPLO 4: Criar triggers com diferentes severidades
    """
    print("\n" + "="*70)
    print("EXEMPLO 4: Criar Triggers".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    if tester.conectar():
        # Criar host
        host_id = tester.criar_host(
            hostname="ProductionServer",
            ip="192.168.1.40"
        )
        
        if host_id:
            # Criar item
            item_id = tester.criar_item(
                host_id=host_id,
                name="CPU Load",
                key="system.cpu.load"
            )
            
            if item_id:
                # Criar triggers com diferentes severidades
                triggers = [
                    {
                        "name": "CPU Warning",
                        "expression": "last(/ProductionServer/system.cpu.load)>2",
                        "severity": 2  # Warning
                    },
                    {
                        "name": "CPU High",
                        "expression": "last(/ProductionServer/system.cpu.load)>3",
                        "severity": 4  # High
                    },
                    {
                        "name": "CPU Critical",
                        "expression": "last(/ProductionServer/system.cpu.load)>4",
                        "severity": 5  # Disaster
                    }
                ]
                
                for trigger in triggers:
                    tester.criar_trigger(
                        name=trigger["name"],
                        expression=trigger["expression"],
                        severity=trigger["severity"],
                        description=f"Alerta de CPU - {trigger['name']}"
                    )


def exemplo_5_listar_e_filtrar():
    """
    EXEMPLO 5: Listar e filtrar recursos
    """
    print("\n" + "="*70)
    print("EXEMPLO 5: Listar e Filtrar Recursos".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    if tester.conectar():
        print("\n📋 Listando hosts...")
        hosts = tester.listar_hosts(limit=20)
        
        if hosts:
            # Filtrar apenas hosts ativos
            hosts_ativos = [h for h in hosts if h['status'] == '0']
            print(f"\n✅ Total de hosts: {len(hosts)}")
            print(f"✅ Hosts ativos: {len(hosts_ativos)}")
            
            # Listar items do primeiro host
            if hosts_ativos:
                first_host_id = hosts_ativos[0]['hostid']
                print(f"\n📊 Items do host '{hosts_ativos[0]['name']}':")
                tester.listar_items(first_host_id)


def exemplo_6_script_inteligente():
    """
    EXEMPLO 6: Script inteligente que verifica e cria se não existir
    """
    print("\n" + "="*70)
    print("EXEMPLO 6: Script Inteligente".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    if tester.conectar():
        # Dados do servidor
        servidor = {
            "hostname": "SmartServer",
            "ip": "192.168.1.50",
            "description": "Servidor inteligente"
        }
        
        # Verificar se host já existe
        try:
            hosts = tester.zabbix.host.get(
                filter={"host": servidor["hostname"]},
                output=['hostid']
            )
            
            if hosts:
                print(f"✅ Host '{servidor['hostname']}' já existe!")
                host_id = hosts[0]['hostid']
            else:
                print(f"❌ Host não existe, criando...")
                host_id = tester.criar_host(**servidor)
            
            if host_id:
                print(f"\n✅ Usando host ID: {host_id}")
                
                # Criar items se não existirem
                items_necessarios = [
                    ("System Uptime", "system.uptime"),
                    ("System Load", "system.cpu.load"),
                ]
                
                for name, key in items_necessarios:
                    # Verificar se item já existe
                    existing_items = tester.zabbix.item.get(
                        filter={"key_": key, "hostid": host_id},
                        output=['itemid']
                    )
                    
                    if not existing_items:
                        print(f"   Criando item: {name}")
                        tester.criar_item(
                            host_id=host_id,
                            name=name,
                            key=key
                        )
                    else:
                        print(f"   ✅ Item '{name}' já existe")
        
        except Exception as e:
            print(f"❌ Erro: {e}")


def exemplo_7_usar_variaveis_ambiente():
    """
    EXEMPLO 7: Usar variáveis de ambiente para segurança
    """
    print("\n" + "="*70)
    print("EXEMPLO 7: Usar Variáveis de Ambiente".center(70))
    print("="*70 + "\n")
    
    import os
    from dotenv import load_dotenv
    
    # Carregar variáveis do arquivo .env
    load_dotenv()
    
    # Obter credenciais de variáveis de ambiente
    zabbix_url = os.getenv('ZABBIX_URL', 'http://localhost/zabbix')
    zabbix_user = os.getenv('ZABBIX_USER', 'Admin')
    zabbix_password = os.getenv('ZABBIX_PASSWORD', 'zabbix')
    
    print(f"✅ Usando credenciais de variáveis de ambiente:")
    print(f"   URL: {zabbix_url}")
    print(f"   User: {zabbix_user}")
    print(f"   Password: ****** (oculta por segurança)")
    
    tester = ZabbixTester(zabbix_url, zabbix_user, zabbix_password)
    
    if tester.conectar():
        print("\n✅ Conectado com sucesso usando variáveis de ambiente!")


def exemplo_8_tratamento_erros():
    """
    EXEMPLO 8: Tratamento robusto de erros
    """
    print("\n" + "="*70)
    print("EXEMPLO 8: Tratamento de Erros".center(70))
    print("="*70 + "\n")
    
    tester = ZabbixTester(
        url="http://localhost/zabbix",
        username="Admin",
        password="zabbix"
    )
    
    try:
        if not tester.conectar():
            print("❌ Não foi possível conectar ao Zabbix!")
            print("\nCausas comuns:")
            print("  1. Zabbix não está rodando")
            print("  2. URL incorreta")
            print("  3. Firewall bloqueando a conexão")
            return
        
        # Tentar criar host
        host_id = tester.criar_host(
            hostname="ErrorTestServer",
            ip="192.168.1.60"
        )
        
        if not host_id:
            print("❌ Erro ao criar host!")
            return
        
        # Tentar criar item com dados inválidos
        item_id = tester.criar_item(
            host_id=host_id,
            name="Test Item",
            key="sistema.invalida.chave"  # Chave inválida
        )
        
        if not item_id:
            print("⚠️  Item não foi criado (chave pode ser inválida)")
            print("   Tente usar uma chave conhecida como 'system.uptime'")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("\nDica: Verifique a documentação da API do Zabbix")


# Executar exemplos
if __name__ == "__main__":
    import sys
    
    exemplos = {
        "1": exemplo_1_conectar_basico,
        "2": exemplo_2_criar_host_simples,
        "3": exemplo_3_criar_multiplos_items,
        "4": exemplo_4_criar_triggers_completo,
        "5": exemplo_5_listar_e_filtrar,
        "6": exemplo_6_script_inteligente,
        "7": exemplo_7_usar_variaveis_ambiente,
        "8": exemplo_8_tratamento_erros,
    }
    
    print("\n" + "="*70)
    print("EXEMPLOS DE USO DA API DO ZABBIX".center(70))
    print("="*70)
    print("\nEscolha um exemplo para executar:\n")
    
    for chave, funcao in exemplos.items():
        print(f"  {chave}. {funcao.__doc__.split(chr(10))[1].strip()}")
    
    print(f"  0. Executar todos")
    print(f"  q. Sair\n")
    
    escolha = input("Digite sua escolha: ").strip()
    
    if escolha == "0":
        print("\n🚀 Executando todos os exemplos...\n")
        for funcao in exemplos.values():
            try:
                funcao()
            except Exception as e:
                print(f"❌ Erro ao executar: {e}")
    
    elif escolha in exemplos:
        try:
            exemplos[escolha]()
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    elif escolha != "q":
        print("❌ Opção inválida!")
    
    print("\n✅ Fim dos exemplos!\n")
