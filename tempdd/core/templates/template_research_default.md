---
build:
  prompt: |
    This agent specializes in gathering practical implementation information through systematic web research and documentation analysis. Your task is completing a research document to gather all information needed for development. You ALWAYS MUST follow the guidelines shown in the document.

    Target Document: {{TARGET_DOCUMENT}}

    **Core Responsibilities**:
    - **Web Research Execution**: Perform extensive web searches for architecture, development tools, and implementation best practices
    - **Resource Collection**: Gather and organize URLs, documentation, code examples, and technical resources
    - **Implementation Analysis**: Focus research on practical development needs and implementation concerns
    - **Progressive Research**: Execute 5-step research process with documentation updates after each step

    **Research Excellence Standards**:
    - Collect and verify all source URLs for accuracy
    - Provide working code examples and configuration samples
    - Focus on practical implementation rather than theoretical concepts
    - Document complexity and risk assessments for each component
    - Build a comprehensive resource library for development teams

---

# Development-Focused Research Document

**Guidelines**:
- **Implementation Focus**: Gather practical information needed for development
- **Sequential Steps**: Complete each step in order before moving to the next
- **Resource Collection**: Collect relevant URLs, documentation, and examples
- **Development Ready**: Build sufficient detail to start implementation

**Table of Contents**
📋 Basic Information
🔍 Step 1: Development and Architecture Information Collection
🧩 Step 2: Components and Packages Planning
❓ Step 3: Implementation Questions and Concerns
🔗 Step 4: Resource URLs for Question Resolution
📖 Step 5: Detailed Research Analysis and Solutions
🚀 Development Readiness Assessment
✅ Research Completion Validation

**Fill-in `[[...]]` placeholders with appropriate content**

---

## 📋 Basic Information

**PRD Reference**: {{PATH_PRD}}

**Architecture Reference**: {{PATH_ARCH}}

**Project Name**: [[From PRD - Product Name]]

---

## 🔍 Step 1: Development and Architecture Information Collection

### 1.1 Architecture Research Findings
*Web search and compile architectural patterns and implementation approaches*

**Architecture Patterns**:
- [[Pattern 1]]: [[Details and use cases]]
- [[Pattern 2]]: [[Details and use cases]]
- *Add more patterns as needed*

**Technology Stack**:
- [[Technology 1]]: [[Pros/cons and implementation notes]]
- [[Technology 2]]: [[Pros/cons and implementation notes]]
- *Add more technologies as needed*

**Research Sources**:
- [[URL 1]]: [[Brief description]]
- [[URL 2]]: [[Brief description]]
- *Add more sources as needed*

**Summary**:
[[Key findings and architectural decisions]]

### 1.2 Development Framework and Tools Research
*Web search research on development tools and frameworks*

**Framework Analysis**:
- [[Framework 1]]: [[Key features and suitability]]
- [[Framework 2]]: [[Key features and suitability]]
- *Add more frameworks as needed*

**Development Tools**:
- **Build Tools**: [[Selected tools and reasoning]]
- **Testing**: [[Testing approach and tools]]
- **Development Environment**: [[Setup requirements]]
- **Deployment**: [[Deployment strategy]]

**Research Sources**:
- [[URL 1]]: [[Brief description]]
- [[URL 2]]: [[Brief description]]
- *Add more sources as needed*

**Summary**:
[[Development toolchain decisions and rationale]]

### 1.3 Update Status
- [ ] Architecture patterns research completed
- [ ] Technology stack analysis finished
- [ ] Development framework research completed
- [ ] All relevant URLs collected and categorized
- [ ] Research findings organized for development use

---

## 🧩 Step 2: Components and Packages Planning

### 2.1 Required Components Analysis

**Frontend Components**:
- [[Component Name]]: [[Purpose and functionality]]
  - Dependencies: [[List of dependencies]]
  - Complexity: [[High/Medium/Low]]
- *Add more frontend components as needed*

**Backend Components** (if applicable):
- [[Component Name]]: [[Purpose and functionality]]
  - Dependencies: [[List of dependencies]]
  - Complexity: [[High/Medium/Low]]
- *Add more backend components as needed*

### 2.2 Required Packages and Libraries

**Essential Packages**:
- [[Package Name]] (v[[version]]): [[Purpose and justification]]
- [[Package Name]] (v[[version]]): [[Purpose and justification]]
- *Add more packages as needed*

**Development Dependencies**:
- [[Package Name]] (v[[version]]): [[Purpose and justification]]
- [[Package Name]] (v[[version]]): [[Purpose and justification]]
- *Add more dev dependencies as needed*

### 2.3 Technology Stack Summary

**Programming Languages**: [[List with versions and reasoning]]

**Frameworks**: [[Selected frameworks with versions]]

**Database** (if applicable): [[Type and version]]

**Infrastructure**: [[Deployment and hosting approach]]

### 2.4 Update Status
- [ ] Required components identified and documented
- [ ] Package dependencies mapped and versioned
- [ ] Technology stack finalized
- [ ] Component complexity assessed

---

## ❓ Step 3: Implementation Questions and Concerns

### 3.1 Critical Implementation Questions

**Technical Questions**:
- [[Technical question 1]]
  - Impact: [[High/Medium/Low]]
  - Risk if unresolved: [[Description]]
- [[Technical question 2]]
  - Impact: [[High/Medium/Low]]
  - Risk if unresolved: [[Description]]
- *Add more technical questions as needed*

**Integration Questions**:
- [[Integration question 1]]
  - Dependencies affected: [[List]]
  - Risk if unresolved: [[Description]]
- [[Integration question 2]]
  - Dependencies affected: [[List]]
  - Risk if unresolved: [[Description]]
- *Add more integration questions as needed*

**Performance Questions** (if applicable):
- [[Performance question 1]]
  - Expected load: [[Description]]
  - Risk if unresolved: [[Description]]
- *Add more performance questions as needed*

**Security Questions** (if applicable):
- [[Security question 1]]
  - Security level required: [[High/Medium/Low]]
  - Risk if unresolved: [[Description]]
- *Add more security questions as needed*

### 3.2 Update Status
- [ ] Critical technical questions identified
- [ ] Impact and risk assessment completed
- [ ] Questions prioritized by importance
- [ ] Dependencies and affected components mapped

---

## 🔗 Step 4: Resource URLs for Question Resolution

### 4.1 Technical Documentation URLs

**Official Documentation**:
- [[Package/Framework Name]]: [[URL]] - [[Relevant sections]]
- [[Package/Framework Name]]: [[URL]] - [[Relevant sections]]
- *Add more documentation as needed*

**API References**:
- [[API Name]]: [[URL]] - [[Relevant endpoints/methods]]
- *Add more API references as needed*

### 4.2 Tutorial and Guide URLs

**Implementation Guides**:
- [[Guide Title]]: [[URL]] - [[Relevance to questions]]
- [[Guide Title]]: [[URL]] - [[Relevance to questions]]
- *Add more guides as needed*

**Best Practices**:
- [[Best Practice Guide]]: [[URL]] - [[Application to project]]
- *Add more best practices as needed*

### 4.3 Code Examples and Repositories

**Sample Projects**:
- [[Project Name]]: [[URL]] - [[Similar functionality]]
- *Add more sample projects as needed*

**Code Snippets**:
- [[Snippet Source]]: [[URL]] - [[Implementation pattern]]
- *Add more code snippets as needed*

### 4.4 Update Status
- [ ] Relevant documentation URLs collected
- [ ] Tutorial and guide resources identified
- [ ] Code examples and repositories catalogued
- [ ] URLs mapped to specific questions

---

## 📖 Step 5: Detailed Research Analysis and Solutions

### 5.1 Technical Implementation Solutions

**Q**: [[Question from Step 3]]
**Research Sources**: [[List of URLs consulted]]
**A**: [[Answer with implementation details]]
**Sample Code**:
```[[language]]
[[Code example demonstrating the solution]]
```
**Additional Notes**: [[Important considerations]]

*Add more Q&A pairs as needed*

### 5.2 Integration Solutions (if applicable)

**Q**: [[Integration question from Step 3]]
**Research Sources**: [[List of URLs consulted]]
**A**: [[Integration approach with steps]]
**Sample Code**:
```[[language]]
[[Code example showing integration pattern]]
```
**Configuration Example**:
```[[format]]
[[Configuration settings or setup instructions]]
```

*Add more integration solutions as needed*

### 5.3 Performance Solutions (if applicable)

**Q**: [[Performance question from Step 3]]
**Research Sources**: [[List of URLs consulted]]
**A**: [[Performance optimization strategies]]
**Sample Code**:
```[[language]]
[[Performance-optimized code example]]
```
**Benchmarking Approach**: [[How to measure and validate performance]]

*Add more performance solutions as needed*

### 5.4 Security Solutions (if applicable)

**Q**: [[Security question from Step 3]]
**Research Sources**: [[List of URLs consulted]]
**A**: [[Security implementation approach]]
**Sample Code**:
```[[language]]
[[Secure implementation example]]
```
**Security Checklist**: [[Verification steps for security measures]]

*Add more security solutions as needed*

### 5.5 Update Status
- [ ] Questions answered with detailed research
- [ ] Sample code provided for each solution
- [ ] Implementation approaches validated
- [ ] Additional considerations documented

---

## 🚀 Development Readiness Assessment

### Implementation Plan Summary
[[Overview of the implementation approach based on research findings]]

### Technology Decisions Validated
- **Frontend**: [[Technology choices with justification]]
- **Backend** (if applicable): [[Technology choices with justification]]
- **Database** (if applicable): [[Technology choices with justification]]
- **Infrastructure**: [[Technology choices with justification]]

### Resource Inventory
- **Documentation**: [[Count]] resources identified
- **Code Examples**: [[Count]] samples collected
- **Tutorials**: [[Count]] guides available
- **Best Practices**: [[Count]] guidelines to follow

### Risk Mitigation
- **High Priority Risks**: [[List with mitigation strategies]]
- **Medium Priority Risks**: [[List with mitigation strategies]]
- **Monitoring Requirements**: [[What to track during development]]

### Development Confidence
- **Technical Feasibility**: [[High/Medium/Low]] - [[Justification]]
- **Resource Adequacy**: [[High/Medium/Low]] - [[Justification]]
- **Timeline Realism**: [[High/Medium/Low]] - [[Justification]]
- **Success Probability**: [[High/Medium/Low]] - [[Justification]]

---

## ✅ Research Completion Validation

### Step-by-Step Completion Check
- [ ] **Step 1**: Development and Architecture research completed
- [ ] **Step 2**: Components and packages identified and planned
- [ ] **Step 3**: Implementation questions raised and categorized
- [ ] **Step 4**: URL resources collected for questions
- [ ] **Step 5**: Research conducted with solutions and code samples

### Quality Assurance
- [ ] Questions have research-backed answers
- [ ] Sample code provided for critical implementation areas
- [ ] `[[...]]` placeholders replaced with actual content
- [ ] Resource URLs verified and accessible
- [ ] Implementation approach clearly documented

### Development Readiness
- [ ] Technical approach validated through research
- [ ] Major risks identified with mitigation strategies
- [ ] Resource library available for reference
- [ ] Development can commence with confidence
- [ ] Success criteria and validation methods defined

**Final Readiness Status**: [[READY/NOT READY]] - [[Justification based on completion criteria]]