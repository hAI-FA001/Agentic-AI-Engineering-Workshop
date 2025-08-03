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

- Terminology
  - <b>Agents</b> = LLMs
  - <b>Handoffs</b> = interactions
  - <b>Guardrails</b> = controls

<br>
<br>

- 3 steps:
  - Create an instance of Agent
  - Use `with trace()` to track / monitor
  - Call `Runner.run()`

### Module 2 - Designing Agents | Engineering Team with CrewAI

#### Workflow Design Patterns

- Blog post from Anthropic, "Building Effective Agents"
- <b>Prompt Chaining</b>
  - Decompose into fixed sub-tasks
  - Why?
    - More control
    - Guardrails for each step
    - Easier debugging
  - E.g:
    - LLM1 (outline) -> Code (check brand guidelines) -> LLM2 (full draft) -> LLM3 (polish + SEO)
    - LLM1 (pseudocode) -> Code (check architectural soundness) -> LLM2 (actual code) -> LLM3 (documentation + test cases)
- <b>Routing</b>
  - Direct an input into a specialized subtask (separation of concerns)
    - LLM Router routes input to specialized LLMs
  - E.g:
    - Patient symptoms -> LLM Router -> specialized LLM (cardiology, neurological, dermatological)
    - Legal document -> LLM Router (categorize) -> specialized LLM (contracts, compliance, litigation)
- <b>Parallelization</b>
  - Break tasks, run concurrently
    - Coordinator (code) -> LLMs -> Aggregator (code)
  - E.g:
    - Research papers -> specialized LLMs (methodology, statistical analysis, interpretation of results) -> Aggregator
    - Market data -> specialized LLMs (tech analysis, healthcare, energy) -> Aggregator
- <b>Orchestrator-Worker</b>
  - Break tasks dynamically, combine
    - Similar to previous but Coordinator and Aggregator are LLMs (renamed to "Orchestrator" and "Synthesizer")
  - Similar examples
- <b>Evaluator-Optimizer</b>
  - LLM output is validated by another
    - Input -> Generator - Solution -> Evaluator - Accepted -> Output
    - Input -> Generator <- Reject with Feedback - Evaluator
    - Loop introduced
  - E.g:
    - Evaluator ensuring coding standards and security
    - Evaluator ensuring effectiveness, age appropriateness, alignment with learning objectives

#### Agents in Contrast

- Open-ended
  - We don't define specific flows
- Feedback loops
- No fixed path
  - Higher risks and costs but we can minimize these with good design
- E.g: Human -> LLM <- Action / Feedback -> Environment
  - LLM -> Stop (Code)
  - Environment could be: DBs, Internet, IoT

### Module 2 - Code

- CrewAI
  - Lightweight
  - More opinionated than OpenAI Agents SDK
- Concepts
  - <b>Agent:</b> autonomous unit with: LLM, role, goal, backstory, memory, tools
    - role, goal and backstory become part of the System Prompt
    - Idea is to think explicitly in these terms
  - <b>Task:</b> specific assignment with: description, expected output, agent
  - <b>Crew:</b> a team of <b>Agents</b> and <b>Tasks</b>
    - <b>Sequential:</b> run in the order they are defined
      - More like a workflow
    - <b>Hierarchical:</b> use a Manager LLM
      - More autonomy

<br>
<br>

- 5 steps:
  - Create with `crewai create my_project`
  - Fill the config yaml files, define Agents and Tasks
  - Complete the `crew.py` to create Agents, Tasks and Crew
  - Update `main.py` to set inputs
  - Run with `crewai run`

<br>
<br>

- Giving coding skills is hard and complex
  - Write code
  - Execute code
  - Isolated in a Docker container
  - Interact with the container for feedback
- But it's not
  - `Agent(allow_code_execution=True, code_execution_mode="safe")`
    - Becomes harder to debug
  - <b>"Coder Agents"</b>
    - Any agent that uses code
    - E.g: Customer support agent using Python for calculations

<br>
<br>

- Engineering team:
  - Engr. Lead
  - Backend Engr.
  - Frontend Engr.
  - Test Engr.

### Module 3 - Developing Agents | Autonomous Traders with MCP

#### MCP

- "Model Context Protocol"

<br>
<br>

- It's not a:
  - Framework for building agents
  - Fundamental change to how agents work
  - Way to code agents
- It is a:
  - Protocol (standard)
  - Way to integrate tools, resources, prompts
  - "USB-C for AI apps"

<br>
<br>

- Reasons to not be excited:
  - Is a standard (not the tools themselves)
  - LangChain already has a big tool ecosystem
  - Any function can already be turned into a tool
- Reasons to be excited:
  - Frictionless integration
  - Exploding ecosystem
  - HTML was just a standard too

<br>
<br>

- 3 components:
  - <b>Host:</b> an app with LLMs
    - Can be: Any LLM app on your desktop (Claude Desktop, Cursor, our own Agent architecture)
    - Can not be: Claude on the web (claude.ai)
  - <b>MCP Client:</b> Inside <b>Host</b>, connects 1:1 to <b>MCP Server</b>
    - For every MCP Server, we have 1 MCP Client
  - <b>MCP Server:</b> Provides tools, context, prompts
- Example:
  - Google Maps is an <b>MCP Server</b> with geolocation tools
  - Claude Desktop can be configured to run an <b>MCP Client</b> that launches the Google Maps <b>MCP Server</b>

<br>
<br>

- Architecture
  - Locally
    - Your computer runs the Host
      - Host may be Cursor, Claude Desktop, etc
    - The Host creates MCP Clients (also on your computer)
    - MCP Clients spin up MCP Servers (also on your computer, unlike the traditional Client-Server idea)
    - Every MCP Server has 1 MCP Client (1:1 connection)
  - Remotely
    - A remote server may also be running MCP Servers
    - Need MCP Clients (locally) to connect to these MCP Servers (remote)
  - MCP Server might access an API on a remote server
    - E.g: Google Maps MCP Server needs information from Google's API

<br>
<br>

- Misconception: MCP Servers run remotely
- Reality: Download an Open-Source MCP Server and run it locally

<br>
<br>

#### Making an MCP Server

- Why?
  - Sharing of tools and resources
  - Consistently incorporate MCP Servers
    - Call tools in the same way
  - Understand the plumbing
- Why not?
  - If it's only for us, then just make tools
    - `@function_tool` decorator

### Module 3 - Code

- Autonomous Traders
- Commercial project (most projects are technical, like Deep Research)
- 6 MCP Servers, 44 tools, 2 resources
- Agents
- Autonomous
