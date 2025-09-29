# Template-Driven Development Framework for AI-Augmented Coding

![banner](misc/banner.png)

**Read this in other languages:** [繁體中文](docs/readmes/README-zh-TW.md) | [简体中文](docs/readmes/README-zh-CN.md) | [Español](docs/readmes/README-es.md) | [日本語](docs/readmes/README-ja.md)

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
tempdd init  # You can choose the built-in workflow and preferred AI tool during initialization
```

### 3. Example: Default Workflow with Claude Code

The following example demonstrates using the default workflow with Claude Code. For detailed customization options and available workflows, refer to `tempdd help`.

Once you enter Claude Code, execute the following commands in sequence:

```bash
# Get help and understand available commands
/tempdd-go help

# Generate product requirements document
/tempdd-go prd build

# After finishing the PRD, create architecture design
/tempdd-go arch build

# After finishing the architecture design document, conduct research
/tempdd-go research build

# After finishing the research report, build implementation blueprint
/tempdd-go blueprint build

# After finishing the blueprint, generate task list
/tempdd-go tasks build

# After finishing the task list, execute tasks to generate the codes
/tempdd-go tasks run
```

From this example, you can see that development progresses from idea to implementation through multi-layered documentation. Each document is filled out by AI asking users for input when needed, which reduces the complexity of form-filling for users while enhancing consensus between AI and humans. Worth noting, the research step involves AI proactively searching for information online to improve its understanding of the implementation. I believe better workflows exist, and we shouldn't expect one workflow to satisfy every project. Therefore, this framework is designed to be easily customizable. Please refer to section ["Customize your workflow"](#customize-your-workflow) to learn more.

## Customize your workflow

TempDD allows you to create custom workflows tailored to your specific development needs. 

Follow the below steps to customize your workflow:
1. **Read the guide**: See [./customized/](./customized/) for comprehensive workflow creation instructions
2. **Create your workflow** following the structure and examples provided
3. **Initialize project** with your custom workflow:

```bash
tempdd init --workflow /path/to/your/custom/workflow_dir/
```

## Contributing Built-in Workflows

We encourage contributors to help expand TempDD's built-in workflow collection! By contributing new workflows, you can help other developers benefit from proven development patterns and specialized domain workflows.

### How to Contribute a New Built-in Workflow

1. **Fork this repository** - Create your own fork to work on
2. **Add your workflow files**:
   - Add new configuration files to `./tempdd/core/configs/`
   - Add corresponding templates to `./tempdd/core/templates/`
3. **Submit a Pull Request** - Share your workflow with the community

Your contributions will help make TempDD more valuable for developers across different domains and use cases. Whether it's a workflow for mobile development, data science, DevOps, or any other specialization, we welcome your expertise!

## Cross-AI tool integration

TempDD seamlessly integrates with multiple AI development tools:

| AI Tool | Status |
|---------|--------|
| **Claude Code** | ✅ Full Support |
| **Gemini CLI** | ✅ Full Support  |
| **Cursor** | ✅ Full Support  |
| **GitHub Copilot** | ✅ Full Support  |

## Acknowledgments

Thanks to the following repositories for inspiration:
- [github/spec-kit](https://github.com/github/spec-kit)
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)
