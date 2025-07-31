# Agentic AI Engineering Workshop

<a href="https://www.youtube.com/watch?v=LSk5KaEGVk4&list=WL&index=1&t=1s">Youtube Link</a>

## Modules

### Module 1 - Defining Agents | Deep Research with OpenAI Agents

#### Agents

- "Programs where LLM outputs control the workflow"
- AI solution that involves:

  - Multiple LLM calls
  - Tool-use
  - Environment where LLMs interact
  - A planner
  - Autonomy

<br>
<br>

- <a href="https://www.youtube.com/watch?v=m9ccaNDS-LI&list=PLRDl2inPrWQVW4aBgenJsTvw97qMhRtb8&index=70">Podcast episode 841 | Andrew Ng</a>
  - In support of LLMs
- <a href="https://www.youtube.com/watch?v=cuPUh7eTh8k&list=PLRDl2inPrWQVW4aBgenJsTvw97qMhRtb8&index=44">Podcast episode 867 | Andriy Burkov</a>
  - "LLMs are overhyped"

<br>
<br>

- "Humanity's Last Exam" benchmark
  - 2500 challenging questions
  - \> 100 subject areas
- With agentic design (Deep Research), o3 reaches > 25%
- Length of tasks AI can do is doubling every 7 months
  - Q/A -> Count words -> Find facts on web -> Train classifier
  - Getting closer to 1hr with 50% success rate

<br>
<br>

- Unprecedented time to develop agents due to:
  - ML/LLM advancements
    - PyTorch Lightning, HuggingFace, Agentic Frameworks
  - Cloud infra
  - Data
    - Massive open-source datasets
  - Open-Source Software
  - Low-cost Hardware
  - Dev tools
    - Drag-and-drop interfaces
  - Connectivity
    - Internet, wireless
  - Supportive regulatory environment
  - Market demand
  - Educational resources

<br>
<br>

- Examples:
  - Code Generation -> Team of S/W Devs
    - Module 2
  - Medical diagnosis
    - Specialized multi-modal models
  - Literature review
  - Design and run experiments, then write paper
    - Multi-agent
  - Replace more and more enterprise tasks
    - Billion $ firm with no employees

#### Agentic Systems

- 2 Types:
  - `Workflows`: Predefined orchestration of LLMs and tools
  - `Agents`: Dynamic orchestration via LLMs
- Tools give autonomy
  - Query DB, message other LLMs
  - "LLM can reach into my computer"
    - Reality: LLM doesn't execute the tool itself, LLM only responds with the actions needed (the actual code executes the tool)

<br>
<br>

- Risks:
  - Unpredictable path
  - Unpredictable output
  - Unpredictable costs
- Solutions:
  - Monitoring
  - Guardrails

#### Agentic Frameworks

- 1st layer

  - No framework
    - Understand under-the-hood
  - MCP
    - Protocol to connect agents with data sources and tools
    - Don't need the "code glue", just conform to MCP standard
    - Module 3

- 2nd layer

  - OpenAI Agents SDK
  - CrewAI
    - Heavier than Agents SDK
    - YAML configs
    - Module 2

- 3rd layer
  - LangGraph
  - AutoGen

### Module 1 - Code

- OpenAI Agents SDK
  - Lightweight
  - Unopinionated
  - Not a big learning curve

### Module 2 - Designing Agents | Engineering Team with CrewAI

### Module 3 - Developing Agents | Autonomous Traders with MCP
