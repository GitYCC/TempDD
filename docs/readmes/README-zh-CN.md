# Template-Driven Development Framework for AI-Augmented Coding

![banner](../../misc/banner.png)

## 概述

TempDD是一个模板驱动的开发框架，通过可定制的工作流程和智能引导的模板交互，实现结构化的人机协作。

随着项目复杂性的增加，AI智能体面临独立操作的挑战，使得人机协作变得越来越重要。开发者需要有效的工具来与这些黑盒AI智能体进行沟通。模板驱动的方法提供了结构化沟通，减少认知负担，并通过引导式工作流程实现一致的AI协作。本仓库提供了一个框架，允许用户根据其开发项目定制工作流程，将过程简化为一系列模板填写任务。该框架结合了智能体机制来降低模板复杂性，使AI智能体能够有效地协助用户完成文档编写。我们预期这个框架适用于各种开发场景，甚至非开发环境，同时促进开源协作以整合全球知识。

## 特性

- 📚 **通过分层文档逐步掌握AI** - 通过复杂的多层文档从AI用户转变为AI专家，放大您对AI行为的控制
- 📋 **可定制的模板驱动工作流程** - 通过可定制模板进行项目开发的结构化方法
- 💬 **可定制的智能引导模板交互** - 可定制智能体适应每个模板，提供交互式指导帮助用户协作填写模板
- 🤖 **跨AI工具集成** - 与Claude Code、Gemini CLI、Cursor和GitHub Copilot无缝集成
- 🌐 **多语言支持** - 用户可以使用他们偏好的语言填写模板

## 快速开始

### 1. 安装

使用uv安装`tempdd`：

```bash
uv tool install --force --from git+https://github.com/GitYCC/TempDD.git tempdd && exec $SHELL
```

### 2. 初始化项目

创建新的项目目录并初始化TempDD：

```bash
mkdir demo
cd demo
tempdd init  # 您可以在初始化期间选择内置工作流程和首选AI工具
```

### 3. 示例：使用Claude Code的默认工作流程

以下示例演示了如何使用Claude Code的默认工作流程。有关详细的自定义选项和可用工作流程，请参考`tempdd help`。

进入Claude Code后，按顺序执行以下命令：

```bash
# 获取帮助并了解可用命令
/tempdd-go help

# 生成产品需求文档
/tempdd-go prd build

# 完成PRD后，创建架构设计
/tempdd-go arch build

# 完成架构设计文档后，进行研究
/tempdd-go research build

# 完成研究报告后，构建实施蓝图
/tempdd-go blueprint build

# 完成蓝图后，生成任务列表
/tempdd-go tasks build

# 完成任务列表后，执行任务以生成代码
/tempdd-go tasks run
```

从这个示例中，您可以看到开发过程从想法到实现通过多层文档进行。每个文档由AI在需要时向用户询问输入来填写，这减少了用户填表的复杂性，同时增强了AI与人类之间的共识。值得注意的是，研究步骤涉及AI主动在线搜索信息以提高其对实施的理解。我相信存在更好的工作流程，我们不应该期望一个工作流程满足每个项目。因此，该框架设计为易于定制。请参考["定制您的工作流程"](#定制您的工作流程)部分了解更多。

## 定制您的工作流程

TempDD允许您创建适合特定开发需求的自定义工作流程。

按照以下步骤定制您的工作流程：
1. **阅读指南**：查看[./customized/](../../customized/)获取全面的工作流程创建说明
2. **创建您的工作流程**，遵循提供的结构和示例
3. **使用自定义工作流程初始化项目**：

```bash
tempdd init --workflow /path/to/your/custom/workflow_dir/
```

## 贡献内置工作流程

我们鼓励贡献者帮助扩展TempDD的内置工作流程集合！通过贡献新的工作流程，您可以帮助其他开发者从经过验证的开发模式和专业领域工作流程中受益。

### 如何贡献新的内置工作流程

1. **Fork此仓库** - 创建您自己的fork进行工作
2. **添加您的工作流程文件**：
   - 将新的配置文件添加到`./tempdd/core/configs/`
   - 将相应的模板添加到`./tempdd/core/templates/`
3. **提交Pull Request** - 与社区分享您的工作流程

您的贡献将帮助TempDD对不同领域和用例的开发者更有价值。无论是移动开发、数据科学、DevOps还是任何其他专业化工作流程，我们都欢迎您的专业知识！

## 跨AI工具集成

TempDD与多个AI开发工具无缝集成：

| AI工具 | 状态 |
|---------|--------|
| **Claude Code** | ✅ 完全支持 |
| **Gemini CLI** | ✅ 完全支持 |
| **Cursor** | ✅ 完全支持 |
| **GitHub Copilot** | ✅ 完全支持 |

## 致谢

感谢以下仓库的启发：
- [github/spec-kit](https://github.com/github/spec-kit)
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)