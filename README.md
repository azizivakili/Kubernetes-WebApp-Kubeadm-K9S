## Project Goal: Kubernetes, PostgreSQL and WebAPI: kubeadm, kubelet, k9s
I this project we will install and run Kubernetes using Kubeadm, kubelet and kubecetl.
We will run both master and worker node in same machine! (Ubuntu 22.04)
Then will create our two pods:
* One pod will run PostgreSQL
* Another pod will run our webAPI APP connecting to database to retrieve Database and its Tables

## Setup Kubernetes: 
Running both the Kubernetes master (control plane) and worker node on the same Ubuntu machine is great for testing and learning! 

* [Kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) is the recommended tool for bootstrapping Kubernetes clusters. 
* We need at least:
  * 2 CPUs and 2GB RAM (4GB+ recommended)
  * Docker or another container runtime installed (we’ll use containerd here)

### Installation (Single Node with Master + Worker)
#### Disable Swap
```
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab
```
#### Install Container Runtime (containerd)
```
sudo apt update && sudo apt install -y containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd
```
#### Load Kernel Modules & sysctl settings
```
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system
```

#### Install kubeadm, kubelet, kubectl
Note: Based of Kubernetes formal website, these instructions are for Kubernetes v1.32.

```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
```
Download the public signing key:
```
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
``` 
Add the appropriate Kubernetes apt repository:
```
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
#### Finally install:
```
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
Note: If problem with kubectl installation, then try [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) to install. 

### Install K9S:
K9S is a greate kubenetes management tool which can follow [k9s](https://dev.to/dm8ry/how-to-install-k9s-on-ubuntu-a-step-by-step-guide-2f98) to install it. 

## Create and run Pods!
We will go ahead with following structure:
```
azizi-k8s-project$ tree
.
├── db-init/
│   └── init.sql                                 # SQL script to initialize the database and create table
│
├── webapi/
│   ├── app.py                                   # Flask app to connect and query the database
│   └── Dockerfile                               # Dockerfile to containerize the Flask app
│
├── k8s/
│   ├── secret.yaml                              # Secret for PostgreSQL username and password
│   ├── db-init-config.yaml                      # ConfigMap with init.sql content to bootstrap the database
│   ├── db-deployment-service.yaml               # Combined Deployment and Service for the PostgreSQL database
│   ├── webapi-deployment-service.yaml           # Combined Deployment and Service for the Web API
│   └── ingress.yaml                             # Ingress to expose the Web API via HTTP
```
Here are files:
* db-deployment-service.yaml [here](k8s/db-deployment-service.yaml)
* webapi-deployment-service.yaml [here](k8s/webapi-deployment-service.yaml)
* secret.yaml [here](secret.yaml)
* db-init-config.yaml [here](k8s/db-init-config.yaml)
* ingress.yaml [here](k8s/ingress.yaml)
* app.py [here](webapi/app.py)
* Dockerfile [here](webapi/Dockerfile)
* init.sql [here](db-init/init.sql)



# Nice Commands

kubectl logs pod/webapi-deployment-58d4cfb8f7-lgp88

kubectl describe pod webapi-deployment-58d4cfb8f7-lgp88


# Troubleshooting
If docker error for permission: 
sudo usermod -aG docker $USER    






