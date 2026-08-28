# App de Exemplo — API + Zabbix

API REST mínima (Flask) para testar monitoramento de aplicação no Zabbix
com dados reais, usando itens **trapper** (push via Zabbix Sender) em vez
de exigir Zabbix Agent instalado.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `app.py` | API Flask com `/health`, `/api/users`, `/api/users/<nome>`, `/api/fail` (gera erro 500 de propósito) e `/metrics` (agrega `requests_total`, `errors_total`, `avg_latency_ms`, `uptime_seconds`) |
| `zabbix_sender.py` | Implementação própria (Python puro) do protocolo Zabbix Sender — envia métricas por conexão de saída, sem depender do binário `zabbix_sender` nem abrir porta de entrada |
| `enviar_metricas.py` | Lê `/metrics` da app e envia os valores ao Zabbix |

## Passo a passo

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Rode a API:
   ```bash
   python3 app.py
   ```

3. Crie no Zabbix um host (ex: `AppWebExemplo`) com 4 itens **do tipo
   Zabbix trapper**, com estas chaves exatas:
   - `requests_total` (numeric unsigned)
   - `errors_total` (numeric unsigned)
   - `avg_latency_ms` (numeric float)
   - `uptime_seconds` (numeric float)

   Pode usar o `ZabbixTester` (`../zabbix_api_tester.py`) para isso — os
   itens trapper usam `item_type=2` e não precisam de `interfaceid`.

4. Gere tráfego na API (`curl`, navegador, etc.) e envie as métricas:
   ```bash
   python3 enviar_metricas.py --zabbix-server <IP_DO_SEU_ZABBIX> --host AppWebExemplo
   ```

5. Crie um trigger de exemplo, ex: `last(/AppWebExemplo/errors_total)>=5`.

Repita o passo 4 periodicamente (cron, loop, etc.) para manter os dados
atualizados — itens trapper só recebem valor quando alguém envia.
