import os
import sys

def main():
    # Importar o Groq
    try:
        from groq import Groq
    except ImportError as e:
        print(f"ERRO: Não foi possível importar groq: {e}")
        sys.exit(1)
    
    try:
        api_key = os.environ["AI_API_KEY"]
    except KeyError:
        print("Error: AI_API_KEY environment variable not set.")
        sys.exit(1)

    diff_content = os.environ.get("PR_DIFF", "")

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
        client = Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",  # Modelo atual do Groq
        )
        
        # Imprimir a resposta da IA
        response = chat_completion.choices[0].message.content
        print(response)
        
    except Exception as e:
        # Fallback - análise simples sem IA
        fallback_response = f"""**Resumo da Mudança:**
Foram detectadas alterações nos arquivos do projeto.

**Pontos de Atenção e Riscos:**
- Verificar se as mudanças não introduziram breaking changes
- Validar se todas as dependências estão corretas

**Sugestões de Testes Unitários:**
- Adicionar testes para as novas funcionalidades
- Verificar cobertura de testes para o código alterado
- Testar cenários de edge cases

*Nota: Análise gerada automaticamente. API da IA não disponível no momento.*"""
        
        print(fallback_response)

if __name__ == "__main__":
    main()