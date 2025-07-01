import sqlite3
import re
import spacy
import unicodedata

# Carrega modelo spaCy para NLP em português
nlp = spacy.load("pt_core_news_sm")

def inicializar_contexto():
    """
    Inicializa o dicionário de contexto compartilhado.
    """
    return {
        "ultimo_tecnico": None,
        "nome_ultimo_tecnico": None,
        "especialidade_ultimo_tecnico": None,
        "turno_ultimo_tecnico": None,
        "ultima_ordem": None,
        "equipamento_ultima_ordem": None,
        "status_ultimo_equipamento": None
    }

def resposta_contexto(contexto, campo, mensagem_ok, mensagem_faltando):
    """
    Retorna mensagem de contexto se disponível.
    """
    valor = contexto.get(campo)
    if valor:
        return mensagem_ok.format(valor)
    else:
        return mensagem_faltando

def interpretar_pergunta_nlp(pergunta, contexto):
    """
    Analisa a pergunta em linguagem natural e devolve uma query SQL ou mensagem.
    """
    # Normaliza o texto
    pergunta_normalizada = (
        unicodedata.normalize("NFKD", pergunta.lower())
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )

    # Extrai números da pergunta
    doc = nlp(pergunta_normalizada)
    numeros = [ent.text for ent in doc.ents if ent.label_ == "CARDINAL"]
    if not numeros:
        numeros = re.findall(r"\b\d+\b", pergunta)

    # Detecta intenção e monta query
    if "ordem" in pergunta_normalizada and any(k in pergunta_normalizada for k in ["tecnico", "executou", "responsavel"]):
        if numeros:
            ordem = numeros[0]
            return (
                "SELECT t.id_tecnico, t.nome, t.especialidade, t.turno, ot.id_ordem, o.id_equipamento "
                "FROM tecnicos t "
                "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
                "JOIN ordens_manutencao o ON ot.id_ordem = o.id_ordem "
                f"WHERE ot.id_ordem = {ordem}"
            )
        else:
            return "Por favor, informe o número da ordem."

    if "tecnico" in pergunta_normalizada and any(k in pergunta_normalizada for k in ["mais ordens", "mais intervencoes", "mais manutencao"]):
        return (
            "SELECT t.nome, COUNT(ot.id_ordem) as total "
            "FROM tecnicos t "
            "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
            "GROUP BY t.id_tecnico ORDER BY total DESC LIMIT 1"
        )

    if any(k in pergunta_normalizada for k in ["listar tecnicos", "quais tecnicos", "me liste todos os tecnicos"]):
        return "SELECT id_tecnico, nome, especialidade, turno FROM tecnicos"

    if any(k in pergunta_normalizada for k in ["listar equipamentos", "quais equipamentos", "liste todos os equipamentos"]):
        return "SELECT id_equipamento, tipo, localizacao, status FROM equipamentos"

    if "ordens abertas" in pergunta_normalizada or "ordens estao abertas" in pergunta_normalizada:
        return "SELECT id_ordem, id_equipamento, status FROM ordens_manutencao WHERE status = 'aberta'"

    if ("ordens em andamento" in pergunta_normalizada) or (
        "quantas ordens" in pergunta_normalizada and "andamento" in pergunta_normalizada
    ):
        return "SELECT COUNT(*) FROM ordens_manutencao WHERE status = 'em andamento'"

    if "tipos de equipamentos" in pergunta_normalizada and "ultimos 3 meses" in pergunta_normalizada:
        return (
            "SELECT DISTINCT e.tipo "
            "FROM equipamentos e "
            "JOIN ordens_manutencao o ON e.id_equipamento = o.id_equipamento "
            "WHERE o.data_abertura >= date('now', '-3 months')"
        )

    if "status do equipamento" in pergunta_normalizada:
        eq = numeros[0] if numeros else contexto.get("equipamento_ultima_ordem")
        if eq:
            return f"SELECT id_equipamento, tipo, localizacao, status FROM equipamentos WHERE id_equipamento = {eq}"
        else:
            return "Desculpe, poderia informar o número do equipamento?"

    if "historico" in pergunta_normalizada and "equipamento" in pergunta_normalizada and numeros:
        eq = numeros[0]
        return (
            "SELECT id_ordem, data_abertura, data_conclusao, tipo_manutencao, status "
            f"FROM ordens_manutencao WHERE id_equipamento = {eq}"
        )

    if "data de abertura" in pergunta_normalizada and numeros:
        ordem = numeros[0]
        return f"SELECT data_abertura FROM ordens_manutencao WHERE id_ordem = {ordem}"

    if "tipo de manutencao" in pergunta_normalizada and numeros:
        ordem = numeros[0]
        return f"SELECT tipo_manutencao FROM ordens_manutencao WHERE id_ordem = {ordem}"

    if "especialidade" in pergunta_normalizada:
        return resposta_contexto(
            contexto,
            "especialidade_ultimo_tecnico",
            "A especialidade do último técnico foi {}.",
            "Ainda não tenho essa informação."
        )

    if "turno" in pergunta_normalizada:
        return resposta_contexto(
            contexto,
            "turno_ultimo_tecnico",
            "O último técnico trabalhava no turno {}.",
            "Ainda não sei o turno do técnico."
        )

    if "qual e mesmo o tecnico" in pergunta_normalizada or "quem era o tecnico" in pergunta_normalizada:
        return resposta_contexto(
            contexto,
            "nome_ultimo_tecnico",
            "O último técnico se chamava {}.",
            "Ainda não sei o nome do técnico."
        )

    if "equipamento da ordem" in pergunta_normalizada or "qual o equipamento" in pergunta_normalizada:
        return resposta_contexto(
            contexto,
            "equipamento_ultima_ordem",
            "O equipamento da última ordem foi {}.",
            "Ainda não sei qual era o equipamento."
        )

    return "Desculpe, não consegui entender sua pergunta. Pode reformular?"

def executar_consulta(sql, contexto):
    """
    Executa a consulta SQL e atualiza contexto quando necessário.
    """
    if not sql:
        return "Desculpe, não consegui entender sua pergunta. Pode reformular?"

    # Se não for um SELECT, apenas retorne a mensagem
    if not sql.lower().strip().startswith("select"):
        return sql

    # Executa SELECT
    conn = sqlite3.connect("manutencao_industrial.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "Não encontrei informações sobre isso."

    resposta = []
    for row in rows:
        if len(row) == 6:
            # Atualiza contexto ao consultar técnico por ordem
            contexto.update({
                "ultimo_tecnico": row[0],
                "nome_ultimo_tecnico": row[1],
                "especialidade_ultimo_tecnico": row[2],
                "turno_ultimo_tecnico": row[3],
                "ultima_ordem": row[4],
                "equipamento_ultima_ordem": row[5]
            })
        resposta.append(", ".join(str(r) for r in row))

    return "\n".join(resposta)
