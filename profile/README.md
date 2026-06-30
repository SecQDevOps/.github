<div align="center">
  <img src="https://secqdevops.eu/wp-content/uploads/2025/12/SecQDevOps-web.png" alt="SecQDevOps Logo" width="400"/>

  ### Trustworthy Quantum DevOps for Secure Software and Hardware Engineering
  
  [![Website](https://img.shields.io/badge/Website-secqdevops.eu-blue?style=flat-square)](https://secqdevops.eu/)
  [![Horizon Europe](https://img.shields.io/badge/EU_Funding-Horizon_Europe-yellow?style=flat-square)](https://cordis.europa.eu/project/id/101225776)
</div>

---

Welcome to the official GitHub organization for **SecQDevOps** (Secure Quantum Development and Operations). 

We are an EU-funded research and engineering consortium dedicated to building a secure, continuous DevOps pipeline for quantum software and hardware. As the quantum computing landscape accelerates, we are bridging the critical gap between rapid quantum development and robust, quantum-specific security infrastructures.

## 🚀 Coming Soon: QNODE (Quantum Network Orchestration & Decomposition Engine)

Currently in active development, **QNODE** is our flagship distributed quantum-circuit simulation network. 

Designed for massive scalability, QNODE leverages advanced tensor network slicing to decompose complex quantum circuits into independent tasks. This allows for highly parallelized edge execution without the overhead of inter-node communication. 

### System Architecture

```mermaid
flowchart TB
    researcher(["Researcher / User<br/>«person»<br/>submits quantum circuits, retrieves results"]):::person
    volunteer(["Volunteer Operator<br/>«person»<br/>donates a machine's CPU/RAM/GPU"]):::person

    qnode["QNODE<br/>«software system»<br/>Quantum Network Orchestration &amp; Decomposition Engine.<br/>Cuts large quantum circuits into independent tasks, distributes<br/>them to volunteer edge nodes, and reduces the partial results<br/>into a final answer."]:::focus

    researcher -->|"uploads OpenQASM circuits, polls status, downloads results (HTTPS)"| qnode
    volunteer -->|"runs an Edge Worker that pulls tasks and returns results (HTTPS)"| qnode

    classDef focus fill:#fb8500,stroke:#b35900,color:#fff,stroke-width:2px
    classDef person fill:#2da44e,stroke:#176f2c,color:#fff
```

**Open Source Commitment:**
The entire QNODE platform is designed to be **100% open-source**. We recently reached our MVP milestone and are currently optimizing the network and conducting a rigorous Supply Chain License review. 

Once these audits are complete, the repositories will be made public here. Watch this space!

## 📦 Repository Map

| Repository | Language/Tech | Role |
|-----------|--------------|------|
| [qnode-backend-gateway](https://github.com/SecQDevOps/qnode-backend-gateway) | Go | HTTP API gateway; entry point for circuit submission and result retrieval |
| [qnode-backend-orchestrator](https://github.com/SecQDevOps/qnode-backend-orchestrator) | Python | Temporal-based workflow orchestration; manages circuit decomposition and task distribution |
| [qnode-backend-slicer](https://github.com/SecQDevOps/qnode-backend-slicer) | Python | Tensor network slicing; decomposes quantum circuits into independent contractions |
| [qnode-backend-reducer](https://github.com/SecQDevOps/qnode-backend-reducer) | Rust | High-performance result aggregation; combines partial results from edge workers |
| [qnode-edge-worker](https://github.com/SecQDevOps/qnode-edge-worker) | Go | Edge node agent; pulls tasks from the network and computes tensor contractions |
| [qnode-tooling-frontend](https://github.com/SecQDevOps/qnode-tooling-frontend) | TypeScript | Web UI for researchers; submit circuits, monitor jobs, retrieve results |
| [qnode-at-home](https://github.com/SecQDevOps/qnode-at-home) | Python/Go | Volunteer installation and management; easy deployment for edge node operators |

## 🔬 Our Core Pillars

* **Security by Design:** Automated security assessments and real-time vulnerability detection for quantum algorithms.
* **Quantum Engineering:** Hardware-aware compilers and high-level programming workflows powered by tools like Eclipse Qrisp.
* **Distributed Quantum Execution:** Orchestrating edge infrastructure to securely distribute and compute massive quantum tasks via QNODE.

---

*This work has received funding from the European Union under the Horizon Europe Research and Innovation Programme (Grant Agreement No. 101225776).*