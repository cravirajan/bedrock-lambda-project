# Bedrock Lambda Project

This project demonstrates a Lambda function that uses Amazon Bedrock for embeddings and text generation.

## Prerequisites
- Python 3.9+
- AWS account with access to Amazon Bedrock
- AWS credentials configured in your environment

## Setup

1. **Clone the repository**:
git clone https://github.com/yourusername/bedrock-lambda-project.git  cd bedrock-lambda-project


2. **Create a virtual environment**:
python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate


3. **Install dependencies**:
pip install -r requirements.txt


4. **AWS Authentication**:
Ensure AWS credentials are configured with appropriate permissions for Amazon Bedrock:
- Using AWS CLI: `aws configure`
- Or set environment variables:
  ```
  export AWS_ACCESS_KEY_ID=your_access_key
  export AWS_SECRET_ACCESS_KEY=your_secret_key
  export AWS_REGION=us-east-1
  ```

5. **Run the test**:
python test_local.py


## Project Structure
- `lambda_function.py`: The main Lambda function code
- `test_local.py`: Local test script
- `requirements.txt`: Project dependencies
