#!/usr/bin/env python3
"""Automated integration tests for the isolated Energia Inteligente lab copy."""
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
DATA = ROOT / "test-data"
DB = DATA / "automated-test.db"
JAR = ROOT / "target" / "energia-inteligente-0.0.1-SNAPSHOT.jar"
LOG = HERE / "backend-test.log"
REPORT = HERE / "RELATORIO-TESTES.md"
PORT = 18081
BASE = "http://127.0.0.1:" + str(PORT)
CASES = []
PROCESS = None
LOG_HANDLE = None
SIM_ID = None
USER_ID = None


class CheckFailed(Exception):
    pass


def http(method, path, payload=None, raw=None):
    body = raw if raw is not None else (None if payload is None else json.dumps(payload).encode("utf-8"))
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def start_server():
    global PROCESS, LOG_HANDLE
    env = os.environ.copy()
    env.pop("NVIDIA_API_KEY", None)
    env["SPRING_DATASOURCE_URL"] = "jdbc:sqlite:" + DB.as_posix()
    env["SERVER_PORT"] = str(PORT)
    LOG_HANDLE = LOG.open("a", encoding="utf-8")
    PROCESS = subprocess.Popen(
        ["java", "-jar", str(JAR)], cwd=str(ROOT), env=env,
        stdout=LOG_HANDLE, stderr=subprocess.STDOUT
    )
    deadline = time.time() + 45
    last = "aguardando inicialização"
    while time.time() < deadline:
        if PROCESS.poll() is not None:
            raise RuntimeError("Spring Boot encerrou com código " + str(PROCESS.returncode))
        try:
            status, body = http("GET", "/api/teste")
            if status == 200:
                return
            last = "HTTP " + str(status) + " " + body[:200]
        except Exception as exc:
            last = str(exc)
        time.sleep(0.5)
    raise RuntimeError("API não iniciou em 45 segundos. Último erro: " + last)


def stop_server():
    global PROCESS, LOG_HANDLE
    if PROCESS is not None and PROCESS.poll() is None:
        PROCESS.terminate()
        try:
            PROCESS.wait(timeout=10)
        except subprocess.TimeoutExpired:
            PROCESS.kill()
            PROCESS.wait(timeout=5)
    PROCESS = None
    if LOG_HANDLE is not None:
        LOG_HANDLE.close()
        LOG_HANDLE = None


def check(name, expected, func):
    try:
        actual = func()
        CASES.append({"name": name, "status": "PASS", "expected": expected, "actual": str(actual)})
        print("[PASS] " + name + " — " + str(actual))
    except CheckFailed as exc:
        CASES.append({"name": name, "status": "FAIL", "expected": expected, "actual": str(exc)})
        print("[FAIL] " + name + " — " + str(exc))
    except Exception as exc:
        CASES.append({"name": name, "status": "ERROR", "expected": expected,
                      "actual": type(exc).__name__ + ": " + str(exc)})
        print("[ERROR] " + name + " — " + type(exc).__name__ + ": " + str(exc))


def json_ok(method, path, payload=None):
    status, body = http(method, path, payload)
    if status < 200 or status >= 300:
        raise CheckFailed("esperado 2xx, recebido HTTP " + str(status) + ": " + body[:300])
    try:
        return json.loads(body) if body else None
    except json.JSONDecodeError:
        raise CheckFailed("resposta deveria ser JSON: " + body[:300])


def test_health():
    status, body = http("GET", "/api/teste")
    if status != 200 or "funcionando" not in body.lower():
        raise CheckFailed("esperado HTTP 200 e mensagem de saúde; recebido " + str(status) + ": " + body)
    return "HTTP 200"


def test_create_sim():
    global SIM_ID
    data = {"consumoMensal": 350, "areaDisponivel": 40, "investimento": 15000,
            "localizacao": "TESTE AUTOMATIZADO JANDIRA"}
    obj = json_ok("POST", "/api/simulacoes", data)
    SIM_ID = obj.get("id")
    if not SIM_ID:
        raise CheckFailed("resposta sem ID: " + str(obj))
    if obj.get("consumoMensal") != 350 or obj.get("localizacao") != data["localizacao"]:
        raise CheckFailed("campos retornados divergentes: " + str(obj))
    return "criada simulação ID " + str(SIM_ID)


def test_list_sim():
    rows = json_ok("GET", "/api/simulacoes")
    matches = [row for row in rows if row.get("id") == SIM_ID]
    if len(matches) != 1:
        raise CheckFailed("registro não encontrado ou duplicado na listagem")
    return "simulação encontrada"


def test_persistence_after_restart():
    stop_server()
    start_server()
    rows = json_ok("GET", "/api/simulacoes")
    if not any(row.get("id") == SIM_ID for row in rows):
        raise CheckFailed("registro desapareceu após reiniciar a aplicação")
    return "registro preservado após reinício"


def test_create_user():
    global USER_ID
    data = {"nome": "USUARIO AUTOMATED QA", "email": "qa-automated@example.invalid"}
    obj = json_ok("POST", "/api/usuarios", data)
    USER_ID = obj.get("id")
    if not USER_ID or obj.get("email") != data["email"]:
        raise CheckFailed("resposta inesperada: " + str(obj))
    return "criado usuário ID " + str(USER_ID)


def test_list_user():
    rows = json_ok("GET", "/api/usuarios")
    if not any(row.get("id") == USER_ID for row in rows):
        raise CheckFailed("usuário não encontrado")
    return "usuário encontrado"


def test_update_user():
    data = {"nome": "USUARIO QA ATUALIZADO", "email": "qa-updated@example.invalid"}
    obj = json_ok("PUT", "/api/usuarios/" + str(USER_ID), data)
    if obj.get("nome") != data["nome"] or obj.get("email") != data["email"]:
        raise CheckFailed("resposta não contém os novos dados: " + str(obj))
    return "nome e e-mail atualizados"


def test_delete_user():
    status, body = http("DELETE", "/api/usuarios/" + str(USER_ID))
    if status not in (200, 204):
        raise CheckFailed("esperado HTTP 200/204, recebido " + str(status) + ": " + body[:200])
    rows = json_ok("GET", "/api/usuarios")
    if any(row.get("id") == USER_ID for row in rows):
        raise CheckFailed("usuário ainda aparece após DELETE")
    return "usuário removido e ausência confirmada"


def test_malformed_json():
    status, body = http("POST", "/api/simulacoes", raw=b'{"consumoMensal":')
    if status != 400:
        raise CheckFailed("esperado HTTP 400, recebido " + str(status) + ": " + body[:250])
    return "HTTP 400"


def test_empty_simulation():
    status, body = http("POST", "/api/simulacoes", {})
    if status not in (400, 422):
        raise CheckFailed("esperado HTTP 400/422, recebido " + str(status) + ": " + body[:250])
    return "HTTP " + str(status)


def test_empty_user():
    status, body = http("POST", "/api/usuarios", {})
    if status not in (400, 422):
        raise CheckFailed("esperado HTTP 400/422, recebido " + str(status) + ": " + body[:250])
    return "HTTP " + str(status)


def test_negative_simulation():
    data = {"consumoMensal": -1, "areaDisponivel": -10, "investimento": -100,
            "localizacao": "DADOS NEGATIVOS TESTE"}
    status, body = http("POST", "/api/simulacoes", data)
    if status not in (400, 422):
        raise CheckFailed("esperado HTTP 400/422, recebido " + str(status) + ": " + body[:250])
    return "HTTP " + str(status)


def test_missing_analysis_target():
    status, body = http("POST", "/api/simulacoes/987654321/analise")
    if status != 404:
        raise CheckFailed("esperado HTTP 404, recebido " + str(status) + ": " + body[:250])
    return "HTTP 404"


def test_missing_api_key():
    status, body = http("POST", "/api/simulacoes/" + str(SIM_ID) + "/analise")
    if status not in (424, 503):
        raise CheckFailed("esperado HTTP 424/503 sem chave; recebido " + str(status) + ": " + body[:250])
    return "HTTP " + str(status) + " sem chave, sem chamada externa"


def write_report():
    passed = sum(x["status"] == "PASS" for x in CASES)
    failed = sum(x["status"] == "FAIL" for x in CASES)
    errors = sum(x["status"] == "ERROR" for x in CASES)
    lines = [
        "# Relatório de testes automatizados — Energia Inteligente",
        "",
        "- Data/hora: " + datetime.now().astimezone().isoformat(timespec="seconds"),
        "- Ambiente: cópia isolada Energia-Inteligente-lab-20261115",
        "- Execução: API Spring Boot por HTTP local; roteiro Python padrão",
        "- Porta: 18081",
        "- Banco: test-data/automated-test.db (SQLite descartável)",
        "- NVIDIA_API_KEY: removida do ambiente do processo; nenhum pedido externo enviado",
        "- Projeto original/GitHub: não alterados",
        "",
        "## Resumo",
        "",
        "- Aprovados: **" + str(passed) + "**",
        "- Reprovados: **" + str(failed) + "**",
        "- Erros de execução: **" + str(errors) + "**",
        "- Total: **" + str(len(CASES)) + "**",
        "",
        "## Resultado por caso",
        "",
        "| Caso | Resultado | Esperado | Observado |",
        "|---|---|---|---|",
    ]
    for item in CASES:
        vals = [item["name"], item["status"], item["expected"], item["actual"]]
        vals = [str(v).replace("|", "\\|").replace("\n", " ") for v in vals]
        lines.append("| " + " | ".join(vals) + " |")
    lines += [
        "",
        "## Recomendações para falhas confirmadas",
        "",
        "- Validação de entrada: adicionar spring-boot-starter-validation; criar DTOs com @NotBlank, @Email, "
        "@Positive ou @PositiveOrZero; usar @Valid nos endpoints. Não expor entidades JPA diretamente como DTOs.",
        "- Recursos inexistentes: substituir RuntimeException genérica por ResponseStatusException com "
        "HttpStatus.NOT_FOUND (404), ou exceção de domínio mapeada num ControllerAdvice.",
        "- Chave NVIDIA ausente: mapear configuração ausente para HTTP 503 (ou 424 conforme contrato), "
        "sem revelar detalhes internos ao cliente.",
        "- Atualização de usuário: verificar a existência do ID antes do save; retornar 404 para ID inexistente "
        "se a intenção do endpoint PUT for atualizar apenas registros existentes.",
        "- Integração externa: tratar timeout, erros 4xx/5xx e resposta vazia com mensagens controladas; testar "
        "o serviço com RestClient mockado, sem uma chave real.",
        "",
        "## Evidências",
        "",
        "- Banco de testes: test-data/automated-test.db",
        "- Log do servidor: tests/backend-test.log",
        "- A suíte reinicia a API para verificar persistência.",
        "",
        "## Limitações",
        "",
        "- A chamada real à NVIDIA não foi testada; nenhum segredo foi usado.",
        "- Uma API hospedada não foi testada porque ainda não temos URL confirmada.",
        "- Códigos HTTP 400/422, 404 e 424/503 são critérios de qualidade esperados nesta suíte.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    return passed, failed, errors


def main():
    if not JAR.exists():
        raise SystemExit("JAR não encontrado: " + str(JAR) + ". Compile com .\\mvnw.cmd -B -DskipTests package.")
    DATA.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    if LOG.exists():
        LOG.unlink()
    try:
        start_server()
        check("API-001 Saúde GET /api/teste", "HTTP 200", test_health)
        check("SIM-001 Criar simulação", "HTTP 2xx e ID", test_create_sim)
        check("SIM-002 Listar simulações", "simulação criada encontrada", test_list_sim)
        check("DB-001 Persistência após reiniciar API", "registro permanece", test_persistence_after_restart)
        check("USR-001 Criar usuário", "HTTP 2xx e ID", test_create_user)
        check("USR-002 Listar usuários", "usuário encontrado", test_list_user)
        check("USR-003 Atualizar usuário", "campos atualizados", test_update_user)
        check("USR-004 Excluir usuário", "usuário removido", test_delete_user)
        check("VAL-001 JSON malformado", "HTTP 400", test_malformed_json)
        check("VAL-002 Simulação sem campos obrigatórios", "HTTP 400/422", test_empty_simulation)
        check("VAL-003 Usuário sem nome/e-mail", "HTTP 400/422", test_empty_user)
        check("VAL-004 Valores negativos na simulação", "HTTP 400/422", test_negative_simulation)
        check("ERR-001 Análise de simulação inexistente", "HTTP 404", test_missing_analysis_target)
        check("AI-001 Sem chave NVIDIA", "HTTP 424/503 controlado; sem tráfego externo", test_missing_api_key)
    except Exception as exc:
        CASES.append({"name": "Infraestrutura/inicialização", "status": "ERROR",
                      "expected": "Spring Boot iniciar em porta local", "actual": type(exc).__name__ + ": " + str(exc)})
        print("[ERROR] Infraestrutura — " + type(exc).__name__ + ": " + str(exc))
    finally:
        stop_server()
    passed, failed, errors = write_report()
    print("")
    print("RESUMO PASS=" + str(passed) + " FAIL=" + str(failed) + " ERROR=" + str(errors))
    print("RELATORIO=" + str(REPORT))
    print("BANCO=" + str(DB))
    print("LOG=" + str(LOG))
    if failed or errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
