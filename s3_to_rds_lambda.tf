provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "s3_to_rds_lambda" {
  name = "s3-to-rds-lambda"
}

resource "aws_s3_bucket" "s3_to_rds_lambda" {
  bucket = "s3-to-rds-lambda"
  acl    = "private"
}

resource "aws_iam_user" "jenkins_docker_builder" {
  name = "jenkins-docker-builder"
}

resource "aws_iam_access_key" "jenkins_docker_builder" {
  user = aws_iam_user.jenkins_docker_builder.name
}

resource "aws_iam_user_policy" "jenkins_docker_builder_policy" {
  name = "jenkins-docker-builder-policy"
  user = aws_iam_user.jenkins_docker_builder.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["ecr:GetAuthorizationToken"]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action   = ["ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage"]
        Effect  
