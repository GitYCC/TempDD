# Template-Driven Development Framework for AI-Augmented Coding

![banner](misc/banner.png)

🚧 **Work In Progress** - This framework is under active development

## Overview

TempDD is a template-driven development framework that enables structured human-AI collaboration through customizable workflows and agent-guided template interactions. 

As project complexity increases, AI Agents face challenges operating independently, making human-in-the-loop collaboration increasingly critical. Developers need effective tools to communicate with these black-box AI Agents. Template-driven approaches provide structured communication, reduce cognitive load, and enable consistent AI collaboration through guided workflows. This repository provides a framework that allows users to customize workflows according to their development projects, simplifying the process into a series of template-filling tasks. The framework incorporates agent mechanisms to reduce template complexity, enabling AI Agents to effectively assist users in completing documentation. We envision this framework being applicable across various development scenarios and even non-development contexts, while fostering open-source collaboration to integrate global knowledge.

## Features

- 📚 **Progressive AI mastery through layered docs** - Transform from AI user to AI master with sophisticated multi-layer  documentation that amplifies your control over AI behavior
- 📋 **Customizable template-driven workflow** - Structured approach to project development with customizable templates
- 💬 **Customizable agent-guided template interaction** - Customizable agents adapt to each template, providing interactive guidance to help users fill templates collaboratively
- 🤖 **Cross-AI tool integration** - Seamless integration with Claude Code, Gemini CLI, Cursor, and GitHub Copilot
- 🌐 **Multi-language support** - Users can fill templates using their preferred language

## Quick Start

### 1. Installation

Install `tempdd` using uv:

```bash
uv tool install --force --from git+https://github.com/GitYCC/TempDD.git tempdd && exec $SHELL
```

### 2. Initialize Project

Create a new project directory and initialize TempDD:

```bash
mkdir demo
cd demo
tempdd init

claude # run Claude Code
```

### 3. Use with Claude Code

Once in Claude Code, use these commands to build your project structure:

```bash
# Get help
/tempdd-go help

# Generate product requirements document
/tempdd-go prd build

# Create architecture design
/tempdd-go arch build

# Conduct research
/tempdd-go research build

# Build implementation blueprint
/tempdd-go blueprint build

# Generate task list
/tempdd-go tasks build

# Execute tasks
/tempdd-go tasks run
```

