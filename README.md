# MC05 - Large Language Models and Agents

Short Course - JCD 2026  
**Autores:** Bruno Menezes (LNCC), Eduardo Bezerra (CEFET/RJ)

## Slido

https://app.sli.do/event/wrY3XgnsLvwArzwyaaXRmL

## Sobre

Este repositório reúne materiais e um exemplo prático do minicurso **MC05 - Large Language Models and Agents**, com foco em fundamentos e aplicações de LLMs, incluindo uso de agentes.

## Carga Horária e Horários

- **Carga horária total:** 4.5 horas
- **09 de fevereiro de 2026:** 11:00 às 12:00
- **10 de fevereiro de 2026:** 13:30 às 15:00
- **11 de fevereiro de 2026:** 15:30 às 17:00

## Objetivo

Apresentar, de forma concisa e aplicada, os fundamentos conceituais e práticos dos **Large Language Models (LLMs)**, destacando a evolução dos Transformers e inovações recentes em inferência e ajuste fino. O minicurso oferece uma visão atualizada do ecossistema de modelos abertos (LLaMA 3, Qwen2, Mixtral, DeepSeek, entre outros), equilibrando base teórica essencial e demonstrações práticas de geração e fine-tuning, com foco em eficiência, alinhamento e aplicações científicas.

## Ementa

- Introdução aos LLMs: panorama 2023-2025, evolução, impacto e ecossistema open-source.
- Núcleo do Transformer: atenção, embeddings e normalização, compreensão conceitual sem excesso matemático.
- Variações modernas: Mixture of Experts (MoE), Rotary Embeddings e Attention Scaling (visão sintética e aplicada).
- Controle e inferência: parâmetros de geração (temperatura, top-p) e gerenciamento de contexto (KV cache, expected-attention, cache merging).
- Prática 1 - Inferência Interativa: experimentação guiada com prompts e parâmetros de geração, explorando variação de temperatura, top-p e raciocínio via chain-of-thought.
- Prompt engineering e in-context learning: few-shot, self-consistency e limites de contexto.
- Pré-treinamento e otimização: datasets em larga escala, quantização (FP8, INT4) e eficiência computacional.
- Ajuste fino supervisionado (SFT) e métodos eficientes: LoRA 2, QLoRA e estratégias em três estágios para fine-tuning de modelos quantizados.
- Prática 2 - Simulação de Fine-Tuning: demonstração simplificada de pipeline LoRA/QLoRA, seleção de camadas e visualização de pesos adaptados.
- Alinhamento de preferências: DPO, RLHF, GRPO e abordagens emergentes de raciocínio (DeepSeek-R1, raciocínio via RL).
- Avaliação moderna (2024-2025): MMLU-Pro/Pro+, AIME-24/25, LiveBench e GPQA; riscos de contaminação e limitações do LLM-as-a-judge.
- Tendências e desafios em LLMs abertos: interoperabilidade, governança e impacto científico.
- Interaction Patterns.
- Tool Calling.
- RAG.

## Estrutura atual do repositório

- `react_demo.py`: exemplo simples de agente ReAct com LangChain.
- `requirements.txt`: dependências Python do projeto.
- `docs/anatomia-agente-langchain.md`: explicação didática da anatomia de um agente no LangChain.

## Material da aula

- Anatomia do agente (LangChain): `docs/anatomia-agente-langchain.md`

## Instalação (pip)

1. (Opcional, recomendado) Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure a chave da OpenAI no arquivo `.env`:

```env
OPENAI_API_KEY=cole_sua_chave_aqui
```

## Execução do exemplo

```bash
python react_demo.py
```

## Bibliografia

- Bai, Y. et al. *Qwen2: Scaling Open Models for Multilingual and Multimodal Understanding*. Alibaba DAMO Academy, arXiv:2407.10671 (2024). https://arxiv.org/abs/2407.10671
- Qian, J. et al. *Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution*. arXiv:2409.12191 (2025). https://arxiv.org/abs/2409.12191
- Jiang, A.Q. et al. *Mixtral 8x7B: A Mixture-of-Experts Language Model*. Mistral AI Technical Report, arXiv:2401.04088 (2024). https://arxiv.org/abs/2401.04088
- Zhang, Y. et al. *DeepSeek Coder V2: Scaling Open Code Models with Mixture-of-Experts*. arXiv:2410.03810 (2024). https://arxiv.org/abs/2410.03810
- Touvron, H. et al. *LLaMA 3: Open Foundation and Chat Models*. Meta AI Technical Report, arXiv:2407.21783 (2024). https://arxiv.org/abs/2407.21783
- Xu, Y. et al. *Revisiting Group Relative Policy Optimization*. arXiv:2505.22257v1 (2025). https://arxiv.org/abs/2505.22257
- Li, K. et al. *Efficient Fine-Tuning of Quantized LLMs via Three-Stage Optimization*. ICLR 2025 submission. https://openreview.net/forum?id=zcx6rIMbbR
- Dettmers, T. et al. *QLoRA: Efficient Finetuning of Quantized LLMs*. NeurIPS (2023). https://arxiv.org/abs/2305.14314
- Ouyang, L. et al. *Training Language Models to Follow Instructions with Human Feedback*. OpenAI, NeurIPS (2022). https://arxiv.org/abs/2203.02155
