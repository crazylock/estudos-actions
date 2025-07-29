# Reusable Workflow: Build and Push to AWS ECR

This repository exposes a reusable GitHub Actions workflow that performs the following steps:

1. Authenticates to AWS via OIDC.
2. Logs in to Amazon ECR.
3. Builds and pushes the Docker image using `docker/build-push-action@v5` with optional build arguments.
4. Pushes the image to the specified ECR repository.

## Usage

Call the workflow from another repository using `workflow_call`:

```yaml
jobs:
  build_push:
    uses: <org>/reusable-ecr-action/.github/workflows/build-push-ecr.yml@main
    with:
      aws-region: us-east-1
      ecr-repository: my-repo
      image-tag: ${{ github.sha }}
      build-args: |
        ARG1=value1
        ARG2=value2
    secrets:
      AWS_ROLE_TO_ASSUME: arn:aws:iam::123456789012:role/MyOidcRole
      AWS_ACCOUNT_ID: 123456789012
```
