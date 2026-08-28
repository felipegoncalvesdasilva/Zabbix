#!/usr/bin/env python3
"""
Lê /metrics da app_exemplo e envia os valores para o Zabbix via
zabbix_sender.py (protocolo trapper).

Uso:
    python3 enviar_metricas.py --zabbix-server 192.168.1.10 --host AppWebExemplo

    # ou usando variáveis de ambiente:
    ZABBIX_SERVER=192.168.1.10 ZABBIX_HOST=AppWebExemplo python3 enviar_metricas.py

Pré-requisitos:
    1. A app_exemplo (app.py) rodando em APP_URL (padrão http://127.0.0.1:5000)
    2. Um host no Zabbix com esse nome, com 4 itens trapper:
       requests_total, errors_total, avg_latency_ms, uptime_seconds
"""
import argparse
import os
import sys

import requests
from zabbix_sender import enviar_metricas


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--app-url", default=os.environ.get("APP_URL", "http://127.0.0.1:5000"))
    parser.add_argument("--zabbix-server", default=os.environ.get("ZABBIX_SERVER"), required=os.environ.get("ZABBIX_SERVER") is None)
    parser.add_argument("--zabbix-port", type=int, default=int(os.environ.get("ZABBIX_PORT", "10051")))
    parser.add_argument("--host", default=os.environ.get("ZABBIX_HOST", "AppWebExemplo"))
    args = parser.parse_args()

    try:
        m = requests.get(f"{args.app_url}/metrics", timeout=5).json()
    except requests.RequestException as e:
        print(f"Não foi possível ler {args.app_url}/metrics: {e}", file=sys.stderr)
        sys.exit(1)

    print("Métricas locais:", m)

    resultado = enviar_metricas(args.zabbix_server, args.host, m, port=args.zabbix_port)
    print("Resposta do Zabbix:", resultado)

    if resultado.get("response") != "success":
        sys.exit(1)


if __name__ == "__main__":
    main()
