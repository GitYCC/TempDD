# Template-Driven Development Framework for AI Coding

🚧 **Work In Progress** - This framework is under active development

## Overview

TempDD is a template-driven development framework designed to streamline AI-assisted coding workflows. 

## Quick Start

### 1. Installation

Install `tempdd` using uv:

```bash
uv tool install --force --from git+https://github.com/GitYCC/TempDD.git tempdd
source /path/to/.XX-rc  # Replace with your shell config file (.bashrc, .zshrc, etc.)
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
# Generate product requirements document
/tempdd prd build

# Create architecture design
/tempdd arch build

# Conduct research
/tempdd research build

# Build implementation blueprint
/tempdd blueprint build

# Generate task list
/tempdd tasks build

# Execute tasks
/tempdd tasks run
```

## Features

- 📋 **Template-driven workflow** - Structured approach to project development
- 🤖 **AI integration** - Seamless integration with Claude Code
- 🌐 **Multi-language support** - Support for different languages (including Traditional Chinese)
