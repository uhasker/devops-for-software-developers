## Terminology

Kubernetes is an **orchestrator**, i.e. a system that deploys applications and dynamically responds to changes.

Deploying an application with Docker + Kubernetes has the following advantages compared to the simple setup from part I:

- applications can be automatically scaled up (or down) based on demand
- applications can self-heal when something breaks
- zero-downtime rolling updates and rollbacks can be performed

A Kubernetes **cluster** consists of one or more **nodes** that provide resources (CPU, memory, ...) for applications.
Basically, the nodes are the physical machines (e.g. an AWS or Hetzner instance or your local machine).

**Worker nodes** run applications, while **cluster nodes** implement the Kubernetes intelligence.

**Pods** are the basic Kubernetes units.
They wrap containers and execute on nodes.

The **desired state** is what you want, the **observed state** is what you have and they should always match.
If they don't match, a **controller** starts a **reconciliation** process to bring them into sync.
The **declarative model** means that we just tell Kubernetes about our desired state (the "what") and leave the "how" to Kubernetes.

Deployment allow you to perform zero-downtime rolling updates (rollouts).
They work if your apps are:

1. Loosely coupled via APIs
2. Backward and forward compatible
