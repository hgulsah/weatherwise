# 🌍 WeatherWise

A weather-based recommendation app — built with Python, containerized with Docker, and deployed on Kubernetes via Argo CD GitOps workflow.

🔗 **Live:** http://aa1b60212da384b35a0f44864d913eef-1667060396.us-east-1.elb.amazonaws.com

## What it does

Enter any city and get personalized recommendations based on current weather conditions:

- ☂️ Rainy → Take an umbrella + Rainy Day Playlist
- ☀️ Hot & sunny → Apply sunscreen, stay hydrated
- ⚡ Thunderstorm → Stay home + Must-watch films list
- ❄️ Snowy → Warm up + Cozy playlist
- 😎 Beautiful day → Be grateful, go for a walk!

## Tech Stack

- **Python Flask** — web application
- **OpenWeatherMap API** — weather data
- **Docker** — containerization
- **Kubernetes (EKS)** — container orchestration
- **Argo CD** — GitOps deployment
- **AWS ELB** — external access

## Architecture

Code change → Docker build → Docker Hub push → Git push → Argo CD sync → EKS deploy

## Screenshots

### Home
![WeatherWise Home](screenshots/weatherwise-home.png)

### Result
![WeatherWise Result](screenshots/weatherwise-result.png)

## Repository Structure
app/
├── main.py              # Flask application
└── requirements.txt     # Python dependencies
k8s/
├── deployment.yaml      # Kubernetes Deployment
├── service.yaml         # Kubernetes Service (LoadBalancer)
└── argocd-app.yaml      # Argo CD Application
Dockerfile               # Container build instructions

