#!/usr/bin/env python3
"""
Aplicação Web de Exemplo - API Básica
======================================

API REST simples usada para gerar métricas reais (total de requisições,
erros e latência média) que depois são enviadas ao Zabbix via Zabbix
Sender (itens do tipo trapper), para testar monitoramento de aplicação.

Uso:
    python3 app.py
    # abre em http://127.0.0.1:5000

Endpoints:
    GET  /health           -> status simples
    GET  /api/users        -> lista usuários de exemplo
    GET  /api/users/<nome> -> detalhe de um usuário (404 se não existir)
    GET  /api/fail         -> força um erro 500 (para testar trigger)
    GET  /metrics          -> métricas agregadas em JSON
"""
import threading
import time

from flask import Flask, g, jsonify

app = Flask(__name__)

_start_time = time.time()
_lock = threading.Lock()
_stats = {
    "requests_total": 0,
    "errors_total": 0,
    "latency_sum_ms": 0.0,
}

_USERS = {"alice": 30, "bob": 25, "carol": 40}


@app.before_request
def _start_timer():
    g.t0 = time.time()


@app.after_request
def _record_metrics(response):
    elapsed_ms = (time.time() - g.t0) * 1000
    with _lock:
        _stats["requests_total"] += 1
        _stats["latency_sum_ms"] += elapsed_ms
        if response.status_code >= 400:
            _stats["errors_total"] += 1
    return response


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/users")
def list_users():
    return jsonify(users=list(_USERS.keys()))


@app.route("/api/users/<nome>")
def get_user(nome):
    if nome not in _USERS:
        return jsonify(error="not found"), 404
    return jsonify(name=nome, age=_USERS[nome])


@app.route("/api/fail")
def fail():
    # Endpoint só pra gerar erro 500 de propósito e testar o trigger.
    return jsonify(error="simulated failure"), 500


@app.route("/metrics")
def metrics():
    with _lock:
        req = _stats["requests_total"]
        err = _stats["errors_total"]
        avg_latency = (_stats["latency_sum_ms"] / req) if req else 0.0
    return jsonify(
        requests_total=req,
        errors_total=err,
        avg_latency_ms=round(avg_latency, 2),
        uptime_seconds=round(time.time() - _start_time, 1),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
