# Security Policy
Liquidity Sequencing Lab (LSI)

This repository contains research, models, and architectural documentation for timing-based settlement and liquidity sequencing systems. While no production systems exist in this repo, responsible security behavior is required.

---

## 1. Reporting Vulnerabilities

If you discover a potential security issue—conceptual, architectural, or code-related—report it privately.

### Report via:
- Direct message to **Henry Maloba**  
- GitHub private disclosure (if enabled)  

Do **not** open a public issue for sensitive vulnerabilities.

Your report should include:
- Description of the issue  
- Files or models affected  
- Steps to reproduce (if applicable)  
- Any recommended mitigation  

---

## 2. Responsible Disclosure Guidelines

- Do not exploit or weaponize any vulnerabilities found.  
- Do not publish vulnerabilities prior to coordinated disclosure.  
- Provide adequate detail for replication and validation.  

---

## 3. Scope

### **In Scope**
- Model implementations  
- Simulation runners  
- Architecture diagrams  
- Theoretical constructs that imply system weaknesses  
- Any prototype code that may be added in future  

### **Out of Scope**
- Personal data (none is stored here)  
- Production rail integrations (not part of this repo)  
- External services referenced conceptually  

---

## 4. Security Expectations for Contributors

All contributors must:
- Avoid introducing insecure patterns  
- Document assumptions clearly  
- Build models that do not encourage unsafe real-world deployment  
- Never include confidential keys, tokens, sample API credentials, or proprietary data  

---

## 5. Handling of Sensitive Research

Some architectural ideas may imply:
- systemic risks  
- timing-based attack vectors  
- liquidity exhaustion strategies  
- settlement timing manipulation  

Such insights must be:
- documented responsibly  
- reviewed privately before publication  
- included in commit history only in sanitized form  

---

## 6. Simulation Safety

Simulation outputs must **not** contain:
- personally identifiable information  
- sensitive financial datasets  
- real account numbers  
- confidential transaction flows  

Only synthetic or anonymized data is permitted.

---

## 7. Maintainer Responsibilities

The maintainer (Henry Maloba) commits to:
- reviewing vulnerability reports  
- responding within a reasonable timeline  
- determining severity  
- coordinating responsible disclosure  
- enforcing repository security standards  

---

## 8. Final Notes

Security is integral to LSI’s mission.  
All researchers and contributors must prioritize safe, responsible use of theoretical and simulation-based insights.

