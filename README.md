# Exchange Rate App - Python ECS

A modern, responsive currency converter web application built with Python Flask, containerized with Docker, and deployed on AWS ECS with complete CI/CD pipeline integration.

## 🌟 Features

- **Real-time Exchange Rates**: Fetches live currency exchange rates from external API
- **Interactive Web Interface**: Modern, responsive UI with currency swap functionality
- **RESTful API**: JSON endpoints for programmatic access
- **Containerized**: Docker-ready with health checks
- **Cloud-Native**: AWS ECS deployment with Application Load Balancer
- **CI/CD Pipeline**: Automated testing, security scanning, and deployment
- **Infrastructure as Code**: Complete Terraform configuration
- **Security**: Integrated vulnerability scanning with Trivy and Bandit

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │   AWS ECS        │    │  External API   │
│   Actions       │───▶│   Fargate        │───▶│  Exchange Rates │
│   CI/CD         │    │   Load Balancer  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker
- AWS CLI configured
- Terraform (for infrastructure deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd exchange-rate-app-python-ecs
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Web Interface: http://localhost:5000
   - API Endpoints: http://localhost:5000/api

### Docker Development

1. **Build the Docker image**
   ```bash
   docker build -t exchange-rate-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 exchange-rate-app
   ```

## 📋 API Endpoints

### Web Interface
- `GET /` - Main currency converter interface

### API Endpoints
- `POST /convert` - Convert currency amounts
- `GET /currencies` - Get list of available currencies
- `GET /rates?base=USD` - Get exchange rates for base currency

### API Usage Examples

**Convert Currency:**
```bash
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currency": "EUR"}'
```

**Get Available Currencies:**
```bash
curl http://localhost:5000/currencies
```

**Get Exchange Rates:**
```bash
curl http://localhost:5000/rates?base=USD
```

## 🧪 Testing

### Run Tests Locally
```bash
# Install test dependencies
pip install pytest

# Run tests
python -m pytest test_app.py -v
```

### Test Coverage
- Unit tests for currency conversion logic
- API endpoint testing
- Integration tests for external API calls

## 🏗️ Infrastructure Deployment

### AWS Infrastructure

The application deploys to AWS using Terraform with the following components:

- **VPC**: Custom VPC with public subnets
- **ECS Cluster**: Fargate-based container orchestration
- **Application Load Balancer**: Traffic distribution and health checks
- **ECR Repository**: Container image storage
- **CloudWatch**: Logging and monitoring
- **Security Groups**: Network access control

### Deploy with Terraform

1. **Initialize Terraform**
   ```bash
   cd terraform
   terraform init
   ```

2. **Plan deployment**
   ```bash
   terraform plan
   ```

3. **Deploy infrastructure**
   ```bash
   terraform apply
   ```

### Quick Deploy Script

Use the provided deployment script for automated deployment:

```bash
./deploy.sh
```

This script will:
- Validate prerequisites
- Deploy infrastructure with Terraform
- Build and push Docker image to ECR
- Update ECS service
- Provide application URL

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:

### Code Quality & Testing
- **Linting**: Flake8 code quality checks
- **Security Scanning**: Bandit for Python security issues
- **Dependency Scanning**: Safety for vulnerable dependencies
- **Unit Tests**: Pytest execution
- **SonarQube**: Code quality analysis

### Security Scanning
- **Container Scanning**: Trivy vulnerability scanner
- **Filesystem Scanning**: Security analysis of source code
- **SARIF Upload**: Integration with GitHub Security tab

### Deployment
- **ECR Integration**: Automated image builds and pushes
- **ECS Deployment**: Zero-downtime service updates
- **Environment Variables**: Secure configuration management

### Required GitHub Secrets

```bash
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
SONAR_TOKEN=<your-sonar-token>
SONAR_HOST_URL=<your-sonar-url>
```

## 📁 Project Structure

```
exchange-rate-app-python-ecs/
├── .github/
│   └── workflows/
│       └── pipeline.yml          # CI/CD pipeline configuration
├── terraform/
│   ├── main.tf                   # Main infrastructure configuration
│   ├── variables.tf              # Terraform variables
│   └── outputs.tf                # Infrastructure outputs
├── app.py                        # Main Flask application
├── requirements.txt              # Python dependencies
├── test_app.py                   # Unit tests
├── Dockerfile                    # Container configuration
├── deploy.sh                     # Deployment automation script
└── README.md                     # Project documentation
```

## 🔧 Configuration

### Environment Variables

- `PORT`: Application port (default: 5000)
- `AWS_REGION`: AWS deployment region (default: eu-west-2)

### Terraform Variables

- `aws_region`: AWS region for deployment
- `project_name`: Project name for resource naming

## 🛡️ Security Features

- **Container Security**: Multi-stage Docker builds with minimal base images
- **Network Security**: VPC with security groups and NACLs
- **Vulnerability Scanning**: Automated security scans in CI/CD
- **Dependency Management**: Regular security updates
- **Health Checks**: Application and container health monitoring

## 📊 Monitoring & Logging

- **CloudWatch Logs**: Centralized application logging
- **Health Checks**: Load balancer and container health monitoring
- **Metrics**: ECS service and application metrics
- **Alerts**: Configurable monitoring alerts

## 🚀 Production Considerations

### Scaling
- **Auto Scaling**: Configure ECS service auto-scaling based on CPU/memory
- **Load Balancing**: Application Load Balancer distributes traffic
- **Multi-AZ**: Deployment across multiple availability zones

### Performance
- **Caching**: Consider implementing Redis for exchange rate caching
- **CDN**: CloudFront for static asset delivery
- **Database**: RDS for persistent data storage if needed

### Security
- **HTTPS**: Configure SSL/TLS certificates
- **WAF**: Web Application Firewall for additional protection
- **Secrets**: Use AWS Secrets Manager for sensitive configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Docker Build Fails:**
- Ensure Docker is running
- Check Dockerfile syntax
- Verify base image availability

**Terraform Deployment Issues:**
- Verify AWS credentials
- Check region availability
- Ensure required permissions

**Application Not Accessible:**
- Check security group rules
- Verify load balancer health checks
- Review CloudWatch logs

### Support

For issues and questions:
1. Check existing GitHub issues
2. Review CloudWatch logs
3. Verify AWS service status
4. Create a new issue with detailed information

---

**Built with ❤️ using Python, Flask, Docker, AWS ECS, and Terraform**
