# ☸️ Kubernetes Pod Scaling with HPA (FastAPI Demo)

---

## 🎯 **Objective**

**Showcase dynamic scaling of a FastAPI app on Kubernetes using Horizontal Pod Autoscaler (HPA), scaling pods up and down based on CPU load.**

---

## 🛠️ **Setup Overview**

- **Dockerize** a FastAPI app that simulates CPU load on requests.
- **Deploy** on Minikube or any managed K8s cluster.
- **Add HPA config**:  
  - CPU-based scaling rules  
  - Replicas auto-scale from 1 to 10 based on traffic
- **Monitor** scaling with `kubectl top` or Kubernetes dashboard.

---

## 📦 **Deliverables**

- [ ] **K8s YAMLs** for deployment, service, and HPA
- [ ] **Video** showing traffic-based scale-up/down
- [ ] **Commands used** for setup and monitoring
- [ ] **CPU load scripts** for traffic simulation

---

## 🌈 **Main Things To Do (Highlights)**

---

### 1. **Dockerize the FastAPI App**
- Create a simple FastAPI app with a CPU-intensive endpoint.
- Containerize the app for K8s deployment.

---

### 2. **Write Kubernetes YAMLs**
- **Deployment:**  
  - Set resource requests/limits for CPU.
- **Service:**  
  - Expose your app for cluster or external access.
- **HPA:**  
  - Configure autoscaler (min 1, max 10 pods, CPU target).

---

### 3. **Deploy to Kubernetes**
- Apply all YAMLs using `kubectl`.
- Ensure pods and service are running.

---

### 4. **Simulate Load**
- Use a script to generate high CPU load via traffic (many requests).
- Observe CPU usage rise.

---

### 5. **Monitor Scaling**
- Watch pods scale up with `kubectl get hpa` and `kubectl top pods`.
- Optionally use the Kubernetes dashboard for a visual view.
- After stopping load, watch pods scale back down.

---

### 6. **Record and Document**
- Record a short video showing scaling events in real-time.
- List all commands/scripts you used for setup, deployment, load generation, and monitoring.

---

## 🌈 **Tech Stack**

| Layer         | Tools                    |
|---------------|-------------------------|
| API           | **FastAPI**             |
| Container     | **Docker**              |
| Orchestration | **Kubernetes (Minikube)**|
| Scaling       | **HPA**                 |
| Monitoring    | **kubectl** / Dashboard |


## 🚀 **Summary Table**

| Step                 | What to Do                               |
|----------------------|------------------------------------------|
| Dockerize App        | FastAPI + Docker                         |
| Write YAMLs          | Deployment, Service, HPA                 |
| Deploy to K8s        | `kubectl apply -f ...`                   |
| Simulate Traffic     | CPU load script (Python, Bash, etc.)     |
| Monitor Scaling      | `kubectl top`, dashboard                 |
| Record & Document    | Video, commands, load scripts            |

---

> **Tip:**  
> Use emojis, markdown tables, and bold color sections to make your documentation pop!
>  
> For extra clarity, include diagrams and screenshots in your deliverable.

---