# CDK Microservices Platform

A professional-grade AWS CDK infrastructure template for deploying containerized microservices with automated scaling, database support, and secure networking.

## Features

- **Multi-Environment Support**: Configure different environments (dev, staging, prod) through JSON configuration
- **ECS Deployment Options**:
  - Task-based deployments for batch jobs and scheduled tasks
  - Service-based deployments with Auto Scaling for long-running applications
- **Infrastructure Components**:
  - VPC with customizable subnet configurations
  - RDS PostgreSQL databases with automated backups
  - S3 buckets with proper IAM permissions
  - ECR repositories for container images
  - ECS clusters with Fargate and EC2 support
  - Security groups for web and database access

## Prerequisites

- AWS CLI configured with appropriate credentials
- Python 3.8+
- Node.js 14+ (for AWS CDK)
- AWS CDK CLI (`npm install -g aws-cdk`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cdk-microservices-platform.git
cd cdk-microservices-platform
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. Create a `.env` file with your AWS credentials:
```env
CDK_DEFAULT_ACCOUNT=your_account_number
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
region=your_preferred_region
```

## Usage

1. Configure your infrastructure in `configs/project_config.json`:
```json
{
  "projects": [
    {
      "name": "my-application",
      "deployments": [
        {
          "deployment_name": "web-service",
          "ram": 2,
          "cpu": 1,
          "disk": 20,
          "type": "service"
        }
      ],
      "database": {
        "name": "my-application-db",
        "storage": 20
      }
    }
  ]
}
```

2. Deploy your infrastructure:
```bash
cdk deploy
```

3. Update container images:
```bash
./update_image.sh web-service my-registry/my-image:latest
```

## Project Structure

- `/infrastructure`: Core CDK infrastructure components
  - `vpc.py`: VPC and networking configuration
  - `ecs.py`: ECS cluster and service definitions
  - `database.py`: RDS database setup
  - `s3.py`: S3 bucket configuration
  - `iam.py`: IAM roles and policies
- `/configs`: Configuration management
- `/ci_templates`: CI/CD pipeline templates

## Development

1. Install pre-commit hooks:
```bash
pre-commit install
```

2. Run tests:
```bash
pytest
```

3. Lint code:
```bash
ruff check .
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AWS CDK team for their excellent infrastructure framework
- The Python community for inspiration and best practices