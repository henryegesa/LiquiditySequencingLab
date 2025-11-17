# Core LSI Architecture Diagram (Text Description)

The architecture can be visualized as a left-to-right flow:

Client / Payroll / Remittance Systems  
    → Ingress Adapters  
    → Event Normalizer  
    → Sequencing Engine (LSI Core)  
    → Settlement & Routing Layer  
    → External Rails / Wallets / Ledgers

Monitoring, observability, and admin consoles sit alongside all layers.

A proper visual diagram should be stored in `/diagrams/core_architecture.drawio` or similar, referenced here.

