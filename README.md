# Agentic AI Engineering Workshop

<a href="https://www.youtube.com/watch?v=LSk5KaEGVk4&list=WL&index=1&t=1s">Youtube Link</a> for the amazing workshop.

## Table of Contents

### Modules

- [Module 1 - Defining Agents | Deep Research with OpenAI Agents](#module-1---defining-agents--deep-research-with-openai-agents)
  - [Agents](#agents)
  - [Agentic Systems](#agentic-systems)
  - [Agentic Frameworks](#agentic-frameworks)
- [Module 1 - Code](#module-1---code)
- [Module 2 - Designing Agents | Engineering Team with CrewAI](#module-2---designing-agents--engineering-team-with-crewai)
  - [Workflow Design Patterns](#workflow-design-patterns)
  - [Agents in Contrast](#agents-in-contrast)
- [Module 2 - Code](#module-2---code)
- [Module 3 - Developing Agents | Autonomous Traders with MCP](#module-3---developing-agents--autonomous-traders-with-mcp)
  - [MCP](#mcp)
  - [Making an MCP Server](#making-an-mcp-server)
- [Module 3 - Code](#module-3---code)
- [Module 4 - Implications](#module-4---implications)
  - [Workforce Implications](#workforce-implications)
  - [Protopia](#protopia)

### My Notes

- [Notes for Windows (WSL) and MCP](#notes-for-windows-wsl-and-mcp)
  - [Setup in WSL](#setup-in-wsl)
  - [Installing NodeJS in WSL](#installing-nodejs-in-wsl)
  - [Playwright MCP](#playwright-mcp)
    - [Resolving Playwright Issues](#resolving-playwright-issues)
- [Other Errors](#other-errors)

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

<br>
<br>

- To avoid using all tools from MCP Server:
  - Mention it in the System Prompt
  - Or use a subset of tools returned by `list_tools()` and pass it to the `tools` argument in `Agent()`

### Module 4 - Implications

#### Workforce Implications

- More jobs created by AI than lost
- Funding for reskilling programs is key

<br>
<br>

- For data scientists to future-proof:
  - AI trends
    - SuperDataScience Podcast
  - Multi-agent orchestration and management
  - Don't underestimate the power of foundational subjects
    - Things like Linear Algebra, Calculus, Probability, Statistics, Algorithms, Data Structures, Optimization
    - Practically applied, e.g. for performance optimizations
    - Jon's YouTube channel has these
  - Domain expertise
    - Understanding the businesses you work with
  - Human-AI collaboration skills
  - Honing communication and influence skills within organization
    - E.g. Ability to convince people to invest

<br>
<br>

#### Protopia

- AI agents play a big part in "Protopia"
  - Abundant energy
    - Making solar panels, batteries etc more efficient
  - High quality nutrition for everyone
  - Extended lifespans
  - Education
  - Freedom from violence
  - Freedom of expression
  - Sustainability
  - Cultural preservation
  - Exploration
  - Sense of community

## Notes for Windows (WSL) and MCP

### Setup in WSL

- Open the WSL terminal
- Navigate to the agentic workshop directory
  - Windows directories are in `/mnt/`
  - E.g: `/mnt/c/Users/<User Name>/Desktop/some-folder`
- Set up a new virtual env (if current venv isn't compatible with Linux) by running:
  - `pip install uv`
    - Installs in global environment
  - `python3 -m uv venv -p 3.12.3 --seed <venv path/name>`
    - I had python 3.12.3
  - `source <venv path>/bin/activate`
  - `pip install uv`
    - Installs in virtual environment
  - `uv sync --active`

<br>

### Installing NodeJS in WSL

- Run: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash`
  - Check the latest version from <a href="https://github.com/nvm-sh/nvm?tab=readme-ov-file#install--update-script">their GitHub</a>
- Close/Reopen the WSL terminal
- Run: `nvm install node`
- Create links (so, e.g., `sudo npx` will work) by running:
  - `sudo ln -s "$NVM_DIR/versions/node/$(nvm version)/bin/node" "/usr/local/bin/node"`
  - `sudo ln -s "$NVM_DIR/versions/node/$(nvm version)/bin/npm" "/usr/local/bin/npm"`
  - `sudo ln -s "$NVM_DIR/versions/node/$(nvm version)/bin/npx" "/usr/local/bin/npx"`

<br>

### Playwright MCP

- Go to an empty directory (wherever you want to install it)
- Run: `npm init playwright@latest`
- It'll ask for config, I chose:
  - TypeScript or JavaScript: `Javascript`
  - Where to put tests: `tests`
  - Add GitHub Actions: `false`
  - Install Playwright Browsers: `true`
  - Install Playwright OS Dependencies: `true`

#### Resolving Playwright Issues

- If there are issues with the last few steps (when it says something like `switching to root to install dependencies`, or stays stuck for a while without any outputs):
  - Restart the system
  - Open WSL
  - Run: `sudo npx playwright install-deps`

<br>

- If you see this error in the trace:
<pre>
   Error: browserType.launchPersistentContext: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
   Run "npx playwright install chrome"
</pre>
- Do this:
  - Restart
  - Open WSL
  - Navigate to the folder where you installed playwright (where you used `npm init`)
  - Run: `npx playwright install chrome`
    - If you see a `could not resolve host: dl.google.com` error, try running the command again

<br>

- If you see `Request Timed Out` or `Temporary Failure in Name Resolution` errors:
  - Change nameserver in `/etc/resolv.conf` to `8.8.8.8`
  - Optionally, change the env var `DISPLAY=:0` by running:
    - `export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0`
      - This sets it to `8.8.8.8:0`
    - It only changes it for the session

### Other Errors

- When running MCP from `@modelcontextprotocol/server-filesystem`, make sure the path exists

  - Won't work if the `sandbox` folder doesn't exist

- For errors when running the Accounts MCP Server (such as timeout errors), run `uv run accounts_server.py --active` manually from the terminal first so it installs the packages and to see what it's doing

- For the memory MCP Server, make sure the folders exist

  - Won't work if the `memory` folder doesn't exist

- For `mcp-google-custom-search-server` to handle paths with spaces, change the `if` condition at the end of `src/index.ts` to:
  - `if (fileURLToPath(import.meta.url) === process.argv[1])`
  - and add `import { fileURLToPath } from "url";` at the top of the file
