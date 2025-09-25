---
build:
  prompt: |
    You are an engineer working with a senior architect to complete an Architecture Design Document. You MUST follow the guidelines shown in the document.

    Language: {{LANGUAGE}}
    Target Document: {{TARGET_DOCUMENT}}

    **Your Process (Execute Step by Step)**:

    1. **Language Setup**: Update {{TARGET_DOCUMENT}} with {{LANGUAGE}} and switch conversation to this language

    2. **Collaborative Design**: Read {{TARGET_DOCUMENT}} carefully, then propose your architecture design to the senior architect using a questioning approach. Ask only ONE question at a time to engage the architect and align the design. Update {{TARGET_DOCUMENT}} after each information gathering session.

    3. **Gap Analysis**: Carefully review {{TARGET_DOCUMENT}} completely and identify missing information. If gaps remain, return to step 2 for additional details.

    4. **Final Review**: Review and complete the checklist in {{TARGET_DOCUMENT}}

    **Your Architecture Focus**:
    - Analyze PRD requirements as foundation
    - Define clear component responsibilities and interfaces
    - Design data flow and communication patterns
    - Consider scalability, security, and performance
    - Ensure high-level focus, avoid implementation details

    **Engagement Style**: Use questioning to collaborate with the senior architect, asking one focused question at a time to build consensus on the architectural design.

    Begin with: "What are the key technical requirements from the PRD that should guide our architecture?"

---

# Architecture Design Document

**Guidelines**:
- **PRD Foundation**: Use PRD's requirements as your architectural foundation
- **Component Clarity**: Define clear responsibilities, interfaces, and dependencies for each component
- **High-Level Focus**: Focus on architectural design, avoid implementation details
- **Section Constraint**: Fill existing sections only - do not add new sections

**Table of Contents**
📋 Basic Information
🏗️ System Architecture
📊 Data Architecture
💻 Technology Stack
⚡ Performance & Scalability
🧪 Testing Strategy
✅ Review Checklist

**Fill-in language for `[[...]]` placeholders**: {{LANGUAGE}}

---

## 📋 Basic Information

**PRD Reference**: {{PATH_PRD}}

**Project Name**: [[From PRD - Product Name]]

---

## 🏗️ System Architecture

### C4 Architecture Level 1: System Context
*Consider how users interact with your system and what external systems are involved*
```mermaid
[[C4Context diagram showing system context - include users, main system, and external systems with their relationships]]
```

### C4 Architecture Level 2: Container Diagram
```mermaid
[[C4Container diagram showing internal containers/components, their technologies, and interactions]]
```

### Core Components
*List the main system components and their responsibilities*

- **[[Component Name]]**
  - Responsibility: [[What this component does]]
  - Interfaces: [[How other components interact with it]]
  - Dependencies: [[What this component relies on]]
- *Add more components as needed*

---

## 📊 Data Architecture

### Data Models
*Define the key data structures your system will work with*

```
[[Data structure definitions - can be schemas, entities, or data models]]
```

### Data Flow
*Describe how data moves through your system*

```
[[Data flow diagram or description showing data movement from input to output]]
```

### Storage Strategy
*Outline your data storage and persistence approach*

- **Storage Type**: [[Database, files, memory, etc.]]
- **Data Persistence**: [[How data is retained]]
- **Access Patterns**: [[How data is retrieved and updated]]

---

## 💻 Technology Stack

### Frontend (if applicable)
- **Framework/Library**: [[Your choice and reasoning]]
- **UI Components**: [[Component library or custom]]
- **State Management**: [[How you handle application state]]

### Backend (if applicable)
- **Runtime/Language**: [[Your choice and reasoning]]
- **Database**: [[Database type and why]]
- **API Design**: [[REST, GraphQL, etc.]]

### Development & Deployment
- **Build Tools**: [[Build and bundling tools]]
- **Testing Framework**: [[Testing approach and tools]]
- **Deployment**: [[How and where you deploy]]

---

## ⚡ Performance & Scalability

### Error Handling
*How your system will handle different types of errors*

- **[[Error Category 1]]**: [[How you handle this type of error]]
- **[[Error Category 2]]**: [[How you handle this type of error]]
- *Add more error types as needed*

### Performance Requirements
*Key performance metrics your system needs to meet*

- **[[Performance Metric 1]]**: [[Target value and reasoning]]
- **[[Performance Metric 2]]**: [[Target value and reasoning]]
- *Add more metrics as needed*

### Optimization Strategies
*Techniques you'll use to meet performance goals*

- **[[Strategy 1]]**: [[How this will improve performance]]
- **[[Strategy 2]]**: [[How this will improve performance]]
- *Add more strategies as needed*

### Scalability Considerations
*How your system can grow and evolve*

- **[[Scalability Aspect 1]]**: [[Your approach for future growth]]
- **[[Scalability Aspect 2]]**: [[Your approach for future growth]]
- *Add more considerations as needed*

---

## 🧪 Testing Strategy

### Testing Approach
*How you will verify your system works correctly*

- **[[Test Type 1]]**: [[What and how you'll test]]
- **[[Test Type 2]]**: [[What and how you'll test]]
- *Add more test types as needed*

### Quality Gates
*Standards your system must meet before release*

- **[[Quality Metric 1]]**: [[Target threshold]]
- **[[Quality Metric 2]]**: [[Target threshold]]
- *Add more quality gates as needed*

---

## ✅ Review Checklist

- [ ] All PRD FR requirements have corresponding architectural components
- [ ] All PRD NFR requirements have corresponding technical solutions
- [ ] Architecture design supports all user stories in PRD
- [ ] Technology selection meets PRD compatibility requirements
- [ ] Performance design satisfies PRD performance requirements
- [ ] Error handling strategy covers all error scenarios in PRD
- [ ] Testing strategy can verify PRD acceptance criteria
- [ ] Architecture has scalability for PRD-implied expansion needs
- [ ] Component interfaces and dependencies are clearly defined
- [ ] Data flow and storage strategies align with functional requirements
- [ ] Technology stack choices are justified based on requirements
