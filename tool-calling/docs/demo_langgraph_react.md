# Anatomia do Agente no LangGraph/LangChain (`create_agent`)

No trecho abaixo, estamos criando um orquestrador no estilo ReAct, mas com a API mais nova:

```python
agent = create_agent(
    model=llm,
    tools=[get_current_date, payroll_query],
    system_prompt=system_prompt,
)
```

Nesta linha, estamos criando um orquestrador. Ele recebe um objetivo, avalia quais ferramentas tem a disposicao lendo suas descricoes e inicia um ciclo de raciocinio e acao ate encontrar a resposta final.

## Abrindo a caixa do `create_agent`

Quando `create_agent(...)` e chamado, a biblioteca monta um fluxo interno orientado a mensagens:

1. Registra o modelo (`model`) que tomara as decisoes.
2. Registra as ferramentas (`tools`) com nome, descricao e assinatura.
3. Aplica instrucoes globais via `system_prompt`.
4. Inicia um loop ReAct de planejamento e chamada de ferramentas.
5. Mantem o historico em `messages` e retorna o estado final.

Em resumo: a ideia e a mesma do agente classico, mas o contrato principal de entrada/saida e baseado em mensagens.

### Equivalente ao scratchpad no modelo novo

No fluxo com `create_agent`, o equivalente ao scratchpad aparece no estado de `messages`.

Em termos didaticos, voce tende a ver uma sequencia com:

- mensagem do usuario;
- mensagem do assistente com chamada de tool;
- retorno da tool;
- nova mensagem do assistente (com nova chamada ou resposta final).

Ou seja, no lugar de um bloco textual unico (scratchpad), o historico fica estruturado como eventos de mensagem/tool ao longo do fluxo.

## Prompt interno (visao didatica)

O texto exato varia por versao e provedor, mas conceitualmente o agente recebe instrucoes equivalentes a:

```text
You are an assistant with access to tools.
Follow the system instructions.
If needed, call a tool with valid arguments.
Use tool results to produce the final answer.
```

No exemplo `tool-calling/demo_langgraph_react.py`, o `system_prompt` reforca uma regra importante:

- para datas relativas (ex.: "last month"), chamar `CurrentDate` antes de `PayrollQuery`.

## 1. `tools` (As Ferramentas)

**O que e:** Funcoes decoradas com `@tool`.

**No exemplo:**

- `CurrentDate`: devolve a data atual.
- `PayrollQuery`: retorna o valor da folha para `department` e `month` explicitos.

**Ponto didatico:** a descricao da tool e parte da orientacao do agente. Descricao ruim reduz qualidade da decisao.

## 2. `model` (O Cerebro)

**O que e:** O LLM que decide quando responder diretamente e quando chamar tools.

**No exemplo:** `ChatOpenAI(model="gpt-4", temperature=0)`.

## 3. `system_prompt` (Regras Globais)

**O que e:** Instrucoes de alto nivel que governam o comportamento do agente durante toda a execucao.

**No exemplo:** obriga o uso de `CurrentDate` antes de consultar `PayrollQuery` para datas relativas.

## 4. `agent.invoke(...)` com `messages`

No fluxo atual, a chamada principal usa mensagens:

```python
result = agent.invoke({"messages": [("user", query)]})
```

E a resposta final pode ser lida da ultima mensagem:

```python
final_message = result["messages"][-1]
print(final_message.content)
```

## Relacionando com `tool-calling/demo_langgraph_react.py`

No arquivo `tool-calling/demo_langgraph_react.py`, os conceitos ficam mapeados assim:

- `@tool`: define capacidades acionaveis.
- `create_agent(...)`: monta o orquestrador.
- `system_prompt`: define politica de uso das tools.
- `invoke({"messages": ...})`: executa o ciclo ate resposta final.
