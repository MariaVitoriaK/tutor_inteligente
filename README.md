# Trabalho Final: Tutor Inteligente Multiagente com LLM Local

## 👥 Elementos do Grupo
* Maria Vitória Kuhn - 197960

## Descrição do Problema
Estudantes de programação frequentemente encontram dificuldades ao estudar fora do horário de aula e nem sempre possuem acesso imediato a professores ou monitores.

Além disso, assistentes genéricos podem gerar respostas incorretas, excessivamente avançadas ou desconectadas do conteúdo efetivamente trabalhado na disciplina.

O projeto Tutor Inteligente Multiagente foi desenvolvido para fornecer suporte educacional baseado em materiais didáticos previamente disponibilizados, utilizando modelos de linguagem locais, recuperação de contexto (RAG) e múltiplos agentes especializados.

A solução permite que os alunos realizem perguntas em linguagem natural através do terminal e recebam respostas contextualizadas com base no conteúdo das aulas cadastradas.

## Objetivo da Solução

Desenvolver um sistema multiagente capaz de:

- auxiliar estudantes no aprendizado de Python;
- responder dúvidas utilizando materiais didáticos locais;
- gerar exercícios de fixação;
- utilizar recuperação semântica de contexto;
- operar totalmente offline através de modelos locais;
- demonstrar integração entre agentes, tools, MCP, RAG e banco vetorial.

## Arquitetura do Sistema e Papéis dos Agentes
O sistema utiliza uma arquitetura baseada em agentes especializados que cooperam entre si para resolver as solicitações do usuário.

1. **Agente Planejador:** Responsável por analisar a solicitação do usuário e decidir qual fluxo deve ser executado.
2. **Agente Professor:** Responsável pela geração das respostas.
3. **Agente Recuperador:** Responsável pela recuperação de contexto.
4. **Agente Avaliador:** Responsável pela geração e correção de exercícios.
5. **Agente Revisor:** Responsável pela validação final da resposta.

## Tecnologias Utilizadas
* **Modelo de Linguagem Local:** Ollama executando o modelo `llama3.2` de forma 100% offline.
* **Banco de Dados Vetorial & Embeddings:** `ChromaDB` para indexação de documentos e pesquisa por similaridade semântica.
* **Mecanismo de RAG:** Implementado através da segmentação do ficheiro `aula1.txt` em chunks armazenados no ChromaDB, recuperados dinamicamente com base na proximidade vetorial da dúvida.
* **Conceito de Tools e MCP:** O Agente Recuperador expõe a sua capacidade de busca ao ecossistema em formato de ferramenta isolada (Tool Use), simulando a padronização proposta pelo *Model Context Protocol* para acesso seguro a recursos de armazenamento locais.

## Instruções de Instalação e Execução

### Pré-requisitos
1. Clonar o projeto - git clone https://github.com/MariaVitoriaK/tutor_inteligente.git
2. Ter o Python 3.10 ou superior instalado.
3. Instalar dependências - pip install -r requirements.txt
4. Instalar Ollama - https://ollama.com
5. Baixar modelo - ollama pull llama3.2
6. Gerar a base vetorial - python src/rag/ingestao.py
7. Executar o sistema - python src/main.py