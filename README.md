# CloudSearch — Dockerized Flask App on Amazon ECS Fargate

A containerized web application deployed end-to-end on AWS using Docker, Amazon ECR, Amazon ECS (Fargate), and an Application Load Balancer — fully provisioned via AWS CLI and shell scripts (no console clicking, no Infrastructure-as-Code tooling). Includes auto-scaling and a CI/CD pipeline with GitHub Actions.

**Live demo:** http://cloudsearch-alb-1824399561.us-east-1.elb.amazonaws.com
**Repo:** https://github.com/johan06-cloud/ecs-docker-project

---

## What it does

CloudSearch is a Google-style search page (animated rotating Earth, starfield background) with a mock `/search` endpoint that returns sample results for any query. The app itself is intentionally simple — the focus of this project is the deployment pipeline and infrastructure around it, not the application logic.

## Architecture

```
GitHub (push to main)
        │
        ▼
GitHub Actions ──► builds Docker image ──► pushes to Amazon ECR
        │
        ▼
   Amazon ECS (Fargate)
        │
        ▼
Application Load Balancer  ◄── Internet
        │
        ▼
  ECS Service (1–3 tasks, auto-scaled on CPU)
        │
        ▼
  Flask container (gunicorn) on port 5000
```

**Networking:** Custom VPC (`10.1.0.0/16`) with two public subnets across `us-east-1a` / `us-east-1b`, an Internet Gateway, and a public route table. Fargate tasks run in public subnets with public IPs assigned (no NAT Gateway — keeps this fully within the AWS Free Tier).

**Security:** Two security groups — one for the ALB (allows HTTP/80 from the internet), one for the ECS tasks (allows port 5000 only from the ALB's security group, not the open internet).

## Services used

| Service | Purpose |
|---|---|
| **Docker** | Containerizes the Flask app |
| **Amazon ECR** (Elastic Container Registry) | Stores the Docker image |
| **Amazon ECS** (Elastic Container Service) | Runs the container on Fargate (serverless — no EC2 instances to manage) |
| **Application Load Balancer** | Routes public traffic to healthy container tasks |
| **Amazon VPC** | Custom networking (subnets, route tables, IGW, security groups) |
| **IAM** | Task execution role (ECS → ECR/CloudWatch) and a scoped-down CI/CD user |
| **CloudWatch Logs** | Container logs |
| **Application Auto Scaling** | Scales ECS tasks (1–3) based on average CPU utilization (target: 50%) |
| **GitHub Actions** | CI/CD — builds, pushes, and deploys on every push to `main` |

## Tech stack

- **Backend:** Python, Flask, gunicorn
- **Frontend:** HTML/CSS (no JS framework) — CSS-animated rotating Earth using a real equirectangular texture
- **Infra tooling:** AWS CLI, Bash/CMD scripts, Docker CLI

## CI/CD pipeline

Every push to `main` triggers a GitHub Actions workflow that:
1. Builds the Docker image
2. Pushes it to ECR (tagged with commit SHA + `latest`)
3. Pulls the current ECS task definition and swaps in the new image
4. Registers a new task definition revision
5. Updates the ECS service and waits for the deployment to stabilize

See [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

## Cost considerations

- **No NAT Gateway** — public subnets with security-group-restricted access instead, avoiding the ~$0.045/hr + data charge
- **Smallest Fargate task size** — 0.25 vCPU / 0.5 GB memory
- **`desired-count: 1`** baseline, scaling up to 3 only under load
- Running components with an ongoing cost: 1 ALB (~$0.0225/hr) + 1 Fargate task + minimal ECR storage

## Local development

```bash
git clone https://github.com/johan06-cloud/ecs-docker-project.git
cd ecs-docker-project
pip install -r requirements.txt
python app.py
# visit http://localhost:5000
```

## Run with Docker locally

```bash
docker build -t cloudsearch-app .
docker run -p 5000:5000 cloudsearch-app
```

## Author

**Johan (A. Johan)**
Computer Science Engineering, Sri Venkateswara College of Engineering
[LinkedIn](https://linkedin.com/in/a-johan) · a.johan10613@gmail.com

Part of a series of hands-on AWS cloud engineering projects:
1. [Cloud Resume Challenge](https://github.com/johan06-cloud/cloud-resume-project) — S3, CloudFront, Lambda, API Gateway, DynamoDB
2. 3-Tier VPC Architecture — VPC, EC2, RDS MySQL, NAT Gateway
3. **CloudSearch on ECS Fargate** (this project) — Docker, ECR, ECS, ALB, auto-scaling, CI/CD