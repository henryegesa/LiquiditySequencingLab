# Contributing to Liquidity Sequencing Lab (LSI)

Thank you for your interest in contributing to the Liquidity Sequencing Lab.  
This repository maintains rigorous standards for research quality, documentation clarity, and reproducibility.

---

## 🔧 Contribution Types Accepted

### 1. Research Contributions
- New ideas, concepts, or theoretical extensions of Liquidity Sequencing Infrastructure (LSI)
- Improvements to the sequencing graph, FOE, liquidity-time models
- New timing-based settlement frameworks

### 2. Code Contributions
- Simulation runners
- Model implementations
- Analytical tools for sequencing, timing, or corridor optimization

### 3. Documentation Contributions
- Architecture explanations
- Modeling notes
- Diagram improvements
- Corrections, clarifications, refinements

---

## 🧠 Principles

### **1. Precision > volume**
Every contribution must add clarity, correctness, or insight.

### **2. Reproducibility is mandatory**
Simulations must:
- define all parameters  
- document assumptions  
- include reproducible steps  
- store outputs inside `/src/simulations/results`

### **3. No vague ideas**
Every theoretical contribution must include:
- a concrete problem  
- a crisp insight  
- a structured explanation  
- implications for sequencing or settlement  

### **4. Diagrams must be source-editable**
All diagrams must include `.drawio`, `.svg`, or Figma source files.

---

## 📝 Folder Rules

### **/papers**
- Only refined work: abstracts, drafts, finals  
- Must follow academic writing conventions

### **/src/models**
- All model updates require:
  - definition of assumptions  
  - mathematical formulation  
  - pseudo-code  

### **/src/architecture**
- All architectural changes must describe:
  - the purpose of the component  
  - how it interacts with LSI  
  - how it impacts sequencing and settlement  

### **/src/simulations**
- Every scenario must be self-contained and reproducible  
- Runners must be clear and deterministic  
- Outputs must be small or summarized  

### **/notes**
- Free-form, but organized in the correct subfolder  

### **/diagrams**
- Must include editable source formats  

---

## 🔄 Process

### 1. Fork the repository  
Create a personal fork to prepare your changes.

### 2. Create a feature branch  
Use clear naming, e.g.:



### 3. Follow formatting + structure rules  
Markdown must be clean, readable, and structured with headers.

### 4. Submit a Pull Request  
Your PR must include:
- description of changes  
- motivation  
- instructions to reproduce (for simulations)  

### 5. Review & Merge  
Reviews prioritize correctness, clarity, and academic rigor.

---

## 🛡 Standards

- No broken links  
- No unreferenced diagrams  
- No unexplained variables  
- No ambiguous terminology  
- No unexplained assumptions  

Contributions failing these criteria will be rejected.

---

## 🙏 Acknowledgments
Contributors will be listed in `AUTHORS.md` when added.

