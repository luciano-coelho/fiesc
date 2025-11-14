import os
import sys

def main():
    print("Iniciando script call_ai_model.py...")
    
    # Primeiro, verificar se consegue importar o Groq
    try:
        print("Tentando importar biblioteca groq...")
        from groq import Groq
        print("Biblioteca groq importada com sucesso!")
    except ImportError as e:
        print(f"ERRO: Não foi possível importar groq: {e}")
        sys.exit(1)
    
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
        print("Iniciando cliente Groq...")
        client = Groq(api_key=api_key)
        print("Cliente Groq criado com sucesso!")
        
        print("Preparando mensagens para a API...")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        print(f"Enviando {len(messages)} mensagens para a API...")
        
        print("Fazendo chamada para a API...")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )
        print("Chamada da API bem-sucedida!")
        
        # Imprimir a resposta da IA
        response = chat_completion.choices[0].message.content
        print("=== RESPOSTA DA IA ===")
        print(response)
        
    except Exception as e:
        print(f"ERRO ao chamar a API Groq: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        
        # Fallback - análise simples sem IA
        print("=== FALLBACK: ANÁLISE BÁSICA ===")
        fallback_response = f"""
**Resumo da Mudança:**
Foram detectadas alterações no arquivo de workflow `.github/workflows/ai_pr_review.yml`.

**Pontos de Atenção e Riscos:**
- Mudanças em workflows de CI/CD podem afetar o processo de deployment
- Verificar se as dependências estão corretas no requirements.txt

**Sugestões de Testes Unitários:**
- Testar se o workflow executa sem erros
- Verificar se todas as dependências estão instaladas
- Validar se as variáveis de ambiente estão configuradas

**Diff analisado:**
```
{diff_content[:500]}...
```
        """
        print(fallback_response)
        # Não fazer sys.exit(1) para permitir que o comentário seja postado

if __name__ == "__main__":
    main()