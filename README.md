# Agente Industrial Inteligente

Este projeto é um assistente conversacional inteligente desenvolvido em Python, capaz de interpretar perguntas em linguagem natural sobre ordens de manutenção, técnicos e equipamentos de uma planta industrial fictícia.

O agente utiliza spaCy para Processamento de Linguagem Natural (NLP) e executa consultas SQL em um banco de dados SQLite.

Você pode interagir com ele por linha de comando (notebook ou script) ou via interface web construída com Streamlit.

## Funcionalidades

- **Interpretação de Linguagem Natural**: Converte perguntas em português para consultas SQL
- **Memória de Contexto**: Mantém informações da conversa para perguntas encadeadas
- **Múltiplas Interfaces**: Notebook, linha de comando e interface web
- **Consultas Complexas**: Suporte a joins entre tabelas
- **Respostas Amigáveis**: Formata resultados de forma compreensível

## Como Executar

### Pré-requisitos

1. **Python 3.8 ou superior**
   ```bash
   python --version
   # Deve mostrar Python 3.8.x ou superior
   ```

2. **Banco de dados `manutencao_industrial.db`**
   - Certifique-se de que o arquivo está na raiz do projeto
   - Se não existir, execute: `python schema_db.py`

### Instalação das Dependências

1. **Clone ou baixe o projeto**
   ```bash
   git clone <url-do-repositorio>
   cd fiesc
   ```

2. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Baixe o modelo spaCy em português**
   ```bash
   python -m spacy download pt_core_news_sm
   ```

4. **Verifique a instalação**
   ```bash
   python -c "import spacy; nlp = spacy.load('pt_core_news_sm'); print('✅ spaCy instalado com sucesso!')"
   ```

### Modos de Execução

#### 1. Interface Web (Recomendado para uso interativo)

**Passo a passo:**
1. Abra o terminal na pasta do projeto
2. Execute o comando:
   ```bash
   streamlit run app.py
   ```
3. Aguarde a mensagem: "You can now view your Streamlit app in your browser"
4. Abra seu navegador e acesse: `http://localhost:8501`
5. Digite suas perguntas no campo de texto e clique em "Enviar"

**Exemplo de uso:**
- Digite: "Me liste todos os técnicos"
- Clique em "Enviar"
- Veja a resposta formatada na interface

#### 2. Notebook (Google Colab - Recomendado para desenvolvimento)

**Passo a passo:**
1. Acesse [Google Colab](https://colab.research.google.com/)
2. Faça upload do arquivo `agente_industrial.ipynb`
3. Execute a primeira célula para instalar dependências:
   ```python
   !pip install -U spacy
   !python -m spacy download pt_core_news_sm
   ```
4. Execute a segunda célula para fazer upload do banco de dados:
   ```python
   from google.colab import files
   uploaded = files.upload()
   ```
5. Selecione o arquivo `manutencao_industrial.db` quando solicitado
6. Execute as células restantes do notebook
7. Interaja com o agente digitando perguntas no campo de entrada

**Vantagens do Colab:**
- Não precisa instalar nada localmente
- Interface familiar para desenvolvedores
- Fácil compartilhamento e colaboração

#### 3. Linha de Comando (Para testes automatizados)

**Passo a passo:**
1. Abra o terminal na pasta do projeto
2. Execute:
   ```bash
   python testes_agente.py
   ```
3. Observe os resultados dos testes no terminal
4. O script executará automaticamente várias perguntas de exemplo

**Saída esperada:**
```
Iniciando execução dos testes...

1. Pergunta: Qual técnico trabalhou na ordem 32?
Resposta: O técnico foi João Silva (especialidade: Mecânica, turno: Manhã).

2. Pergunta: Qual a especialidade dele?
Resposta: A especialidade do último técnico foi Mecânica.
```

#### 4. Script Python Direto (Para desenvolvimento)

**Passo a passo:**
1. Abra o terminal na pasta do projeto
2. Execute:
   ```bash
   python agente.py
   ```
3. Interaja diretamente com o agente via linha de comando
4. Digite suas perguntas e pressione Enter
5. Para sair, digite "sair" ou "exit"

### Solução de Problemas Comuns

#### Erro: "spacy not found"
```bash
pip install spacy
python -m spacy download pt_core_news_sm
```

#### Erro: "streamlit not found"
```bash
pip install streamlit
```

#### Erro: "database not found"
```bash
python schema_db.py
```

#### Erro: "pt_core_news_sm not found"
```bash
python -m spacy download pt_core_news_sm --force
```

#### Erro de permissão no Windows
Execute o PowerShell como administrador:
```powershell
Set-ExecutionPolicy RemoteSigned
```

## Exemplos de Perguntas

### Perguntas com Contexto
- "Qual técnico trabalhou na ordem 32?"
- "Qual a especialidade dele?"
- "Qual o turno do técnico?"
- "Qual é mesmo o técnico?"
- "Qual o equipamento da ordem?"
- "E o status do equipamento?"

### Perguntas sobre Múltiplas Tabelas
- "Quais os tipos de equipamentos que tiveram manutenção nos últimos 3 meses?"
- "Qual o nome do técnico que trabalhou em mais ordens de manutenção?"
- "Quem foi o técnico que trabalhou na ordem 1?"
- "Qual a especialidade do técnico da ordem 2?"

### Perguntas Básicas
- "Me liste todos os técnicos."
- "Quais equipamentos estão cadastrados?"
- "Quais ordens estão abertas?"
- "Quantas ordens de manutenção estão em andamento?"
- "Qual o status do equipamento 3?"
- "Qual o histórico de manutenções do equipamento 2?"
- "Qual a data de abertura da ordem 4?"

## Estrutura do Projeto

```
fiesc/
├── agente_industrial.ipynb    # Notebook principal a ser executado com Google Colab
├── app.py                     # Interface web (Streamlit)
├── agente.py                  # Lógica do agente
├── testes_agente.py           # Testes automatizados
├── manutencao_industrial.db   # Banco de dados SQLite
└── requirements.txt           # Dependências
```

## Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **spaCy**: Processamento de linguagem natural
- **SQLite**: Banco de dados local
- **Streamlit**: Interface web
- **Regex**: Padrões de reconhecimento de texto

## Limitações Atuais

- **Regras Simbólicas**: O agente usa padrões pré-definidos, não machine learning
- **Cobertura Limitada**: Pode não entender perguntas muito diferentes dos exemplos
- **Contexto Temporário**: Memória apenas durante a sessão atual
- **Validação Básica**: Verificação simples de IDs e dados

## Melhorias Futuras

- Integração com modelos de linguagem avançados (GPT, BERT)
- Expansão da cobertura de intenções e tipos de perguntas
- Interface web mais robusta com histórico persistente
- Autenticação e controle de acesso
- Suporte a múltiplos bancos de dados
- Análise preditiva de manutenção









