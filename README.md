# Trabalho Final: Tutor Inteligente Multiagente com LLM Local

## 👥 Elementos do Grupo
* Maria Vitória Kuhn - 197960

## 📝 Descrição do Problema
O projeto resolve o problema de apoio ao estudo autónomo de estudantes de programação. Muitas vezes, os alunos enfrentam dificuldades fora do horário de aulas e os chatbots genéricos tendem a alucinar ou a fornecer códigos complexos demais. O **Tutor Inteligente** utiliza materiais pedagógicos oficiais da instituição para responder de forma focada, didática e sem custos de API.

## 🏗️ Arquitetura do Sistema e Papéis dos Agentes
O sistema foi desenhado utilizando uma arquitetura de múltiplos agentes especializados que cooperam de forma sequencial:

1. **Agente Recuperador (Especialista em Dados):** Atua como o componente de RAG. Tem como responsabilidade ler a base de dados vetorial, realizar a busca semântica baseada na intenção do utilizador e filtrar o contexto mais relevante.
2. **Agente Professor (Especialista em Síntese):** Utiliza um modelo de linguagem de grande escala (LLM) local para processar a dúvida combinada com o contexto recuperado, gerando uma resposta altamente didática adaptada ao nível do estudante.

## 🛠️ Tecnologias Utilizadas, RAG e MCP
* **Modelo de Linguagem Local:** Ollama executando o modelo `llama3.2` de forma 100% offline.
* **Banco de Dados Vetorial & Embeddings:** `ChromaDB` para indexação de documentos e pesquisa por similaridade semântica.
* **Mecanismo de RAG:** Implementado através da segmentação do ficheiro `aula1.txt` em chunks armazenados no ChromaDB, recuperados dinamicamente com base na proximidade vetorial da dúvida.
* **Conceito de Tools e MCP:** O Agente Recuperador expõe a sua capacidade de busca ao ecossistema em formato de ferramenta isolada (Tool Use), simulando a padronização proposta pelo *Model Context Protocol* para acesso seguro a recursos de armazenamento locais.

## 🚀 Instruções de Instalação e Execução

### Pré-requisitos
1. Ter o Python 3.10 ou superior instalado.
2. Instalar o [Ollama](https://ollama.com/) e descarregar o modelo executando no terminal:
   ```bash
   ollama run llama3.2