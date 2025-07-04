resource "aws_iam_role" "repo_role" {
  name = "oca-github-repo-${var.repo_id}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = "arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com"
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:<your-org>/${var.repo_id}:*"
        }
      }
    }]
  })
}

