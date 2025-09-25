---
build:
  prompt: |
    You are a Product Manager speaking with a stakeholder to complete a comprehensive PRD. You ALWAYS MUST follow the guidelines shown in the document.

    Language: {{LANGUAGE}}
    Target Document: {{TARGET_DOCUMENT}}

    **Your Systematic Approach (Execute Step by Step)**:

    1. **Language Setup**: Update {{TARGET_DOCUMENT}} with {{LANGUAGE}} and switch the conversation to this language.

    2. **Discovery Phase**: Ask the stakeholder "What do you want to build today?" to get an overview of their vision. Use their response to begin filling {{TARGET_DOCUMENT}} with initial product information.

    3. **Iterative Information Gathering**: Systematically identify missing information in the PRD. Use targeted questioning to fill gaps - ask only ONE question at a time for clarity. After each answer, immediately update {{TARGET_DOCUMENT}} before asking the next question.

    4. **Completeness Validation**: Carefully review {{TARGET_DOCUMENT}} completely. If any information is still missing or unclear, return to step 3 to gather additional details until the PRD is comprehensive.

    5. **Final Review**: Complete the review checklist in {{TARGET_DOCUMENT}} to ensure all requirements are met.

    **Your Product Manager Expertise - Focus On**:
    - Understanding the core problem and user pain points
    - Identifying target user personas and their needs
    - Defining measurable success criteria and business value
    - Gathering detailed functional and non-functional requirements
    - Documenting dependencies, assumptions, and constraints
    - Structuring requirements as Epics → User Stories with acceptance criteria

    **Quality Standards**:
    - Replace ALL `[[...]]` placeholders with specific, actionable information
    - Keep focus on user value, avoid technical implementation details
    - Write clearly for non-technical stakeholders
    - Ensure all requirements are testable and measurable
    - Use SMART criteria for goals and success metrics

    Begin with: "What do you want to build today? Tell me about the problem you're trying to solve for your users."

---

# Product Requirements Document (PRD)

**Guidelines**:
- **Content Rules**: Replace all `[[...]]` placeholders; no implementation details; focus on user value; written for non-technical stakeholders
- **Clarity Requirements**: Don't guess - use [NEEDS CLARIFICATION: specific question] for ambiguities; requirements must be testable; success criteria must be measurable
- **Structure**: Epic (user value theme) → User Story (specific implementation)
- **Scope**: Clearly bounded with identified dependencies and assumptions
- **MUST: Section Constraint**: Only fill existing sections - DO NOT add any new sections to this template

**Fill-in language for `[[...]]` placeholders**: {{LANGUAGE}}

---

## 📋 Basic Information

**Product Name**: [[Product Name]]

---

## 🎯 Objective & Goals

### Goals
*Use SMART principles (Specific, Measurable, Achievable, Relevant, Time-bound) to define clear objectives*

[[Primary goal description]]

### Why

[[Business rationale and problem statement]]

### What

[[Solution overview and key features]]

---

## 📝 User Scenarios

### Epic 

- **E1**: [[Epic 1 Name]]
  - Description: [[Epic 1 detailed description]]
  - Business Value: [[What this Epic contributes]]
  - Success Criteria:
    - [[Measurable Epic-level success criterion 1]]
    - [[Measurable Epic-level success criterion 2]]
- **E2**: [[Epic 2 Name]]
  - ...

### User Stories

- **E1S1**: [[Name of Story 1 of Epic 1]]
  - Description: **As a** [[User Type]], **I want** [[Feature Requirement]], **so that** [[Achieve Goal]]
  - Acceptance Criteria:
    -  **Given** [[initial state]], **When** [[action]], **Then** [[expected outcome]]
    -  **Given** [[initial state]], **When** [[action]], **Then** [[expected outcome]]
- **E1S2**: [[Name of Story 2 of Epic 1]]
  - ...

---

## ⚙️ Requirements
*FR (functional) with input/output specs; NFR (performance <200ms, throughput >1000 QPS, concurrent users)*

### Functional Requirements

- **FR001**: [[Functional requirements description]]
  - Input: [[Input description]]
  - Processing Logic: [[Processing logic description]]
  - Output: [[Output description]]
  - Error Handling: [[Error handling description]]
- **FR002**: [[Feature description]]
  - Input: [[Input description]]
  - Processing Logic: [[Processing logic description]]
  - Output: [[Output description]]
  - Error Handling: [[Error handling description]]

### Non-Functional Requirements (Performance, Availability, Scalability, Security, or Compatibility)

- **NFR001**: [[Non-functional requirements description]]
- **NFR002**: [[Non-functional requirements description]]

---

## 🔗 Dependencies and Assumptions

### Dependencies
[[List external dependencies, services, or requirements needed]]

### Assumptions
[[List key assumptions about users, technology, or business context]]

### Technical Constraints
[[List technical limitations or constraints that impact the solution]]

---

## ✅ Review Checklist (for this document)

- [ ] All `[[...]]` placeholders replaced with actual content
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified
