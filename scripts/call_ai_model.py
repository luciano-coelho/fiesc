import os
import sys
from groq import Groq

def main():
    try:
        api_key = os.environ["AI_API_KEY"]
    except KeyError:
        print("Error: AI_API_KEY environment variable not set.")
        sys.exit(1)

    diff_content = os.environ.get("PR_DIFF", "")

    if not diff_content.strip():
        print("No changes detected in the pull request.")
        sys.exit(0)

    system_prompt = """"
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

    user_prompt = f"--- Git diff do Pull Request ---\n{diff_content}\n--- Fim do diff ---"""
   
    #chamar API Groq
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-8b-8192", # Exemplo de modelo
        )
        
        # Imprimir a resposta da IA
        response = chat_completion.choices[0].message.content
        print(response)
        
    except Exception as e:
        print(f"Erro ao chamar a API Groq: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()