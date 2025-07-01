# Agente Industrial Inteligente

Este projeto é um assistente conversacional inteligente desenvolvido em Python, capaz de interpretar perguntas em linguagem natural sobre ordens de manutenção, técnicos e equipamentos de uma planta industrial fictícia.

O agente utiliza spaCy para Processamento de Linguagem Natural (NLP) e executa consultas SQL em um banco de dados SQLite.

Você pode interagir com ele por linha de comando, notebook no Google Colab ou interface web construída com Streamlit.

---

## Funcionalidades

- **Interpretação de Linguagem Natural:** converte perguntas em português para consultas SQL.
- **Memória de Contexto:** mantém informações da conversa para perguntas encadeadas.
- **Múltiplas Interfaces:** notebook, linha de comando e interface web.
- **Consultas Complexas:** suporte a joins entre tabelas.
- **Respostas Amigáveis:** formata resultados de forma compreensível.

---

## Como Executar

### Pré-requisitos

**Python 3.8 ou superior**

```bash
python --version
# Deve mostrar Python 3.8.x ou superior
```

**Banco de dados `manutencao_industrial.db`**

Certifique-se de que o arquivo está na raiz do projeto.

### Instalação das Dependências

Clone o projeto:

```bash
git clone https://github.com/luciano-coelho/fiesc.git
cd fiesc
```

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

Baixe o modelo spaCy em português:

```bash
python -m spacy download pt_core_news_sm
```

Verifique a instalação:

```bash
python -c "import spacy; nlp = spacy.load('pt_core_news_sm'); print('spaCy instalado com sucesso!')"
```

Execute os testes automáticos:

```bash
python testes_agente.py
```

---

Se tudo estiver funcionando, você verá as perguntas de teste respondidas automaticamente no terminal.

## Modos de Execução

### 1. Executar no Google Colab

Passo a passo:

1. Acesse: https://colab.research.google.com/
2. Clique em **"Abrir notebook" (ou Open notebook)**
3. No menu lateral, selecione **GitHub**
4. No campo de busca, insira:

```
https://github.com/luciano-coelho/fiesc
```

5. Aguarde carregar a lista de arquivos
6. Clique em `agente_industrial.ipynb`
7. Abra o notebook.
8. Clique em **Executar tudo (Runtime > Run all)**

O notebook irá:

- Instalar todas as dependências automaticamente.
- Configurar o ambiente.
- Executar os testes automatizados.
- Abrir o chat interativo pronto para uso.

---

### 2. Interface Web (Streamlit)

Passo a passo completo:

```bash
git clone https://github.com/luciano-coelho/fiesc.git
cd fiesc
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python -m streamlit run app.py
```

Após executar, aparecerá no terminal:

```
Local URL: http://localhost:8501
```

Abra este endereço no navegador para usar o chat.

---

### 3. Linha de Comando (Testes Automatizados)

Passo a passo:

```bash
python testes_agente.py
```

O script executará automaticamente exemplos de perguntas e exibirá as respostas.

---

## Solução de Problemas Comuns

**Erro:** `spacy not found`
```bash
pip install spacy
python -m spacy download pt_core_news_sm
```

**Erro:** `streamlit not found`
```bash
pip install streamlit
```
## Exemplos de Perguntas

### Perguntas com Contexto

- Qual técnico trabalhou na ordem 32?
- Qual a especialidade dele?
- Qual o turno do técnico?
- Qual é mesmo o técnico?
- Qual o equipamento da ordem?
- E o status do equipamento?

### Perguntas sobre Múltiplas Tabelas

- Quais os tipos de equipamentos que tiveram manutenção nos últimos 3 meses?
- Qual o nome do técnico que trabalhou em mais ordens de manutenção?
- Quem foi o técnico que trabalhou na ordem 1?
- Qual a especialidade do técnico da ordem 2?
- Me liste todos os técnicos.
- Quais equipamentos estão cadastrados?
- Quais ordens estão abertas?
- Quantas ordens de manutenção estão em andamento?
- Qual o status do equipamento 3?
- Qual o histórico de manutenções do equipamento 2?
- Qual a data de abertura da ordem 4?

---

## Estrutura do Projeto

```
fiesc/
├── agente_industrial.ipynb    # Notebook pronto para Colab
├── app.py                     # Interface web (Streamlit)
├── agente.py                  # Lógica principal
├── testes_agente.py           # Testes automatizados
├── manutencao_industrial.db   # Banco de dados SQLite
├── Fluxo da solução.pdf       # Documento com diagrama do fluxo da solução
└── requirements.txt           # Dependências

```

---

## Tecnologias Utilizadas

- Python 3.8+
- spaCy
- SQLite
- Streamlit
- Regex

---

## Limitações Atuais

- Regras simbólicas (não usa machine learning)
- Cobertura limitada de padrões
- Memória de contexto apenas durante a sessão
- Validação básica dos dados

---

## Melhorias Futuras

- Integração com modelos de linguagem avançados (GPT, BERT)
- Expansão da cobertura de perguntas e intenções
- Interface web mais robusta
- Persistência de contexto entre sessões
- Suporte a múltiplos bancos de dados
- Análise preditiva de manutenção
