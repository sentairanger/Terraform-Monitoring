# Terraform-Monitoring

## Introduction

This project is an extension of [this](https://github.com/sentairanger/Dual-Robot-Monitoring/) project that I did back in 2021. At the time I thought this was the most ambitious project I ever did. But this time I used Terraform for infrastructure provisioning and Ansible for Configuration Automation. Both of these platforms compliment each other since Ansible will configure the hosts on the cloud while Terraform provisions the infrastructure. This application has been tested locally, however this can run on the cloud as well. 

## Getting Started

To get started first install the following required applications. The `playbook` directory includes the playbooks to install the required applications. However, the following platforms need to be installed manually. Follow the instructions depending on your OS or cloud instance.

* [Docker](https://docs.docker.com/engine/install/)
* [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html)

Note: You can use any Kubernetes platform you want, just make sure to follow the syntax based on your platform.

## Explaining the Layers

Now, let's cover the layers of the application as I've done before. This time there are newer layers we will discuss. 

### Code

The main code is found under the `terraform-docker/app` directory. The main application is a Flask Web application that controls two robots. The screenshot below shows the design. To use this application with a phone or tablet on Firefox or Chrome, change `mouseup` and `mousedown` in `logic.js` to `touchstart` and `touchend`.

![App](https://github.com/sentairanger/Terraform-Monitoring/blob/main/images/app.png)

### Docker

The `terraform-docker` directory contains the `providers.tf` file that includes the Docker provider. This is required to build and run the image. The `main.tf` file runs and builds the main application. First run `terraform init` to install the provider. Then run `terraform plan` to plan the build. Then run `terraform apply` and check to see the image was built with `docker ps`. Then go to `localhost:5000` or `<ip-address>:5000`. If it runs correctly then destroy the running container with `terraform destroy`. Then go to Dockerhub to create a repository named `terraform-monitoring`. The `playbook/docker-push.yml` playbook will log you into Dockerhub (be sure to add your username and password), then will tag the image (be sure to change the username linuxrobotgeek to your username) and then log you out.

### Kubernetes

The `terraform-kubernetes` directory also contains the `providers.tf` and `main.tf` files to install the Kubernetes provider and deploy the cluster for testing. As usual first run `terraform init`. Then run `terraform plan` to initiate the cluster. Then deploy with `terraform apply`. Test the cluster to make sure it works before proceeding. Delete the cluster after testing with `terraform destroy`.

### GitHub Actions

The `workflows` directory contains workflows to update the Docker image any time new changes are pushed into Dockerhub.

### ArgoCD

ArgoCD deploys changes pushed by Github Action. The screenshot below shows an example deployment. To run this deployment first have ArgoCD installed and then go under the `terraform-argocd-nodeport` first and then run `terraform init`, `terraform plan` and `terraform apply`. Then the nodeport should be created. Then go to the `playbook` directory and then run `ansible-playbook argocd/argocd-port.yml`. Go to `localhost:30007` and then login with `admin` and use the password generated from the installation. Then go to the `terraform-argocd` directory and run `terraform init`, `terraform plan` and `terraform apply` as before. Then the cluster should appear in the UI. Click on Sync to sync the application.

![ArgoCD](https://github.com/sentairanger/Terraform-Monitoring/blob/main/images/argocd.png)

### Ansible

Ansible is used for configuration management. The `playbooks` directory contains all the relevant playbooks to install and run services. 

### Terraform

Terraform is used for infrastructure provisioning. The `.tf` files are either used to install the providers or deploy our services. The diagram below shows how our application is deployed from a local PC to the cloud.

![terraform](https://github.com/sentairanger/Terraform-Monitoring/blob/main/images/Terraform.drawio(1).png)

### Prometheus

Prometheus is used to scrape applications and gather metrics. The screenshot below shows the cluster being scraped by Prometheus in port 9090. To run Prometheus first have it installed with Ansible and then go to the `playbooks` directory and run `ansible-playbook prometheus/prometheus.yml`. Then go to `localhost:9090` or `<ip-address>:9090`. Then go to Status and then Targets. If it appears with no errors then it is working.

![Prometheus](https://github.com/sentairanger/Terraform-Monitoring/blob/main/images/prometheus.png)

### Grafana

To gather metrics first make sure the cluster is running either from the `terraform-kubernetes` or `terraform-argocd` directory and then go to `playbooks` and run `ansible-playbook kubernetes/port-forward.yml`. Change `5000` to `5000:5000` if running remotely. Then go to `localhost:5000` or `<ip-address>:5000`. Test out the application and move the robots. Then on another terminal go to `playbooks` again and run `ansible-playbook grafana/grafana.yml`. Go to `localhost:3000` or `<ip-address>:3000`. Log in with `admin` and `prom-operator`. Then import the dashboard provided in the `grafana` directory. Then the dashboard should appear as shown below.

![grafana](https://github.com/sentairanger/Terraform-Monitoring/blob/main/images/grafana.png)

## Deploying on the Cloud

While this works locally, Terraform works in the cloud as well. Here are three cloud solutions that would be able to deploy this application.

### AWS

To deploy on AWS first follow [this](https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks) tutorial to provision an EKS cluster and install `kubectl`.

### Azure

To deploy on Azure first follow [this](https://developer.hashicorp.com/terraform/tutorials/kubernetes/aks) tutorial to provision an AKS cluster and install `kubectl`.

### Google Cloud

To deploy on Google Cloud first follow [this](https://developer.hashicorp.com/terraform/tutorials/kubernetes/gke) to provision a GKE cluster and install `kubectl`.

## Compatibility with other Frameworks

This Monitoring System can be modified to be used in any other framework provided that the following is true:

* The web framework supports remote GPIO access. This includes `pigpio-client` for Nodejs or `diozero` for Java for example. Some languages like Java do not support multiple Pi hosts so be aware of those limitations.
* The web framework has a library for Prometheus such as `express-prometheus-middleware` for Nodejs.

This has been tested and should work on the following:

* Django
* Pyramid
* Nodejs
* Spring Boot



