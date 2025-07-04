locals {
  policies_infra = [
    "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
  ]

  policies_app = [
    "arn:aws:iam::aws:policy/AWSCodeDeployFullAccess",
    "arn:aws:iam::aws:policy/AWSLambda_FullAccess",
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  ]
}

locals {
  selected_policies = var.repo_type == "infra" ? local.policies_infra : local.policies_app
}

resource "aws_iam_role_policy_attachment" "attach_policies" {
  for_each = toset(local.selected_policies)

  role       = aws_iam_role.repo_role.name
  policy_arn = each.value
}

