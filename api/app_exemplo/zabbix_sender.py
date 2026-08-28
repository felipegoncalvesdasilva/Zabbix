#!/usr/bin/env python3
"""
Implementação mínima do protocolo Zabbix Sender (trapper), em Python puro.

Envia métricas de um host para o Zabbix server via TCP (porta 10051 por
padrão) sem depender do binário `zabbix_sender`. A conexão é sempre de
saída (o cliente conecta no servidor), então não exige liberar porta de
entrada em nenhum firewall local.

Protocolo: cabeçalho "ZBXD\x01" + tamanho do payload em 8 bytes
little-endian + payload JSON. Referência:
https://www.zabbix.com/documentation/current/en/manual/appendix/protocols/header_datalen
"""
import json
import socket
import struct
import time
from typing import Dict, Union


def enviar_metricas(
    server: str,
    host: str,
    valores: Dict[str, Union[str, int, float]],
    port: int = 10051,
    timeout: float = 10.0,
) -> dict:
    """
    Envia um conjunto de métricas para o Zabbix via protocolo trapper.

    Args:
        server: endereço do Zabbix server
        host: nome do host (como cadastrado no Zabbix) dono das métricas
        valores: dict {chave_do_item: valor}
        port: porta do trapper no Zabbix server (padrão 10051)
        timeout: timeout de conexão/leitura em segundos

    Returns:
        dict com a resposta decodificada do servidor
        (ex: {"response": "success", "info": "processed: 3; failed: 0; ..."})
    """
    clock = int(time.time())
    payload = {
        "request": "sender data",
        "data": [
            {"host": host, "key": chave, "value": str(valor), "clock": clock}
            for chave, valor in valores.items()
        ],
        "clock": clock,
    }
    body = json.dumps(payload).encode("utf-8")
    header = b"ZBXD\x01" + struct.pack("<Q", len(body))

    with socket.create_connection((server, port), timeout=timeout) as sock:
        sock.sendall(header + body)

        resp_header = _recv_exact(sock, 13)
        if resp_header[:5] != b"ZBXD\x01":
            raise ValueError(f"Resposta com cabeçalho inesperado: {resp_header!r}")
        (resp_len,) = struct.unpack("<Q", resp_header[5:13])
        resp_body = _recv_exact(sock, resp_len)

    return json.loads(resp_body.decode("utf-8"))


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    chunks = []
    remaining = n
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("Conexão fechada antes de receber os dados esperados")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Envia uma métrica de teste via Zabbix Sender")
    parser.add_argument("server", help="IP/host do Zabbix server")
    parser.add_argument("host", help="Nome do host cadastrado no Zabbix")
    parser.add_argument("chave", help="Chave do item")
    parser.add_argument("valor", help="Valor a enviar")
    parser.add_argument("--port", type=int, default=10051)
    args = parser.parse_args()

    resultado = enviar_metricas(args.server, args.host, {args.chave: args.valor}, port=args.port)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
