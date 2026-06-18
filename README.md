**AVISO:** Existem alguns commits feitos por outras pessoas, a explicação é  que eu estava usando um pc da faculdade e não notei que as credencias eram outras.

# Trabalho Final: Tutor Inteligente Multiagente com LLM Local

## 👥 Integrantes do Grupo
* Maria Vitória Kuhn - 197960 (Fiz o trabalho sozinha)

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

## Justificativa da Arquitetura Multiagente

A escolha por uma arquitetura multiagente se justifica pela necessidade de especialização e eficiência no ecossistema do tutor inteligente, superando as limitações de uma abordagem com agente único (single-agent). Dividir o sistema em papéis claros traz dois ganhos principais: otimização de recursos (tokens/tempo) e separação de preocupações (Separation of Concerns).

Enquanto um único agente agiria de forma generalista e sobrecarregada, o Planejador atua como um roteador determinístico ágil, direcionando o fluxo e evitando o desperdício de tokens com buscas desnecessárias no banco vetorial (RAG) quando o aluno solicita apenas uma avaliação. Por sua vez, o Professor e o Avaliador focam estritamente na lógica pedagógica e no consumo de contexto, deixando a validação sintática e conceitual a cargo do Revisor, que funciona como uma camada isolada de controle de qualidade. Essa cooperação distribuída garante maior robustez ao modelo local (llama3.2), minimiza alucinações e eleva a precisão técnica das respostas entregues ao estudante.

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

## Exemplo de sessão (transcrição)

Exemplo de uma sessão típica no terminal:

Aluno: O que é uma lista em Python?

🧠 INICIANDO FLUXO MULTIAGENTE

📋 [Planejador] Fluxo escolhido: DUVIDA
🎓 [Planejador] Encaminhando para Professor

🎓 [Professor] Analisando pergunta...
🛠️ [Professor] Decidiu usar uma Tool
🔍 [Professor] Buscando contexto para: O que é uma lista em Python?
📚 [Professor] Contexto recuperado
✅ [Professor] Resposta gerada
🔎 [Revisor] Revisando resposta...
✅ [Revisor] Revisão concluída

📚 RESPOSTA FINAL

Uma lista em Python é um tipo de sequência mutável, que armazena valores de forma ordenada. As listas são representadas por `[ ]` e permitem a inclusão de elementos individuais. No Python, as listas também suportam operações como inserção, exclusão e permutação de elementos.

---

Aluno: Quero um teste sobre listas

🧠 INICIANDO FLUXO MULTIAGENTE

📋 [Planejador] Fluxo escolhido: AVALIACAO
📝 [Planejador] Encaminhando para Avaliador

[Avaliador] Gerando exercício...

Segue aqui a questão de múltipla escolha sobre listas em Python:

Qual é o propósito de uma lista em Python?

A) Armazenar apenas valores numéricos
B) Repetir código para execução automática
C) Criar um conjunto de dados que pode ser acessado por índice ou chave
D) Encerrar programas

Digite apenas a letra da resposta.
---

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

---

## Reflexão Crítica sobre o Projeto

O desenvolvimento deste Tutor Inteligente proporcionou um aprendizado profundo sobre os desafios reais da implementação de sistemas baseados em LLMs locais. Abaixo, destaquei os principais pontos de reflexão estruturados ao longo do projeto:

1. **Engenharia de Prompt para Modelos Locais (LLaMA 3.2):**
Um dos maiores desafios foi lidar com a tendência de modelos menores à alucinação e à "desobediência" de restrições rígidas. Observamos que o modelo, por vezes, trazia conhecimentos prévios errôneos (como inverter a mutabilidade de listas e tuplas em Python) ou ignorava a instrução de usar apenas o contexto do RAG. A solução exigiu uma arquitetura de prompts muito mais rigorosa, separando claramente o papel do sistema (`system`) da entrada do usuário (`user`), e impondo o uso de delimitadores explícitos (`[CONTEXTO]`, `[REGRAS]`).
2. **O Papel Essencial da Arquitetura Multiagente:**
Inicialmente, pensar em múltiplos agentes para um problema de "Perguntas e Respostas" pode parecer excessivo, mas na prática, a divisão de responsabilidades provou-se indispensável. Ao isolar a validação sintática no agente **Revisor**, evitamos sobrecarregar o **Professor** com regras gramaticais. Da mesma forma, o **Planejador** atua como um "escudo", poupando o custo computacional (e o tempo de inferência) de buscar informações no banco vetorial quando o aluno quer apenas gerar um exercício (acionando o **Avaliador**). Isso tornou o sistema significativamente mais ágil.


3. **Trade-offs de uma Solução 100% Local e Offline:**
A exigência de rodar localmente  revelou o balanço entre privacidade/independência e infraestrutura. Por um lado, o sistema garante total privacidade dos dados do aluno e funciona sem custos de API ou dependência de internet. Por outro lado, a latência de geração de respostas e a qualidade do *reasoning* (raciocínio) são diretamente limitadas pelo hardware da máquina onde o Ollama é executado. A implementação do *fallback textual* para o caso de falha do banco vetorial Chroma foi uma medida necessária para garantir a resiliência do software.


4. **Padronização com MCP:**
A adoção do *Model Context Protocol* (MCP) adicionou uma camada de complexidade inicial à arquitetura, exigindo a formatação de contratos estritos de entrada e saída. Contudo, essa abstração garantiu que a ferramenta de busca (`buscar_material`) se tornasse agnóstica ao agente que a chama, facilitando futuras expansões do sistema sem a necessidade de reescrever a lógica de integração.



