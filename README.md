# Trabalho Final: Tutor Inteligente Multiagente com LLM Local

## 👥 Integrantes do Grupo
* Maria Vitória Kuhn - 197960

## Descrição do Problema
Estudantes de programação enfrentam dificuldades ao estudar fora do horário de aula:
- dúvidas sem resposta imediata;
- ausência de material explicativo contextualizado;
- respostas genéricas ou fora do nível da disciplina.

Este projeto entrega um tutor inteligente que responde dúvidas de Python usando apenas conteúdos didáticos locais, com um fluxo multiagente coordenado e suporte a recuperação de contexto.

## Visão Geral da Solução
O Tutor Inteligente é um sistema offline que combina:
- interação por terminal em linguagem natural;
- multiagentes com responsabilidades claras;
- recuperação de contexto local por similaridade (RAG);
- um banco vetorial persistente para documentos didáticos;
- geração de exercícios e correção orientadas por contexto.

## O que mudou nesta versão
- `src/rag/banco_vetorial.py` foi implementado para usar `chromadb.PersistentClient`.
- O sistema agora cria uma coleção Chroma persistente em `bd_vetorial/`.
- `src/rag/ingestao.py` foi tornado mais robusto para importar corretamente o repositório e detectar se a base já existe.
- `src/agentes/avaliador.py` agora recupera contexto automaticamente antes de gerar exercícios, evitando respostas vazias.
- Foi adicionado um fallback textual simples quando o banco vetorial estiver vazio ou não responder.

## Arquitetura e Papéis dos Agentes
A aplicação está organizada em agentes com responsabilidades separadas:

1. **Planejador** (`src/agentes/planejador.py`)
   - Analisa a pergunta do aluno.
   - Decide entre fluxo de dúvida ou fluxo de avaliação.

2. **Professor** (`src/agentes/professor.py`)
   - Recebe a pergunta do aluno.
   - Tenta chamar a tool de busca de material para acessar o contexto.
   - Se o contexto for recuperado, responde com base nele; caso contrário, responde diretamente.

3. **Recuperador** (`src/agentes/recuperador.py` + `src/mcp/tools.py`)
   - Consulta o banco vetorial para retornar trechos relevantes.
   - Expõe essa lógica como uma tool usada pelo `Professor`.

4. **Avaliador** (`src/agentes/avaliador.py`)
   - Gera questões de múltipla escolha com base no tema e no contexto.
   - Busca contexto se este não for fornecido explicitamente.
   - Possui também função de correção de respostas do aluno.

5. **Revisor** (`src/agentes/revisor.py`)
   - Verifica clareza e gramática da resposta final.
   - Não altera conceitos nem adiciona conteúdo.

## Estrutura do Repositório
- `README.md` — documentação do projeto.
- `requirements.txt` — dependências do Python.
- `data/` — conteúdos didáticos em `.txt`.
- `bd_vetorial/` — banco vetorial persistente gerado pelo Chroma.
- `src/main.py` — ponto de entrada do sistema.
- `src/agentes/` — implementação dos agentes.
- `src/mcp/` — definições de ferramenta e esquema MCP.
- `src/rag/` — ingestão e busca de contexto vetorial.

## Funcionamento do Banco Vetorial
O banco usa `chromadb.PersistentClient` para manter a coleção de documentos entre execuções.

- A base é criada em `bd_vetorial/`.
- Os arquivos `*.txt` dentro de `data/` são divididos em chunks com `RecursiveCharacterTextSplitter`.
- Cada chunk é indexado como documento no Chroma.
- A consulta utiliza o texto da pergunta para recuperar os trechos mais relevantes.
- Se o Chroma não estiver inicializado ou estiver vazio, o sistema cai para um fallback básico de busca textual.

## Ingestão de Dados
Execute:

```bash
python src/rag/ingestao.py
```

Esse script:
- lê todos os arquivos `.txt` em `data/`;
- divide os textos em blocos de até 500 caracteres com 100 de sobreposição;
- adiciona os conteúdos à coleção `documentos` do Chroma.

Se a coleção já existir, ela não será recriada.

## Requisitos e Instalação
### Pré-requisitos
- Python 3.10 ou superior
- Ollama instalado e em funcionamento
- Modelo local `llama3.2` disponível via Ollama

### Instalação
```bash
pip install -r requirements.txt
```

### Preparar o modelo local
```bash
ollama pull llama3.2
```

### Gerar a base vetorial
```bash
python src/rag/ingestao.py
```

### Executar o tutor
```bash
python src/main.py
```

## Uso
- Digite sua pergunta no terminal.
- Para encerrar, digite `sair`.
- Perguntas que contenham termos como `teste`, `quiz`, `exercício`, `avaliar` ou `prova` acionam o fluxo de avaliação.
- Outras perguntas seguem o fluxo de dúvida e consultam o contexto disponível.

## Observações
- O sistema foi desenhado para operar 100% offline, desde que o modelo local esteja instalado.
- A recuperação de contexto depende da base vetorial; se ela não estiver disponível, o tutor usa um fallback de busca textual.
- O revisor é um passo de controle de qualidade, mas não altera o conteúdo original da resposta.

## Possíveis melhorias futuras
- adicionar testes automatizados para cada agente;
- incluir suporte a mais formatos de conteúdo (PDF, Markdown);
- tornar o fluxo de correção interativo com o aluno;
- melhorar o fallback de busca para usar embeddings offline sem Ollama.
