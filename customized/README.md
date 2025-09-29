# Custom Workflow Creation Guide

This document provides comprehensive guidance for creating custom workflows using the TempDD framework. The workflow system allows you to define structured development processes tailored to your specific needs.

## Overview

TempDD custom workflows enable you to create systematic approaches to software development by defining stage-based processes with templates, prompts, and data flow. Each workflow consists of multiple stages that can build upon previous stage outputs. Please reference `./workflow_example` as an example.

## Workflow Structure

A custom workflow consists of:

- **Configuration file** (`config.yaml`) - Defines workflow metadata, stages, and data flow
- **Template files** - Markdown templates for each stage with prompts and structured content
- **Symbol system** - Data variables that flow between stages

## Creating a Custom Workflow

### Step 1: Create Workflow Directory

```bash
mkdir my_custom_workflow
cd my_custom_workflow
mkdir templates
```

### Step 2: Define Configuration (`config.yaml`)

Create your workflow configuration following this structure:

```yaml
description: "Brief description of your workflow purpose"
help: |
  [Workflow instrution]
language: en
logging_level: WARNING
stages:
  - stage1_name
  - stage2_name
  - stage3_name
define:
  stage1_name:
    template: templates/stage1.md
    input_symbols: null
    output_symbol: PATH_STAGE1
  stage2_name:
    template: templates/stage2.md
    input_symbols:
      PATH_STAGE1
    output_symbol: PATH_STAGE2
  stage3_name:
    template: templates/stage3.md
    input_symbols:
      PATH_STAGE1
      PATH_STAGE2
    output_symbol: null
```

#### Configuration Elements

- **description**: Brief workflow description
- **help**: User guidance with stage sequence and commands
- **language**: Content language (en, zh, etc.)
- **logging_level**: Log verbosity (DEBUG, INFO, WARNING, ERROR)
- **stages**: Ordered list of stage names
- **define**: Stage definitions with templates and data flow

#### Stage Definition Properties

- **template**: Path to markdown template file
- **input_symbols**: List of variables from previous stages (null for first stage)
- **output_symbol**: Variable name for this stage's output (null if no output needed)

### Step 3: Create Stage Templates

Each stage needs a markdown template file in the `templates/` directory. Templates have two sections:

1. **YAML frontmatter** - Contains prompts for different actions
2. **Markdown content** - The structured template users will fill

#### Template Structure

```markdown
---
build:
  prompt: |
    Your role and instructions for the build action.

    Target Document: {{TARGET_DOCUMENT}}

    Your systematic approach:
    1. Step one description
    2. Step two description
    3. Step three description

    Quality standards and requirements.

run:
  prompt: |
    Instructions for the run action (if applicable).
    This is typically used for execution/implementation stages.
---

# Template Content

**Guidelines**:
- Content rules and constraints
- Quality requirements
- Structure requirements

**Fill-in `[[...]]` placeholders with appropriate content**

## Section 1
[[Placeholder for content]]

## Section 2
[[Another placeholder]]

### Subsection
- [[Bullet point placeholder]]
- [[Another bullet point]]
```

(1) A template can support multiple actions:

```markdown
---
build:
  prompt: |
    Instructions for building/creating content

run:
  prompt: |
    Instructions for executing/implementing
---
```

(2) Access previous stage outputs using symbol syntax:

```markdown
**PRD Reference**: {{PATH_PRD}}
**Blueprint Reference**: {{PATH_BLUEPRINT}}

Based on the requirements in {{PATH_PRD}}, implement:
[[Feature implementation based on PRD]]
```

#### Prompt Design Best Practices

- **Define clear roles**: Specify who the AI should act as (Product Manager, Technical Lead, etc.)
- **Provide systematic approach**: Break down the task into numbered steps
- **Set quality standards**: Define specific requirements and constraints
- **Use placeholders**: Include `{{TARGET_DOCUMENT}}` and input symbols like `{{PATH_STAGE1}}`
- **Include validation**: Add review checklists and completion criteria

### Step 4: Design Data Flow

- **Input symbols**: Variables from previous stages available as `{{SYMBOL_NAME}}`
- **Output symbols**: Stage output stored in specified variable
- **Symbol flow**: Design dependencies between stages

## Example: Software Development Workflow

Using the `workflow_example/` as reference:

### Configuration Analysis

```yaml
description: "Simple flow of software development, including PRD, Arch., Tasks stages."
stages:
  - prd        # Product Requirements Document
  - blueprint  # Technical Architecture
  - tasks      # Implementation Tasks

define:
  prd:
    template: templates/prd.md
    input_symbols: null           # First stage, no inputs
    output_symbol: PATH_PRD       # Creates PATH_PRD variable

  blueprint:
    template: templates/blueprint.md
    input_symbols:
      PATH_PRD                    # Uses PRD as input
    output_symbol: PATH_BLUEPRINT # Creates PATH_BLUEPRINT variable

  tasks:
    template: templates/tasks.md
    input_symbols:
      PATH_PRD                    # Uses both PRD and blueprint
      PATH_BLUEPRINT
    output_symbol: null           # Final stage, no output symbol
```

### Stage Templates

#### PRD Template (`templates/prd.md`)
- **Role**: Product Manager gathering requirements
- **Process**: Systematic requirement gathering through targeted questions
- **Output**: Comprehensive Product Requirements Document
- **Key sections**: Basic Information, Objectives, User Scenarios, Requirements

#### Blueprint Template (`templates/blueprint.md`)
- **Role**: Technical Lead with "just ship it" mentality (Linus style)
- **Process**: Transform PRD into concrete development blueprint
- **Input**: `{{PATH_PRD}}` - References the completed PRD
- **Output**: Technical implementation guide
- **Key sections**: Architecture, Components, APIs, Quick Start

#### Tasks Template (`templates/tasks.md`)
- **Role**: Senior Developer managing task execution
- **Process**: Break blueprint into actionable tasks with TDD cycles
- **Inputs**: `{{PATH_PRD}}` and `{{PATH_BLUEPRINT}}`
- **Output**: Executable task list
- **Key sections**: Task list, TDD cycles, validation checkpoints

### Usage Commands

```bash
# Build PRD (first stage)
/tempdd-go prd build

# Build technical blueprint (uses PRD)
/tempdd-go blueprint build

# Build task list (uses PRD and blueprint)
/tempdd-go tasks build

# Execute tasks (run implementation)
/tempdd-go tasks run
```
