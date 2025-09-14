provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "lambda_role" {
  name = "elevenlabs_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "arn:aws:s3:::elevenlabs-demo-bucket-*/*"
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = data.aws_secretsmanager_secret.elevenlabs_api_key.arn
      }
    ]
  })
}

data "aws_secretsmanager_secret" "elevenlabs_api_key" {
  name = "elevenlabs-api-key"
}

resource "aws_s3_bucket" "demo_bucket" {
  bucket = "elevenlabs-demo-bucket-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  lower   = true
  upper   = false
}

resource "aws_lambda_function" "voice_test" {
  function_name    = "elevenlabs_voice_test"
  handler          = "index.handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_role.arn
  filename         = "../lambda_function.zip"
  source_code_hash = filebase64sha256("../lambda_function.zip")
  timeout          = 30 # Add this line
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.demo_bucket.bucket
      SECRET_NAME = data.aws_secretsmanager_secret.elevenlabs_api_key.name
    }
  }
}
