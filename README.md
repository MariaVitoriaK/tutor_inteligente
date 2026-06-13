**AVISO:** Existem alguns commits feitos por outras pessoas, a explicação é  que eu estava usando um pc da faculdade e não notei que as credencias eram outras.

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
- embeddings locais para indexação semântica dos documentos;
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
- `src/rag/` — ingestão, armazenamento e recuperação de contexto via RAG.
- `src/config/` — configuração centralizada do projeto e variáveis de ambiente.
- `.env.example` — exemplo de configuração para o ambiente local.

## Funcionamento do Banco Vetorial
O projeto usa um pipeline RAG com embeddings locais e Chroma para recuperar contexto relevante durante as perguntas.

- A base é criada em `bd_vetorial/`.
- Os arquivos `*.txt` dentro de `data/` são divididos em blocos com `RecursiveCharacterTextSplitter`.
- Cada bloco é indexado no Chroma usando embeddings locais (`sentence-transformers`).
- Em tempo de execução, o agente recuperador consulta o Chroma com a pergunta do aluno e retorna os trechos mais relevantes.
- O `Professor` e o `Avaliador` usam esse contexto para gerar respostas ou criar exercícios mais precisos.
- Se o Chroma não estiver disponível, o sistema usa um fallback de busca textual direto nos arquivos.

## Ingestão de Dados
Execute:

```bash
python -m src.rag.ingestao
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
pip install langchain-text-splitters
```

### Configuração opcional com variáveis de ambiente
Copie o arquivo de exemplo `.env.example` para `.env` e ajuste os valores se necessário:

```bash
copy .env.example .env
```

O projeto carrega as configurações de modelo, embeddings e Chroma via `src/config/config.py`.

### Preparar o modelo local
```bash
ollama pull llama3.2
```

### Gerar a base vetorial
```bash
python -m src.rag.ingestao
```

### Executar o tutor
```bash
python -m src.main
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

## Testes automatizados

Este repositório agora inclui testes automatizados com `pytest` cobrindo:

- testes unitários para os agentes em `tests/`;
- um teste E2E que executa o fluxo principal (`src/main.py`) com mocks para o modelo e banco vetorial.

Como executar os testes:

1. Instale o `pytest` (recomendado em um virtualenv):

```bash
pip install pytest
```

2. Execute os testes a partir da raiz do repositório:

```bash
python -m pytest -q
```

Observações:

- Os testes usam `monkeypatch` para substituir chamadas a `ollama.chat` e ao banco vetorial, portanto
   não precisam de um modelo local nem de um Chroma ativo para rodar.
- Se desejar rodar testes que integrem o modelo real e o Chroma, execute-os manualmente após garantir
   que `ollama` e o banco vetorial estejam corretamente configurados.

## Exemplo de sessão (transcrição)

Exemplo de uma sessão típica no terminal:

Aluno: O que é uma lista em Python?

🧠 INICIANDO FLUXO MULTIAGENTE

📋 [Planejador] Fluxo escolhido: DUVIDA
🎓 [Planejador] Encaminhando para Professor

🎓 [Professor] Analisando pergunta...
📚 [Professor] Contexto recuperado
🔎 [Revisor] Revisando resposta...
✅ [Revisor] Revisão concluída

📚 RESPOSTA FINAL

Uma lista em Python é uma coleção ordenada e mutável de itens. Exemplo: [1, 2, 3].

---

Aluno: Quero um teste sobre listas

🧠 INICIANDO FLUXO MULTIAGENTE

📋 [Planejador] Fluxo escolhido: AVALIACAO
📝 [Planejador] Encaminhando para Avaliador

[Avaliador] Gerando exercício...

1) O que retorna len([1, 2, 3])?
A) 2
B) 3
C) 1
D) 0

Digite apenas a letra da resposta.

---

Observação: as respostas acima são exemplos; a saída real depende do modelo local e do conteúdo disponível na base vetorial.

## Exemplo de mensagem/contrato MCP

O projeto expõe tools MCP em `src/mcp/`. Abaixo um exemplo simplificado de como um agente pode solicitar
uma tool de busca de material seguindo o contrato definido em `src/mcp/esquemas.py`:

Exemplo de pedido (agent -> tool):

{
   "type": "tool_call",
   "tool": "buscar_material",
   "function": {
      "name": "buscar_material",
      "arguments": {"pergunta": "O que é lista em Python?"}
   }
}

Exemplo de resposta (tool -> agent):

{
   "type": "tool_response",
   "tool": "buscar_material",
   "result": {
      "documents": ["Uma lista em Python é...", "Exemplo: [1, 2, 3]"]
   }
}

No repositório, `src/mcp/esquemas.py` define a assinatura esperada (`tool_busca_material`) e `src/mcp/tools.py`
faz o roteamento para `AgenteRecuperador`.

