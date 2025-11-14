import os
import sys
from groq import Groq

def main():
    print("Iniciando script call_ai_model.py...")
    
    try:
        api_key = os.environ["AI_API_KEY"]
        print("API_KEY encontrada!")
    except KeyError:
        print("Error: AI_API_KEY environment variable not set.")
        sys.exit(1)

    diff_content = os.environ.get("PR_DIFF", "")
    print(f"Diff content length: {len(diff_content)} characters")

    if not diff_content.strip():
        print("No changes detected in the pull request.")
        sys.exit(0)

    system_prompt = """
    Contexto: Você é um Engenheiro de Qualidade de Software (QA) Sênior e um especialista em testes unitários.
    Tarefa: Analise o 'git diff' de um Pull Request e forneça uma análise técnica focada em testes.
    
    Formato de Resposta (em Markdown):
    **Resumo da Mudança:**
    (Descreva brevemente a lógica principal que foi alterada ou adicionada.)
    
    **Pontos de Atenção e Riscos:**
    (Identifique lógicas complexas, potenciais 'breaking changes' ou código sem tratamento de erros.)
    
    **Sugestões de Testes Unitários:**
    (Liste casos de borda (edge cases) e cenários de teste que precisam ser cobertos para o arquivo `testes_agente.py`.)
    """

    user_prompt = f"--- Git diff do Pull Request ---\n{diff_content}\n--- Fim do diff ---"
   
    #chamar API Groq
    try:
        print("Tentando importar e inicializar cliente Groq...")
        client = Groq(api_key=api_key)
        
        print("Fazendo chamada para a API...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-8b-8192", # Exemplo de modelo
        )
        
        # Imprimir a resposta da IA
        response = chat_completion.choices[0].message.content
        print("=== RESPOSTA DA IA ===")
        print(response)
        
    except ImportError as e:
        print(f"Erro ao importar biblioteca groq: {e}")
        print("Verifique se 'groq' está listado no requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao chamar a API Groq: {e}")
        print(f"Tipo do erro: {type(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()