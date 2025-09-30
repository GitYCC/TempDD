# TempDD Operating Principles

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [How the System Works](#how-the-system-works)
3. [Template-Driven Implementation](#template-driven-implementation)
4. [Why Easy to Customize](#why-easy-to-customize)

---

## Core Concepts

### What is TempDD?

TempDD (Template-Driven Development) is a framework that **structures the development process** through three core mechanisms:

```
📋 Configuration File (config.yaml)
   ↓ Defines workflow
📝 Template Files (templates/*.md)
   ↓ Defines structure and AI behavior for each stage
🤖 AI Collaboration
   ↓ Assists in completing documents through guided conversation
```

### Design Philosophy

TempDD follows a simple philosophy:

> **"Users only need to declare what they want, the system automatically handles how to do it"**

This means:
- ✅ Users define workflow in YAML → System executes automatically
- ✅ Users define AI behavior in templates → AI follows automatically
- ✅ Users add stages or modify flow → No code changes needed

---

## How the System Works

### Overall Architecture

```
                    User
                      │
                      │ Execute command: /tempdd-go prd build
                      ↓
              ┌─────────────────┐
              │    AI Tool      │  (Claude/Gemini/Cursor/Copilot)
              │ Command System  │
              └────────┬────────┘
                       │ Call: tempdd ai "prd build"
                       ↓
              ┌─────────────────┐
              │  TempDD Core    │
              │                 │
              │ 1. Read config  │  config.yaml
              │ 2. Load template│  templates/prd.md
              │ 3. Generate     │  [AI_INSTRUCTION_START]...
              │    instruction  │
              └────────┬────────┘
                       │ Return AI instruction
                       ↓
              ┌─────────────────┐
              │  AI Execution   │
              │                 │
              │ - Converse with │
              │   user          │
              │ - Fill document │
              │ - Complete stage│
              └─────────────────┘
```

### Execution Flow Example

Suppose the user executes `/tempdd-go prd build`:

```
Step 1: Read configuration
   config.yaml → stages: [prd, arch, blueprint]
   define.prd → template: templates/prd.md

Step 2: Parse template
   templates/prd.md →
   ├─ YAML frontmatter: build.prompt (AI behavior definition)
   └─ Markdown content: document structure

Step 3: Handle dependencies
   prd stage's input_symbols: null (no dependencies)
   prd stage's output_symbol: PATH_PRD (output path)

Step 4: Replace variables
   {{TARGET_DOCUMENT}} → docs-for-works/001_initialization/prd.md

Step 5: Generate AI instruction
   [AI_INSTRUCTION_START]
   System rules (language settings, etc.)
   ===
   Stage instruction (with variables processed)
   [AI_INSTRUCTION_END]

Step 6: AI execution
   AI converses with user following the instruction to complete PRD document
```

### Connecting Stages

TempDD uses a **Symbol System** to connect different stages:

```
Stage 1: PRD
   Input: None
   Output: PATH_PRD → "docs-for-works/001_initialization/prd.md"

Stage 2: Architecture
   Input: PATH_PRD (reads PRD content)
   Output: PATH_ARCH → "docs-for-works/001_initialization/arch.md"

Stage 3: Blueprint
   Input: PATH_PRD, PATH_ARCH (reads content from previous two stages)
   Output: PATH_BLUEPRINT → "docs-for-works/001_initialization/blueprint.md"
```

**Key Mechanism**:
- Each stage's output document path is stored as a symbol (e.g., `PATH_PRD`)
- Subsequent stages can reference it in templates using `{{PATH_PRD}}`
- System automatically replaces it with the actual path

---

## Template-Driven Implementation

### What is Template-Driven?

**Core Concept**: Separation of "process" and "content"

```
Traditional Approach:
   Code + Logic + Content → Mixed together, hard to modify

Template-Driven:
   Configuration (process definition) → config.yaml
   Templates (content structure) → templates/*.md
   Execution (automation) → TempDD Core
```

### TempDD Template Structure

Each template file contains a **two-layer design**:

```markdown
---
# Layer 1: YAML Frontmatter (defines AI behavior)
build:
  prompt: |
    You are a Product Manager...
    Target document: {{TARGET_DOCUMENT}}

    Your workflow:
    1. Ask user what they want to build
    2. Systematically collect requirements
    3. Fill out complete PRD document

run:
  prompt: |
    Instructions for execution...
---

# Layer 2: Markdown Content (defines document structure)

# Product Requirements Document

## Basic Information
**Product Name**: [[To be filled]]

## Goals & Objectives
[[To be filled]]

## User Scenarios
[[To be filled]]
```

**Design Insight**:
- **Layer 1** controls **how AI interacts with users**
- **Layer 2** controls **the final document structure**

### Configuration-Driven Execution

All workflow is defined by `config.yaml`:

```yaml
# Declare what stages exist
stages:
  - prd
  - arch
  - blueprint

# Define each stage's details
define:
  prd:
    template: templates/prd.md     # Which template to use
    input_symbols: null            # What inputs are needed (none)
    output_symbol: PATH_PRD        # What to output (PRD path)

  arch:
    template: templates/arch.md
    input_symbols: [PATH_PRD]      # Needs PRD as input
    output_symbol: PATH_ARCH

  blueprint:
    template: templates/blueprint.md
    input_symbols: [PATH_PRD, PATH_ARCH]  # Needs PRD and Arch
    output_symbol: PATH_BLUEPRINT
```

**Key Points**:
- Stage order, quantity, and names are fully customizable
- Dependencies between stages are clear and explicit
- Adding stages only requires config changes, no code modification

### Dynamic Instruction Generation

System **dynamically generates** AI instructions based on templates:

```
User executes: /tempdd-go arch build

System processing:
1. Read config.yaml → Find arch stage definition
2. Load templates/arch.md
3. Extract build action's prompt
4. Parse input_symbols: [PATH_PRD]
   → PATH_PRD = "docs-for-works/001_initialization/prd.md"
5. Replace variables in prompt:
   {{PATH_PRD}} → docs-for-works/001_initialization/prd.md
   {{TARGET_DOCUMENT}} → docs-for-works/001_initialization/arch.md
6. Inject system rules (language settings, etc.)
7. Output complete instruction

AI receives:
   [AI_INSTRUCTION_START]

   Global Rules: Use "en" as language...

   ===

   You are an architect...
   Please read PRD: docs-for-works/001_initialization/prd.md
   Design architecture and write to: docs-for-works/001_initialization/arch.md

   [AI_INSTRUCTION_END]
```

### Multilingual Support Mechanism

**Observation**: All TempDD built-in templates are written in English, yet users can interact in Chinese, Japanese, Korean, or any language. How is this achieved?

**Design Principle**: Language Translation Layer

```
          ┌──────────────────────────────────────┐
          │      Template (English)              │
          │                                      │
          │   "You are a Product Manager..."     │
          │   "Ask the stakeholder..."           │
          └──────────────┬───────────────────────┘
                         │
                         ↓ System injects language rule
          ┌──────────────────────────────────────┐
          │   Language Rule Injection            │
          │                                      │
          │   **RULE1:** You MUST use "zh-TW"    │
          │   as your preferred language...      │
          └──────────────┬───────────────────────┘
                         │
                         ↓ AI processes automatically
          ┌──────────────────────────────────────┐
          │       AI Behavior                    │
          │                                      │
          │ - Read English instruction           │
          │   (understand task)                  │
          │ - Interact with user in Chinese      │
          │ - Fill document in Chinese           │
          └──────────────────────────────────────┘
```

#### How It Works

When user executes a command:

```
Step 1: User selects language during tempdd init
   → Stored in config.yaml: language: "zh-TW"

Step 2: System loads English template
   → templates/prd.md (prompt written in English)

Step 3: System injects language rule at the beginning when generating instruction
   [AI_INSTRUCTION_START]

   **Global Rules**:
   **RULE1:** You MUST use "zh-TW" as your preferred language
   for following conversation and documentation.
   However, use English for code (including comments)
   and web search queries.

   ===

   You are a Product Manager...
   [English instruction content]

   [AI_INSTRUCTION_END]

Step 4: AI execution
   → AI reads and understands English instruction
   → But converses with user in Traditional Chinese
   → Generated document is also in Traditional Chinese
```

#### Why This Design?

**Advantage 1: Template Reusability**
```
One English template → Supports all language users

Don't need:
  ├── templates/prd_en.md
  ├── templates/prd_zh-TW.md
  ├── templates/prd_zh-CN.md
  ├── templates/prd_ja.md
  └── templates/prd_ko.md

Only need:
  └── templates/prd.md (English) + language setting
```

**Advantage 2: English as Developer Lingua Franca**
- Template developers can write in English (most widely understood language)
- Code and technical terms remain in English (industry standard)
- Facilitates international collaboration and contribution

**Advantage 3: AI's Multilingual Capability**
- Modern AI models have excellent multilingual understanding
- AI can read English instructions and respond in any language
- Translation quality guaranteed by AI, no manual template translation needed

**Advantage 4: Easy Maintenance**
- Only need to maintain one English template set
- Template modifications don't require updating multiple language versions
- Reduces maintenance cost and synchronization issues

#### Language Configuration Flexibility

Users can select language during initialization:

```bash
$ tempdd init

# Interactive selection
Select a language:
  > English
    繁體中文
    简体中文
    日本語
    한국어
    Custom language code
```

Or modify in `config.yaml` at any time:

```yaml
language: zh-TW  # Change to any language code
```

**Supported Languages**: Any language supported by AI models
- `en` - English
- `zh-TW` - Traditional Chinese
- `zh-CN` - Simplified Chinese
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- ... and more

#### Real-World Example

**Scenario**: Taiwan user selects Traditional Chinese

Template (English):
```markdown
---
build:
  prompt: |
    You are a Product Manager.
    Ask "What do you want to build today?"
---
```

AI actual behavior:
```
AI: 你今天想要建立什麼？
User: 我想做一個任務管理系統
AI: 好的，讓我們來定義這個任務管理系統的需求...
```

Generated document:
```markdown
# 產品需求文件 (PRD)

## 基本資訊
**產品名稱**: 任務管理系統

## 目標與目的
建立一個簡單易用的任務管理系統...
```

**Key Insight**: Separation of template language and user language enables TempDD to support global users with minimal maintenance cost.

---

## Why Easy to Customize

### 1. Configuration as Specification

**Traditional Approach**: Modifying workflow requires code changes

**TempDD Approach**: Only need to modify YAML

```yaml
# Example: Customize workflow for data science projects

stages:
  - problem_definition   # Define problem
  - data_exploration     # Data exploration
  - model_design         # Model design
  - evaluation          # Evaluation report

define:
  problem_definition:
    template: templates/problem.md
    input_symbols: null
    output_symbol: PATH_PROBLEM

  data_exploration:
    template: templates/data_explore.md
    input_symbols: [PATH_PROBLEM]
    output_symbol: PATH_DATA

  # ... and so on
```

**Done!** No code modification needed.

### 2. Templates as Plugins

Adding capabilities is like adding building blocks:

```
Original templates:
templates/
  ├── prd.md
  ├── arch.md
  └── blueprint.md

Add custom templates:
templates/
  ├── prd.md
  ├── arch.md
  ├── blueprint.md
  ├── security_review.md   ← New!
  └── performance_test.md  ← New!
```

Reference in `config.yaml`:

```yaml
define:
  security_review:
    template: templates/security_review.md
    input_symbols: [PATH_BLUEPRINT]
    output_symbol: PATH_SECURITY

  performance_test:
    template: templates/performance_test.md
    input_symbols: [PATH_BLUEPRINT]
    output_symbol: PATH_PERF
```

### 3. Full Control Over AI Behavior

Each stage's AI behavior is defined by the template's `prompt`:

```markdown
---
build:
  prompt: |
    [Role Definition]
    You are a senior [Technical Expert/Product Manager/Data Scientist]...

    [Interaction Style]
    - Systematic questioning: Ask one question at a time, update document immediately after getting answer
    - Free discussion: Conversationally explore requirements with user
    - Guided completion: Step-by-step guide user through each section

    [Quality Standards]
    - All [[...]] must be replaced
    - Ensure content is complete and actionable
    - Follow specific formats or conventions
---
```

**Flexibility**:
- Define AI's role and expertise
- Control AI's questioning approach
- Set output quality standards
- Support multilingual instructions

### 4. Multiple Actions Support

Each stage can have multiple actions:

```markdown
---
build:
  prompt: |
    Create document from scratch...

continue:
  prompt: |
    Continue from existing content...

review:
  prompt: |
    Review document and provide suggestions...

refactor:
  prompt: |
    Refactor existing content...
---
```

Usage:

```bash
/tempdd-go prd build      # Build PRD
/tempdd-go prd continue   # Continue PRD
/tempdd-go prd review     # Review PRD
/tempdd-go tasks run      # Execute tasks
```

### 5. Symbol System Flexibility

Supports complex stage dependencies:

```yaml
# Linear flow: A → B → C
define:
  stage_a:
    output_symbol: PATH_A
  stage_b:
    input_symbols: [PATH_A]
    output_symbol: PATH_B
  stage_c:
    input_symbols: [PATH_B]
    output_symbol: PATH_C

# Branching flow: A → (B, C) → D
define:
  stage_a:
    output_symbol: PATH_A
  stage_b:
    input_symbols: [PATH_A]  # B depends on A
    output_symbol: PATH_B
  stage_c:
    input_symbols: [PATH_A]  # C also depends on A (parallel with B)
    output_symbol: PATH_C
  stage_d:
    input_symbols: [PATH_B, PATH_C]  # D depends on both B and C
    output_symbol: PATH_D
```

### 6. Cross-AI Tool Integration

TempDD designed a unified integration interface:

```
All AI tools follow the same pattern:

User command → AI tool command system → Call tempdd ai → Receive instruction → Execute
```

**Adding new AI tool support** only requires:
1. Define integration config (tool directory, file format)
2. Create command file (calls `tempdd ai`)
3. Run `tempdd init` and select new tool

---

## Summary: Design Essence

TempDD's ease of customization stems from three core designs:

### 1. Configuration-Logic Separation
```
  Configuration (YAML) ────→ Defines "what to do"
          │
          ↓
  Logic (Core) ────→ Handles "how to do"
```
Users only need to care about configuration; system executes logic automatically.

### 2. Templates as Languages
```
  Each template = A development "language"

  PRD template         → Language of product requirements
  Architecture template → Language of system design
  Task template        → Language of implementation planning

  Adding templates = Extending language capabilities
```

### 3. Symbols Connect Stages
```
  Stage A ─(PATH_A)→ Stage B ─(PATH_B)→ Stage C
                      ↓(PATH_A)
                     Stage D ─(PATH_D)→ ...
```
Symbol system enables flexible stage composition, supporting arbitrarily complex workflows.

---

## Real-World Use Cases

### Example 1: Standard Software Development

```yaml
stages: [prd, arch, research, blueprint, tasks]
```

```
PRD → Architecture → Technical Research → Implementation Blueprint → Task Breakdown → Execution
```

### Example 2: Data Science Projects

```yaml
stages: [problem, data_explore, feature_eng, model, evaluation]
```

```
Problem Definition → Data Exploration → Feature Engineering → Model Design → Evaluation Report
```

### Example 3: Documentation-Driven Development

```yaml
stages: [spec, api_design, test_plan, implementation]
```

```
Specification → API Design → Test Plan → Implementation
```

**Key Insight**: Same system, just modify configuration and templates to adapt to completely different development workflows.
