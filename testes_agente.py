from agente import inicializar_contexto, interpretar_pergunta_nlp, executar_consulta

# Inicializa contexto
contexto = inicializar_contexto()

# Lista de perguntas de teste
perguntas = [
    # Contexto
    "Qual técnico trabalhou na ordem 32?",
    "Qual a especialidade dele?",
    "Qual o turno do técnico?",
    "Qual é mesmo o técnico?",
    "Qual o equipamento da ordem?",
    "E o status do equipamento?",

    # Múltiplas tabelas
    "Quais os tipos de equipamentos que tiveram manutenção nos últimos 3 meses?",
    "Qual o nome do técnico que trabalhou em mais ordens de manutenção?",
    "Quem foi o técnico que trabalhou na ordem 1?",
    "Qual a especialidade do técnico da ordem 2?",
    "Me liste todos os técnicos.",
    "Quais equipamentos estão cadastrados?",
    "Quais ordens estão abertas?",
    "Quantas ordens de manutenção estão em andamento?",
    "Qual o status do equipamento 3?",
    "Qual o histórico de manutenções do equipamento 2?",
    "Qual a data de abertura da ordem 4?"
]

print("\nIniciando execução dos testes...\n")

for idx, pergunta in enumerate(perguntas, 1):
    print(f"{idx}. Pergunta: {pergunta}")
    sql = interpretar_pergunta_nlp(pergunta, contexto)
    resposta = executar_consulta(sql, contexto)
    print(f"Resposta:\n{resposta}\n")
    print("-" * 70)
