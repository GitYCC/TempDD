# Template-Driven Development Framework for AI-Augmented Coding

![banner](misc/banner.png)

🚧 **Work In Progress** - This framework is under active development

## Overview

TempDD is a template-driven development framework designed to streamline AI-assisted coding workflows. 

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

