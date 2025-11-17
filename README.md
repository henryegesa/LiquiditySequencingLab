# Liquidity Sequencing Lab (LSI)

The Liquidity Sequencing Lab houses the research, models, simulations, and system architecture behind **Liquidity Sequencing Infrastructure (LSI)** — a framework for organizing, sequencing, and settling money based on **time**, not only value.

LSI treats money as a *sequence of timed liquidity commitments* rather than isolated payment events. The lab explores how timing-aware financial infrastructure can reduce liquidity stress, optimize settlement, and make cross-border flows more efficient.

---

## 📚 Repository Structure

### **papers/**
Formal research outputs:
- abstracts  
- drafts  
- final papers  

### **src/**
Core research and engineering:
- **models/** — sequencing graphs, timing models, FOE algorithms  
- **architecture/** — system architecture for a timing-native settlement layer  
- **simulations/** — corridor tests, sequencing behavior, stress scenarios  

### **notes/**
Unfiltered thinking, research notes, and scratch work.

### **diagrams/**
All architecture diagrams, sequence graphs, and simulation figures.

---

## 🧠 Core Concepts

### **Liquidity Sequencing Infrastructure (LSI)**
A structured approach that sequences liquidity events in time to minimize timing mismatches, reduce stress, and optimize multi-rail settlement.

### **Sequencing Graph**
A graph where:
- nodes = liquidity events  
- edges = timing relationships  
- weights = value × time cost  

### **Flow Optimization Engine (FOE)**
An algorithmic engine that selects optimal execution paths across timing windows, corridors, FX environments, and settlement rails.

### **Liquidity-Time Curve**
A model encoding how available liquidity and expected obligations evolve over time.

---

## 🧪 Purpose of This Lab
- Model timing-based settlement behavior  
- Run corridor simulations (e.g., US → Kenya)  
- Develop sequencing algorithms  
- Produce publishable research  
- Document reference architecture for programmable liquidity systems  

---

## 🚀 Vision
Timing is the new capital.  
LSI provides the infrastructure for when money moves — not just where.

