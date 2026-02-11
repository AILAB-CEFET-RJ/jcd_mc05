# Anatomia do Agente no LangChain

No trecho abaixo, estamos criando um orquestrador. Ele recebe um objetivo, avalia quais ferramentas tem à disposição lendo suas descrições e inicia um ciclo de raciocínio e ação até encontrar a resposta final.

```python
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

O comando `initialize_agent` transforma um modelo de linguagem estático em um **agente dinâmico**.  
Ele configura o "cérebro" para saber quando parar de apenas responder texto e começar a agir com ferramentas.

## Abrindo a caixa do `initialize_agent`

Quando a função  `initialize_agent(...)` é invocada, o LangChain monta um pipeline interno.  
O ponto principal é que existe  um **prompt de sistema/instrução** por trás, com regras de formato para o padrão ReAct.

Em termos práticos, o que a função faz:

1. Monta um prompt-base do agente com instruções de comportamento.
2. Injeta no prompt a lista de tools (`name` + `description`).
3. Define o formato esperado de resposta do modelo (por exemplo: `Thought`, `Action`, `Action Input`, `Observation`, `Final Answer`).
4. Cria um parser para ler a saída do modelo e decidir:
   - se ele pediu uma tool (`Action`)
   - ou se terminou (`Final Answer`).
5. Executa um loop:
   - LLM raciocina
   - chama tool
   - recebe observação
   - adiciona ao histórico interno (scratchpad)
   - repete até resposta final.

### Prompt interno (visão didática)

O texto exato pode variar por versão, mas o esqueleto é equivalente a isto:

```text
You are an agent that can use the following tools:
- ToolA: <description>
- ToolB: <description>

Use this format:
Question: ...
Thought: ...
Action: one of [ToolA, ToolB]
Action Input: ...
Observation: ...
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: ...
```

Por isso `description` é tão importante: ela vira parte do prompt e orienta a decisão do agente sobre **quando** e **qual** ferramenta usar.

### Estrutura do scratchpad (`intermediate_steps`)

No agente clássico, o "histórico interno" costuma ser representado por `intermediate_steps`.

Conceitualmente, ele é uma lista de pares:

```text
[
  (AgentAction, observation),
  (AgentAction, observation),
  ...
]
```

Cada `AgentAction` carrega, em geral:

- `tool`: nome da ferramenta escolhida.
- `tool_input`: entrada passada para a ferramenta.
- `log`: trecho textual com o passo de raciocínio/ação.

Esse conteúdo é convertido para o formato textual ReAct e reinjetado no prompt a cada iteração (`Thought/Action/Action Input/Observation`), até o `Final Answer`.

## 1. `tools` (As Ferramentas)

**O que é:** Uma lista de funções que o agente pode executar.

**Explicação para o curso:**  
Imagine que o LLM é um consultor. As `tools` são os aplicativos instalados no celular dele (calculadora, busca na web, acesso ao banco de dados).  
Sem essas ferramentas, o agente só pode usar o que aprendeu no treinamento, ou seja, informação estática e potencialmente desatualizada.

## 2. `llm` (O Cérebro)

**O que é:** O modelo de linguagem (por exemplo, GPT-4 ou Llama 3) que toma decisões durante a execução.

**Explicação para o curso:**  
É o componente que interpreta o pedido do usuário, decide qual ferramenta usar e analisa os resultados retornados por cada ferramenta.

## 3. `agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION` (A Lógica)

Este é o ponto central para explicar o padrão **ReAct**.

- **Zero-Shot:** o agente não precisa de exemplos prévios de uso das ferramentas; ele decide na hora usando a descrição de cada tool.
- **ReAct:** acrônimo de **Reason + Act** (Raciocinar + Agir).
- **Description:** o agente escolhe a ferramenta com base no campo `description` definido em cada tool.

**Importante:** se a descrição da ferramenta for ruim, o agente tende a escolher mal (ou não escolher) a ferramenta certa.

## 4. `verbose=True` (A Caixa Preta Aberta)

**O que é:** Modo de depuração.

**Explicação para o curso:**  
É essencial para ensino, pois exibe o loop interno do agente no terminal:

- **Thought (Pensamento):** "Preciso saber o gasto de pessoal."
- **Action (Ação):** "Vou usar a ferramenta `PayrollQuery`."
- **Observation (Observação):** "A ferramenta retornou `$142,500`."

Com isso, os alunos visualizam claramente como o agente decide, executa e integra resultados.

## Relacionando com `tool-calling/demo_langchain_react.py`

No arquivo `tool-calling/demo_langchain_react.py`, é possível mapear os conceitos aqui descritos da seguinte forma:

- `tools=[...]`: define o conjunto de ações disponíveis para o agente.
- `llm = ChatOpenAI(...)`: define o modelo que orquestra as decisões.
- `agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION`: ativa o padrão ReAct clássico.
- `verbose=True`: exibe o ciclo de raciocínio e ação durante a execução.
