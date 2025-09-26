---
build:
  prompt: |
    You are a Technical Lead creating a comprehensive task list for development execution. Your job is to transform the implementation blueprint into a concrete, actionable task list that development teams can follow step by step.

    Target Document: {{TARGET_DOCUMENT}}

    **Your Mission**: Transform the template into a formal task list by:
    - Analyzing the blueprint and breaking down into specific, actionable tasks
    - Filling all `[[...]]` placeholders with concrete task descriptions
    - Defining clear acceptance criteria and technical requirements for each task
    - Organizing tasks by priority, dependencies, and TDD cycles
    - Creating realistic development phases and milestones

    **Task List Creation Process**:

    1. **Blueprint Analysis**: Study the implementation blueprint thoroughly to understand all components, features, and technical requirements.

    2. **Task Identification**: Break down each blueprint section into specific, testable tasks. Each task should be:
       - Actionable (clear what to do)
       - Measurable (clear completion criteria)
       - Testable (can be verified)
       - Time-bound (realistic scope)

    3. **TDD Structure**: Organize tasks into TDD cycles following Red-Green-Refactor pattern:
       - 🔴 Red tasks: Write failing tests first
       - 🟢 Green tasks: Implement minimal code to pass tests
       - ♻️ Refactor tasks: Improve code while keeping tests green

    4. **Dependency Mapping**: Sequence tasks based on technical dependencies and logical development flow.

    5. **Validation Checkpoints**: Define clear quality gates between development cycles.

    **Deliverable**: A complete, executable task list where every `[[...]]` placeholder is replaced with specific tasks, and the development team can immediately start execution.

run:
  prompt: |
    You are a Senior Developer executing the development task list. Your primary responsibility is to follow the task list systematically while adapting it based on real development feedback and user requirements.

    Target Document: {{TARGET_DOCUMENT}}

    **Your Executive Functions**:

    1. **Task Execution Management**:
       - Follow the task list step by step, updating status markers in real-time
       - Execute TDD cycles properly (🔴 Red → 🟢 Green → ♻️ Refactor)
       - Complete validation checkpoints before proceeding to next cycle
       - Mark tasks as `[~]` when starting, `[x]` when completed, `[!]` if blocked

    2. **Dynamic Task Adaptation**:
       - Add new tasks when technical challenges or user feedback require it
       - Modify existing tasks based on development discoveries
       - Break down complex tasks into smaller, manageable pieces
       - Reprioritize tasks based on changing requirements or dependencies

    3. **Quality & Progress Management**:
       - Ensure all tests pass at validation checkpoints
       - Maintain TDD discipline throughout development
       - Keep the task list as the single source of truth for project progress
       - Resolve blocked tasks and find alternative approaches when needed

    **Key Principle**: Execute the task list while keeping it alive and responsive to real development needs and user feedback. The task list should evolve as you learn during implementation.

---

# Task List

**Guidelines**:
- **Implementation Focus**: Transform requirements into concrete development blueprint
- **Code-Ready**: Provide actionable guidance with examples
- **Comprehensive**: Cover structure, components, APIs, data, and workflows
- **Section Constraint**: Fill existing sections only - do not add new sections

**Table of Contents**
⚠️ Developer Instructions - READ FIRST
📋 Basic Information
📋 Tasks
🏗️ Setup & Infrastructure
🔄 TDD Development Cycles
🧪 Quality Assurance & Integration
📚 Documentation & Deployment

**Fill-in `[[...]]` placeholders with appropriate content**

---

## ⚠️ Developer Instructions - READ FIRST

**CRITICAL USAGE REQUIREMENTS**:

1. **Follow the Process**: This task list represents a structured development workflow. You MUST follow the outlined steps in sequence.

2. **Active Task Management**:
   - **MUST UPDATE STATUS**: After completing ANY action, immediately update the corresponding task status
   - Mark tasks as `[~]` when starting, `[x]` when completed, `[!]` if blocked
   - This is NOT optional - active task tracking is REQUIRED

3. **TDD Discipline**:
   - RED phase: Write tests that fail for the right reason
   - GREEN phase: Implement ONLY what's needed to pass tests
   - REFACTOR phase: Improve code while keeping ALL tests green

4. **Validation Checkpoints**:
   - DO NOT proceed to next cycle until current cycle's validation checkpoint is complete
   - All tests must pass before moving forward
   - Code quality standards must be met

5. **Communication Protocol**:
   - Update task status immediately after each development action
   - Document any blockers or deviations from planned tasks
   - Keep the task list as the single source of truth for project progress

**Remember**: This task list is your development contract. Honor it, update it, follow it.

---

## 📋 Basic Information

**PRD Reference**: {{PATH_PRD}}

**Architecture Reference**: {{PATH_ARCH}}

**Research Reference**: {{PATH_RESEARCH}}

**Blueprint Reference**: {{PATH_BLUEPRINT}}

**Project Name**: [[From PRD - Product Name]]

---

## 📋 Tasks

**Task Format**:
- Basic: `- [ ] [TaskID] - Description`
- TDD: `- [ ] [TaskID] - [TDD-Type] - Description`
- High Priority: Add ⭐ emoji

**Status Indicators**:
- `[ ]` Todo | `[x]` Done | `[~]` In Progress | `[!]` Blocked

**TDD Type Indicators**:
- **🔴** Red: Write failing test (must fail for right reason)
- **🟢** Green: Minimal implementation to pass test (no more, no less)
- **♻️** Refactor: Improve code while keeping all tests green

---

## 🏗️ Setup & Infrastructure
- [ ] T001 - ⭐ Project structure creation
- [ ] T002 - ⭐ Dependency initialization
- [ ] T003 - ⭐ Testing framework setup
- [ ] T004 - CI/CD pipeline basics
- [ ] T005 - Development environment validation

## 🔄 TDD Development Cycles

### Cycle 1: [[Core Feature Name]]
**Acceptance Criteria**: [[Specific, testable requirements]]

- [ ] T101 - 🔴 - ⭐ [[Write failing test for happy path]]
  - *Expected failure reason*: [[Why should this test fail?]]
  - *Test scope*: [[What exactly are we testing?]]
- [ ] T102 - 🔴 - [[Write failing test for edge cases]]
  - *Expected failure reason*: [[Why should this test fail?]]
- [ ] T103 - 🟢 - ⭐ [[Minimal implementation for happy path]]
  - *Success criteria*: T101 passes, others may still fail
- [ ] T104 - 🟢 - [[Implementation for edge cases]]
  - *Success criteria*: T101-T102 all pass
- [ ] T105 - ♻️ - [[Refactor for clarity and performance]]
  - *Validation*: All tests still pass, code quality improved
- [ ] T106 - ♻️ - [[Extract reusable components]]

**Validation Checkpoint**:
- [ ] All tests pass
- [ ] Code coverage meets threshold (≥60%)
- [ ] No code smells detected

### Cycle 2: [[Next Feature Name]]
**Acceptance Criteria**: [[Specific, testable requirements]]

- [ ] T201 - 🔴 - ⭐ [[Write failing test for integration]]
- [ ] T202 - 🔴 - [[Write failing test for error handling]]
- [ ] T203 - 🟢 - ⭐ [[Implement core functionality]]
- [ ] T204 - 🟢 - [[Implement error handling]]
- [ ] T205 - ♻️ - [[Optimize and clean up]]

**Validation Checkpoint**:
- [ ] All tests pass (including previous cycles)
- [ ] Code coverage meets threshold (≥60%)
- [ ] No code smells detected

### Cycle N: [[Additional Features]]
*Follow same pattern for remaining features*

## 🧪 Quality Assurance & Integration
- [ ] T801 - ⭐ Cross-feature integration tests
- [ ] T802 - Performance testing
- [ ] T803 - Security validation
- [ ] T804 - User acceptance testing
- [ ] T805 - Load/stress testing

## 📚 Documentation & Deployment
- [ ] T901 - API documentation
- [ ] T902 - User guide creation
- [ ] T903 - ⭐ Deployment procedures
- [ ] T904 - Monitoring setup
